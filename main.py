from src.micro import Micro

micro = Micro()


@micro.cron()
def corn_job(event):
    return "cron executed"


@micro.on_start()
def startup_task():
    print("micro deployed")


@micro.get("/")
async def index():
    return {"message": "Hello World"}

app = micro.export
