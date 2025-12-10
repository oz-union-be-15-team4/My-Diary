from fastapi import APIRouter, Depends, status, HTTPException
import random

from app.models.quote import Quote
from app.schemas.quote import QuoteRead
from app.models.quote import Quote
from app.schemas.bookmark import BookmarkCreate
from app.schemas.bookmark import BookmarkCreate
from app.routers.user import get_current_user
from app.models.user import User
from app.models.bookmark import Bookmark

router = APIRouter(prefix="/quotes", tags=["quotes"])


@router.get("/random", response_model=QuoteRead)
async def get_random_quotes() -> QuoteRead:
    quote = await Quote.all()

    if not quote:
        raise HTTPException(status_code=404, detail="No auotes available")

    quote = random.choice(quote)

    return quote

@router.post("/bookmark")
async def bookmark_quote(
    data: BookmarkCreate,
    user: User = Depends(get_current_user)
):
    # quote 존재 여부 체크
    quote = await Quote.get_or_none(id=data.quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    # 이미 북마크 되었는지 확인
    existing = await Bookmark.filter(user=user, quote=quote).first()

    if existing:
        return {"detail": "Already bookmarked"}

    # 새로운 북마크 생성
    await Bookmark.create(user=user, quote=quote)

    return {"detail": "Bookmark created"}

@router.get("/bookmarks")
async def get_bookmarks(user: User = Depends(get_current_user)):
    bookmarks = await Bookmark.filter(user=user).prefetch_related("quote")

    # 필요한 형태로 변환해서 보내기
    result = [
        {
            "id": b.quote.id,
            "title": b.quote.title,
            "content": b.quote.content,
            "author": b.quote.author,
            "category": b.quote.category,
        }
        for b in bookmarks
    ]

    return result

@router.delete("/{quote_id}/bookmark")
async def remove_bookmark(
    quote_id: int,
    user: User = Depends(get_current_user),
):
    # 해당 quote 존재 여부 체크 (선택사항)
    quote = await Quote.get_or_none(id=quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    # 해당 유저의 해당 quote 북마크만 찾아서 삭제
    bookmark = await Bookmark.get_or_none(user=user, quote=quote)
    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found",
        )

    await bookmark.delete()

    return {"detail": "Bookmark removed"}