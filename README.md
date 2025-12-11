# 나만의 일기
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.124-009688?style=flat-square&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)

## 프로젝트 소개
사용자가 매일 일기를 작성하며 자신의 생각을 정리할 수 있도록 돕는 개인 맞춤형 일기 및 자기 관리 서비스

### 주요 기능

| 기능 | 설명 |
|------|------|
| **회원가입/로그인** | JWT을 이용한 사용자 인증 및 세션 관리 |
| **일기 CRUD** | 일기 작성, 조회, 수정, 삭제 (본인만 접근 가능) |
| **오늘의 명언** | 랜덤 명언 제공 및 명언 북마크 |
| **오늘의 질문** | 자기성찰 질문 랜덤 제공 |

## 기술 스택

### Backend
- **Framework**: FastAPI
- **ORM**: Tortoise ORM
- **Database**: PostgreSQL (Neon)
- **Authentication**: JWT (python-jose)

### Frontend
- **HTML5** + **TailwindCSS** + **Alpine.js**


## 프로젝트 구조
```
📦My-Diary
 ┣ 📂app
 ┃ ┣ 📂db
 ┃ ┃ ┗ 📜database.py
 ┃ ┣ 📂frontend
 ┃ ┃ ┣ 📂page
 ┃ ┃ ┃ ┣ 📜bookmarks.html
 ┃ ┃ ┃ ┣ 📜dashboard.html
 ┃ ┃ ┃ ┗ 📜diaries.html
 ┃ ┃ ┗ 📜index.html
 ┃ ┣ 📂models
 ┃ ┃ ┣ 📜bookmark.py
 ┃ ┃ ┣ 📜diary.py
 ┃ ┃ ┣ 📜question.py
 ┃ ┃ ┣ 📜quote.py
 ┃ ┃ ┗ 📜user.py
 ┃ ┣ 📂routers
 ┃ ┃ ┣ 📜diary.py
 ┃ ┃ ┣ 📜question.py
 ┃ ┃ ┣ 📜quote.py
 ┃ ┃ ┗ 📜user.py
 ┃ ┣ 📂schemas
 ┃ ┃ ┣ 📜bookmark.py
 ┃ ┃ ┣ 📜diary.py
 ┃ ┃ ┣ 📜question.py
 ┃ ┃ ┣ 📜quote.py
 ┃ ┃ ┗ 📜user.py
 ┃ ┣ 📂services
 ┃ ┗ ┗ 📜auth.py
 ┣ 📜README.md
 ┗ 📜main.py
```

## 접속 방법

http://3.34.197.233/

## 스크린샷

### 로그인 페이지

<img width="1600" height="851" alt="login" src="https://github.com/oz-union-be-15-team4/My-Diary/blob/meow/rogin.png" />

### 대시보드

<img width="1600" height="851" alt="dashboard" src="https://github.com/oz-union-be-15-team4/My-Diary/blob/meow/dashboard.png" />

### 일기 목록

<img width="1600" height="851" alt="diary" src="https://github.com/oz-union-be-15-team4/My-Diary/blob/meow/diary.png" />

### 북마크 목록

<img width="1600" height="851" alt="bookmark" src="https://github.com/oz-union-be-15-team4/My-Diary/blob/meow/bookmarks.png" />

## 라이선스

MIT License

## 개발자 

- **GitHub**: [@algorid](https://github.com/algorid), [@Ryu-GY](https://github.com/Ryu-GY), [@yoon-122](https://github.com/yoon-122)

  

