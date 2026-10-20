from fastapi import APIRouter, status, Depends
from .service import TagService
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.Auth.dependencies import RoleChecker
from src.books.schemas import Book
from src.errors import BookNotFound, TagNotFound

from .schemas import TagCreateModel ,TagAddModel, TagModel

tags_router = APIRouter()
tags_service = TagService()
user_role_checker = Depends(RoleChecker(["user", "admin"]))

@tags_router.get("/",response_model =List[TagModel], dependencies=[user_role_checker])
async def get_all_tags(session:AsyncSession = Depends(get_session)):
    tags = await tags_service.get_tags(session)
    
    return tags

@tags_router.post("/", response_model = TagModel, 
                  status_code=status.HTTP_201_CREATED, 
                  dependencies= [user_role_checker]
)
async def add_tag(tag_data: TagCreateModel, session:AsyncSession = Depends(get_session))-> TagModel:
    
    tag_added = await tags_service.add_tag(tag_data, session)
    
    return tag_added

@tags_router.post("/book/{book_uid}/tags", response_model = Book, dependencies = [user_role_checker])
async def add_tags_to_book(book_uid: str,tag_data: TagAddModel, session: AsyncSession = Depends(get_session))->Book:
    
    book_with_tag = await tags_service.add_tags_to_book(book_uid, tag_data, session)
    
    return book_with_tag

@tags_router.put("/{tag_uid}", response_model = TagModel, dependencies=[user_role_checker])
async def update_tag(
    tag_uid: str,
    tag_update_data: TagCreateModel,
    session: AsyncSession = Depends(get_session)
)-> TagModel:
    
    updated_tag = await tags_service.update_tag(tag_uid, tag_update_data, session)
    
    return updated_tag

@tags_router.delete("/{tag_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[user_role_checker])
async def delete_tag(tag_uid: str, session:AsyncSession = Depends(get_session))->None:
    
    updated_tag = await tags_service.delete_tag(tag_uid, session)
    return updated_tag
    

    