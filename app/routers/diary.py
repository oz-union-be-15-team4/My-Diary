from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from tortoise.exceptions import DoesNotExist

from app.models.user import User
from app.models.diary import Diary
from app.schemas.diary import DiaryCreate, DiaryUpdate, DiaryResponse
from app.routers.user import get_current_user

router = APIRouter(prefix="/diaries", tags=["일기 CRUD"])

@router.post("/", response_model=DiaryResponse, status_code=status.HTTP_201_CREATED)
async def create_diary(
    diary_in: DiaryCreate,
    current_user: User = Depends(get_current_user)
):
    new_diary = await Diary.create(
        **diary_in.model_dump(),
        user_id=current_user.id
    )
    return new_diary

@router.get("/", response_model=List[DiaryResponse])
async def read_diaries(
    current_user: User = Depends(get_current_user)
):
    diaries = await Diary.filter(user_id=current_user.id).order_by("created_at")
    return diaries

@router.get("/{id}", response_model=DiaryResponse)
async def get_diary(
    id: int,
    current_user = Depends(get_current_user),
):
    try:
        diary = await Diary.get(id=id, user_id=current_user.id)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diary not found"
        )

    return diary

@router.patch("/{diary_id}", response_model=DiaryResponse)
async def update_diary(
    diary_id: int,
    diary_in: DiaryUpdate,
    current_user: User = Depends(get_current_user)
):
    diary = await Diary.filter(id=diary_id).first()

    if not diary:
        raise HTTPException(status_code=404, detail="일기를 찾을 수 없습니다.")

    if diary.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="수정 권한이 없습니다.")

    update_data = diary_in.model_dump(exclude_unset=True)

    await diary.update_from_dict(update_data).save()

    return diary

@router.delete("/{diary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diary(
    diary_id: int,
    current_user: User = Depends(get_current_user)
):
    diary = await Diary.filter(id=diary_id).first()

    if not diary:
        raise HTTPException(status_code=404, detail="일기를 찾을 수 없습니다.")

    if diary.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="삭제 권한이 없습니다.")

    await diary.delete()
    return