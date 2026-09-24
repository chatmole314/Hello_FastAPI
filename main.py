from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def say_hello() -> dict[str, str]:
    return {"message": "Hello World"}
