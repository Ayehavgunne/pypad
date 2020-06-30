from pathlib import Path

import yaml
from uvicorn import Server, Config
from tonberry import expose, File, create_app
from tonberry.content_types import TextHTML, ApplicationJson

local_path = Path(__file__) / ".."


class Root:
    @expose.get
    async def index(self) -> TextHTML:
        return File(local_path / "resources" / "config_man.html")

    @expose.get
    async def get_mappings(self) -> ApplicationJson:
        with (local_path / ".." / "mappings.yaml").open() as fh:
            mappings = yaml.load(fh, Loader=yaml.FullLoader)
            return mappings


async def start_server() -> None:
    app = create_app(Root)
    app.add_static_route(local_path / "resources")
    config = Config(app, port=1337, log_level="warning")
    server = Server(config=config)
    await server.serve()


if __name__ == "__main__":
    import asyncio

    asyncio.run(start_server())
