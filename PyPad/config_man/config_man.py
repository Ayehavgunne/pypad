import asyncio
from pathlib import Path

import yaml
from tonberry import File, create_app, expose
from tonberry.content_types import ApplicationJson, TextHTML, TextPlain
from uvicorn import Config, Server

from PyPad.monitor import monitor

local_path = Path(__file__).parent


class Root:
    @expose.get
    async def index(self) -> TextHTML:
        return File(local_path / "resources" / "config_man.html")

    @expose.get
    async def get_mappings(self) -> ApplicationJson:
        with (local_path.parent / "mappings.yaml").open() as fh:
            mappings = yaml.load(fh, Loader=yaml.FullLoader)
            return mappings

    @expose.get
    async def get_app(self) -> TextPlain:
        return "true"


async def start_server() -> None:
    print("Starting up")
    app = create_app(Root)
    app.add_static_route(local_path / "resources", route="/static")
    config = Config(app, port=1337, log_level="warning")
    server = Server(config=config)
    asyncio.create_task(monitor())
    await server.serve()
