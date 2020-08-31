import subprocess
import sys
from logging import INFO, FileHandler, Formatter, getLogger
from pathlib import Path

import servicemanager
import win32event
import win32service
import win32serviceutil

FILE_DIR = Path(__file__).parent


def _main():
    if (
        len(sys.argv) == 1
        and sys.argv[0].endswith(".exe")
        and not sys.argv[0].endswith(r"win32\PythonService.exe")
    ):
        # invoked as non-pywin32-PythonService.exe executable without
        # arguments

        # We assume here that we were invoked by the Windows Service
        # Control Manager (SCM) as a PyInstaller executable in order to
        # start our service.

        # Initialize the service manager and start our service.
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(WinService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        # invoked with arguments, or without arguments as a regular
        # Python script

        # We support a "help" command that isn't supported by
        # `win32serviceutil.HandleCommandLine` so there's a way for
        # users who run this script from a PyInstaller executable to see
        # help. `win32serviceutil.HandleCommandLine` shows help when
        # invoked with no arguments, but without the following that would
        # never happen when this script is run from a PyInstaller
        # executable since for that case no-argument invocation is handled
        # by the `if` block above.
        if len(sys.argv) == 2 and sys.argv[1] == "help":
            sys.argv = sys.argv[:1]

        win32serviceutil.HandleCommandLine(WinService)


def _configure_logging():
    formatter = Formatter("%(message)s")

    handler = FileHandler("C:/Users/posta/logs/pypad_service.log")
    handler.setFormatter(formatter)

    logger = getLogger("pypad_service")
    logger.addHandler(handler)
    logger.setLevel(INFO)
    return logger


class WinService(win32serviceutil.ServiceFramework):
    """Base class to create winservice in Python"""

    _svc_name_ = "PyPad Service"
    _svc_display_name_ = "PyPad Service"
    _svc_description_ = "PyPad Keyboard Monitor and Config Server"
    _app_exe_name_ = "run_server.py"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self._stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.logger = _configure_logging()

    def GetAcceptedControls(self):
        result = win32serviceutil.ServiceFramework.GetAcceptedControls(self)
        result |= win32service.SERVICE_ACCEPT_PRESHUTDOWN
        return result

    def SvcDoRun(self):
        self.logger.info("has started")

        # determine if application is a script file or frozen exe
        if getattr(sys, "frozen", False):
            application_path = Path(sys.executable).parent
        else:
            application_path = FILE_DIR

        exe_name = (application_path / self._app_exe_name_).as_posix()
        self.logger.info(f"launching subprocess for {exe_name}")

        if exe_name.endswith(".py"):
            p = subprocess.Popen(["python", exe_name])
        else:
            p = subprocess.Popen([exe_name])

        self.logger.info(f"is running in subprocess id {p.pid}")

        while True:
            result = win32event.WaitForSingleObject(self._stop_event, 5000)
            self.logger.info(f"checking subprocess id {p.pid}: {p.poll()}")

            if result == win32event.WAIT_OBJECT_0:
                # stop requested
                self.logger.info(f"output err: '{p.stderr}', out: '{p.stdout}'")
                self.logger.info("is stopping")
                p.kill()
                break

        self.logger.info("has stopped")

    def SvcOtherEx(self, control, event_type, data):
        # See the MSDN documentation for "HandlerEx callback" for a list
        # of control codes that a service can respond to.
        #
        # We respond to `SERVICE_CONTROL_PRESHUTDOWN` instead of
        # `SERVICE_CONTROL_SHUTDOWN` since it seems that we can't log
        # info messages when handling the latter.
        if control == win32service.SERVICE_CONTROL_PRESHUTDOWN:
            self.logger.info("received a pre-shutdown notification")
            self._stop()
        else:
            self.logger.info(
                f"received an event: code={control}, type={event_type}, data={data}"
            )

    def _stop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self._stop_event)

    def SvcStop(self):
        self._stop()


if __name__ == "__main__":
    _main()
