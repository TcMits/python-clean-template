from typing import Any, Callable, Dict, Optional

import gunicorn.app.base
from starlette.types import Receive, Scope, Send


class GunicornApplication(gunicorn.app.base.BaseApplication):
    def __init__(
        self,
        handler: Callable[[Scope, Receive, Send], Any],
        options: Optional[Dict[str, Any]] = None,
    ):
        self.options = options or {}
        self.application = handler
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application
