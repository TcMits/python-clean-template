from contextlib import contextmanager
from unittest.mock import MagicMock


class Fake:
    def __init__(self):
        self.mock_funcs = []

    def query(self, *args, **kwargs):
        mock_func = MagicMock(return_value=self)
        mock_func(*args, **kwargs)
        self.mock_funcs.append(mock_func)
        return self

    def filter(self, *args, **kwargs):
        mock_func = MagicMock(return_value=self)
        mock_func(*args, **kwargs)
        self.mock_funcs.append(mock_func)
        return self

    def first(self, *args, **kwargs):
        mock_func = MagicMock(return_value=self)
        mock_func(*args, **kwargs)
        self.mock_funcs.append(mock_func)
        return self

    def order_by(self, *args, **kwargs):
        mock_func = MagicMock(return_value=self)
        mock_func(*args, **kwargs)
        self.mock_funcs.append(mock_func)
        return self

    def offset(self, *args, **kwargs):
        mock_func = MagicMock(return_value=self)
        mock_func(*args, **kwargs)
        self.mock_funcs.append(mock_func)
        return self

    def limit(self, *args, **kwargs):
        mock_func = MagicMock(return_value=self)
        mock_func(*args, **kwargs)
        self.mock_funcs.append(mock_func)
        return self

    def all(self, *args, **kwargs):
        mock_func = MagicMock(return_value=self)
        mock_func(*args, **kwargs)
        self.mock_funcs.append(mock_func)
        return self

    def add(self, *args, **kwargs):
        mock_func = MagicMock(return_value=self)
        mock_func(*args, **kwargs)
        self.mock_funcs.append(mock_func)
        return self

    def commit(self, *args, **kwargs):
        mock_func = MagicMock(return_value=self)
        mock_func(*args, **kwargs)
        self.mock_funcs.append(mock_func)
        return self

    def delete(self, *args, **kwargs):
        mock_func = MagicMock(return_value=self)
        mock_func(*args, **kwargs)
        self.mock_funcs.append(mock_func)
        return self

    def refresh(self, *args, **kwargs):
        mock_func = MagicMock(return_value=self)
        mock_func(*args, **kwargs)
        self.mock_funcs.append(mock_func)
        return self

    def with_for_update(self, *args, **kwargs):
        mock_func = MagicMock(return_value=self)
        mock_func(*args, **kwargs)
        self.mock_funcs.append(mock_func)
        return self

    def flush(self, *args, **kwargs):
        mock_func = MagicMock(return_value=self)
        mock_func(*args, **kwargs)
        self.mock_funcs.append(mock_func)
        return self

    @property
    @contextmanager
    def no_autoflush(self):
        mock_func = MagicMock(return_value=self)
        try:
            result = mock_func()
            self.mock_funcs.append(mock_func)
            yield result
        finally:
            pass
