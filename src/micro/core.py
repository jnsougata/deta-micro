from __future__ import annotations
from fastapi import FastAPI
from functools import wraps
from typing import Callable
import inspect
from deta import Deta
import os


class Micro(FastAPI):

    _corn: Callable = None

    @property
    def deta(self) -> Deta:
        return Deta(os.getenv("DETA_PROJECT_KEY"))

    @classmethod
    def corn(cls, func: Callable):
        if not inspect.iscoroutinefunction(func) and len(inspect.getfullargspec(func).args) == 1:
            cls._corn = func

    @property
    def export(self) -> Micro:
        try:
            from detalib.app import App
            from detalib.app import Corn
        except ImportError:
            return self
        else:
            def wrapped_corn(event):
                return self._corn(event)
            app = App(self)
            if self._corn:
                corn = Corn()
                corn.populate_cron(wrapped_corn)
                app.lib._corn = corn
            return app
