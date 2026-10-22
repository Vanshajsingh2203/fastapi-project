from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from typing import List
from src.books.schemas import Book
from src.reviews.schemas import ReviewModel

class UserCreateModel(BaseModel):
    first_name: str =Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=14)
    email: str = Field(max_length=40)
    password: str = Field(min_lenth= 6)

class UserModel(BaseModel):
    uid: uuid.UUID 
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at : datetime 
    updated_at : datetime
    
class UserBooks(UserModel):
    books: List[Book]
    reviews : List[ReviewModel]
    
class UserLoginModel(BaseModel):
    
    email: str = Field(max_length=40)
    password: str = Field(min_lenth= 6)

class EmailModel(BaseModel):
    addresses : List[str]
    
class PasswordRequestModel(BaseModel):
    email: str
    
class PasswordResetConfirmModel(BaseModel):
    new_password : str
    confirm_new_password : str