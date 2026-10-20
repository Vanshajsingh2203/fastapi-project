from src.db.models import Reviews
from src.Auth.service import UserService
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ReviewCreateModel, ReviewModel
from fastapi.exceptions import HTTPException
from fastapi import status
from src.db.models import Reviews
from sqlmodel import select, desc
import logging

book_service = BookService()
User_service = UserService()

class ReviewService:
    
    async def add_review_to_book(self, user_email: str , book_uid: str,review_data: ReviewCreateModel,  session: AsyncSession)  :
        try:
            book = await book_service.get_book(
                book_uid = book_uid, 
                session= session
            )
            user = await User_service.get_user_by_email(
                email = user_email , 
                session = session
            )
            review_data_dict = review_data.model_dump()
            new_review = Reviews(
                **review_data_dict
            )
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail = "Book not found"
                )
                
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail = "User not found"
                                    )
            new_review.user = user
            new_review.book = book
            session.add(new_review)
            
            await session.commit()
            
            return new_review
        except Exception as e:
            logging.exception(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail="OOPs.... Something went wrong")
            
    async def get_review(self, review_uid:str, session: AsyncSession):
        statement = select(Reviews).where(review_uid== Reviews.uid)
        
        result = await session.exec(statement)
        
        return result.first()
        
    async def get_all_reviews(self , sesion: AsyncSession):
        
        statement = select(Reviews).order_by(desc(Reviews.created_at))
        
        result = await sesion.exec(statement)
        
        return result.all()
    
    async def delete_review_to_from_book(self, review_uid: str , user_email: str, session: AsyncSession):
        user = await User_service.get_user_by_email(user_email, session)
        
        review = await self.get_review(review_uid, session)
        
        if not review or (review.user is not user):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail = "Cannot delete this review")
            
        session.add(review)
        
        await session.commit()        