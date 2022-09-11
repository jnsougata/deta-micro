from __future__ import annotations
from fastapi import FastAPI
from functools import wraps
from typing import Callable
import inspect
from deta import Deta
import os
import traceback
from typing import Optional
from .utils import *


class Micro(FastAPI):

    _exportable: Micro = None

    @property
    def deta(self) -> Optional[Deta]:
        try:
            return Deta()
        except Exception:
            return None

    @staticmethod
    def startup_task(func: Callable) -> None:
        if not inspect.iscoroutinefunction(func):
            try:
                func()
            except:
                pass

    def cron(self, func: Callable) -> None:
        if single_arged(func) and not coro(func):
            try:
                from detalib.app import App
            except ImportError:
                pass
            else:
                def invoker(event):
                    resource = event.__dict__
                    return func(resource)
                app = App(self)
                app.lib._cron.populate_cron(invoker)
                self._exportable = app

    @property
    def export(self) -> Micro:
        return self._exportable or self
