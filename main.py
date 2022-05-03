from fastapi import FastAPI


app = FastAPI()

# Exe command : uvicorn main:app --reload
@app.get("/")
def read_root():
    return {"message": "Welcome to Fast API"}
