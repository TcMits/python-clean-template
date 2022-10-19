from typing import Any, Callable, Dict, Optional

import gunicorn.app.base
from starlette.types import Receive, Scope, Send


# copied from https://docs.gunicorn.org/en/latest/custom.html
class GunicornApplication(gunicorn.app.base.BaseApplication):
    def __init__(
        self,
        loader: Callable[[], Callable[[Scope, Receive, Send], Any]],
        options: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.options = options or {}
        self.__loader = loader
        super().__init__()

    def load_config(self) -> None:
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self) -> None:
        return self.__loader()
