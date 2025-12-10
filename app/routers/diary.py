from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# Mock User 및 DB Session Import 가정
from app.models.diary import Diary as DiaryModel
from app.schemas.diary import DiaryCreate, DiaryUpdate, DiaryResponse
from app.dependencies.auth import get_current_user # 현재 사용자 정보를 가져오는 함수 (Mock)
# from app.database import get_db

router = APIRouter(prefix="/diaries", tags=["일기 CRUD"])

# 📝 [CREATE] 일기 작성
@router.post("/", response_model=DiaryResponse, status_code=status.HTTP_201_CREATED)
async def create_diary(
    diary_in: DiaryCreate, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user) # 인증 사용자에게 의존
):
    new_diary = DiaryModel(
        title=diary_in.title,
        content=diary_in.content, 
        user_id=current_user.id 
    )
    db.add(new_diary)
    db.commit()
    db.refresh(new_diary)
    return new_diary

# 📖 [READ] 내 일기 목록 조회
@router.get("/", response_model=list[DiaryResponse])
async def read_diaries(
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    diaries = db.query(DiaryModel).filter(DiaryModel.user_id == current_user.id).all()
    return diaries

# ✏️ [UPDATE] 일기 수정 (작성자 본인 권한 처리)
@router.put("/{diary_id}", response_model=DiaryResponse)
async def update_diary(
    diary_id: int, 
    diary_in: DiaryUpdate, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    diary = db.query(DiaryModel).filter(DiaryModel.id == diary_id).first()
    
    if not diary:
        raise HTTPException(status_code=404, detail="일기를 찾을 수 없습니다.")
    
    # 🔑 작성자 본인만 수정 권한 확인
    if diary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="수정 권한이 없습니다.")
    
    update_data = diary_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(diary, key, value)
    
    db.commit()
    db.refresh(diary)
    return diary

# 🗑️ [DELETE] 일기 삭제 (작성자 본인 권한 처리)
@router.delete("/{diary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diary(
    diary_id: int, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    diary = db.query(DiaryModel).filter(DiaryModel.id == diary_id).first()
    
    if not diary:
        raise HTTPException(status_code=404, detail="일기를 찾을 수 없습니다.")
        
    # 🔑 작성자 본인만 삭제 권한 확인
    if diary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="삭제 권한이 없습니다.")
    
    db.delete(diary)
    db.commit()
    return