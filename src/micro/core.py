from __future__ import annotations
from fastapi import FastAPI
from functools import wraps
from typing import Callable
import inspect
from deta import Deta
import os
import asyncio


class Micro(FastAPI):

    _exportable: Micro = None

    @property
    def deta(self) -> Deta:
        return Deta(os.getenv("DETA_PROJECT_KEY"))

    @staticmethod
    def startup_task(func: Callable) -> None:
        if not inspect.iscoroutinefunction(func):
            func()
        else:
            asyncio.create_task(func())

    def cron(self, func: Callable) -> None:
        if not inspect.iscoroutinefunction(func) and len(inspect.getfullargspec(func).args) == 1:
            try:
                from detalib.app import App
            except ImportError:
                pass
            else:
                def wrapped_cron(event):
                    return func(event.__dict__)

                app = App(self)
                app.lib._cron.populate_cron(wrapped_cron)
                self._exportable = app

    @property
    def export(self) -> Micro:
        return self._exportable or self
