from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI()

numbers = [
    1, 2, 3, 4
]



@app.get("/")
def home():
    return numbers

@app.get("/numbers")
def get_numbers():
    return numbers

@app.post("/add_numbers")
def add_numbers(number: int):
    numbers.append(number)

@app.get("/get_number",
         tags=["Книги"],
         summary="Получить конкретный элемент массива")
def get_number(number_id: int):
    return numbers[number_id]

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)