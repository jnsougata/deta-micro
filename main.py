from src.micro import Micro

micro = Micro()


@micro.cron
def corn_job(event):
    return "corn_job executed"


@micro.get("/")
async def index():
    return {"message": "Hello World"}

app = micro.export
