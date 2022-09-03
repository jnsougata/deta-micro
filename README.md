# deta-micro
Deta Micro focused ASGI framework built on FastAPI

## Installation
```bash
pip install git+https://github.com/jnsougata/deta-micro.git
```

## Getting Started

```python
from micro import Micro
import random

micro = Micro()


@micro.cron
def corn_job(event: dict):
    return event


@micro.startup_task
def task_one():
    print("... micro deployed")


@micro.startup_task
def task_two():
    micro.deta.Base("test").put(random.randint(0, 100), "startup")
    print("... record initialized")


@micro.get("/")
async def index():
    return {"number": random.randint(0, 100)}

app = micro.export

```