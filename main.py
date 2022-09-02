from src.micro import Micro

micro = Micro()


@micro.cron
def corn_job(event):
    return "cron executed"


@micro.get("/")
async def index():
    return {"message": "Hello World"}

app = micro.export
