from fastapi import FastAPI

app = FastAPI(title="My Apis",
             description="Developer : Mirshad",
             docs_url=None,
             redoc_url=None)

#domain where this api is hosted for example : localhost:5000/docs to see swagger documentation automagically generated.


@app.get("/")
def home():
    return {"message":"Hello test"}
