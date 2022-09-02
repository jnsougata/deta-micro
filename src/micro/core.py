from __future__ import annotations
from fastapi import FastAPI
from functools import wraps
from typing import Callable
import inspect
from deta import Deta
import os


class Micro(FastAPI):

    _cron: Callable = None

    @property
    def deta(self) -> Deta:
        return Deta(os.getenv("DETA_PROJECT_KEY"))

    @classmethod
    def cron(cls, func: Callable):
        if not inspect.iscoroutinefunction(func) and len(inspect.getfullargspec(func).args) == 1:
            cls._cron = func

    @property
    def export(self) -> Micro:
        try:
            from detalib.app import App
            from detalib.app import Cron
        except ImportError:
            return self
        else:
            app = App(self)
            if self._cron:
                def wrapped_cron(event):
                    return self._cron(event)
                c = Cron()
                c.populate_cron(wrapped_cron)
                app.lib._cron = c
            return app
