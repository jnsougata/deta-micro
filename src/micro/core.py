from __future__ import annotations
from fastapi import FastAPI
from functools import wraps
from typing import Callable
import inspect
from deta import Deta
import os


class Micro(FastAPI):

    __exportable: Micro = None

    @property
    def deta(self) -> Deta:
        return Deta(os.getenv("DETA_PROJECT_KEY"))

    @classmethod
    def corn(cls, func: Callable):
        if not inspect.iscoroutinefunction(func) and len(inspect.getfullargspec(func).args) == 1:
            try:
                from detalib.app import App
                from detalib.app import Cron
            except ImportError:
                pass
            else:
                app = App(self)
                c = Cron()
                c.populate_cron(func)
                app.lib._cron = c
                cls.__exportable = app

    @property
    def export(self) -> Micro:
        return self.__exportable or self
