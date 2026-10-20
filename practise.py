from typing import Optional

from fastapi import FastAPI , Header
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
async def read_root():
    return {'message': 'Hello world'}

# Path parameter
@app.get('/greet/{name}')
async def greet_name(name: str) -> dict:
    return {"message": f"hello {name}"}

# Query Parameters
@app.get('/greet1')
async def greet1_name(name:str)-> dict:
    return {"message": f"Hello {name}"}

# Mix both the parameters
@app.get('/greet2/{name}')
async def greet2_name(name:str, age:int)->dict:
    return {'message':f'hello {name}', 'age':age}

@app.get('/greet3')
async def greet3_name(name:Optional[str]= 'User', age:int = 0)->dict:
    return {"message": f"Hello {name}", "age":age}

# request body  
class BookCreateModel(BaseModel):
    title: str
    author: str

@app.post('/create_book')
async def create_book(book_data: BookCreateModel):
    return {
        "title": book_data.title,
        "author": book_data.author
    }

@app.get('/get_headers')
async def get_headers(accept:str = Header(None), content_type: str = Header(None), 
                      user_agent:str = Header(None), host: str = Header(None), test:str = Header(None)
):
    request_headers = {}
    request_headers['Accept'] = accept
    request_headers["Content-Type"] = content_type
    request_headers['User-Agent'] = user_agent
    request_headers["Host"] = host
    request_headers["Test"] = test 
    return request_headers

