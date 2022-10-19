import os
import signal
import threading
import time
from typing import Any

from uvicorn.workers import UvicornWorker


class ReloaderThread(threading.Thread):
    def __init__(self, worker: UvicornWorker, sleep_interval: float = 1.0) -> None:
        super().__init__()
        self.setDaemon(True)
        self.__worker = worker
        self._interval = sleep_interval

    def run(self) -> None:
        while True:
            if not self.__worker.alive:
                os.kill(os.getpid(), signal.SIGINT)
            time.sleep(self._interval)


class RestartableUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {"loop": "uvloop", "http": "httptools"}

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        super().__init__(*args, **kwargs)
        self.__reloader_thread = ReloaderThread(self)

    def run(self) -> None:
        if self.cfg.reload:
            self.__reloader_thread.start()
        super().run()
