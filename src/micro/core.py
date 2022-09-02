from __future__ import annotations
from fastapi import FastAPI
from functools import wraps
from typing import Callable
import inspect
from deta import Deta
import os


class Micro(FastAPI):

    __cron: Callable = None

    @property
    def deta(self) -> Deta:
        return Deta(os.getenv("DETA_PROJECT_KEY"))

    @classmethod
    def cron(cls, func: Callable):
        if not inspect.iscoroutinefunction(func) and len(inspect.getfullargspec(func).args) == 1:
            cls.__cron = func

    @property
    def export(self) -> Micro:
        try:
            from detalib.app import App
            from detalib.app import Cron
        except ImportError:
            return self
        else:
            app = App(self)
            c = Cron()
            c.populate_cron(self.__cron)
            app.lib._cron = c
            return app
