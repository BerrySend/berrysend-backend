from fastapi import FastAPI

"""
Defines the base app component with FastAPI
"""
app = FastAPI(
    title="BerrySend Backend",
    description="API to register exports of blue berries anc calculate the shortest route",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {"Application is up and functioning"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
