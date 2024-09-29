---
layout: post
title: "[python] SQLAlchemy를 통한 DB session 연결"
date: 2024-04-30 17:15:18 +0900
categories: python python이론
tag: [python, 파이썬, SQLAlchemy]
---

# SQLAlchemy란

Java의 `JPA`와 같이, Python의 `ORM` 라이브러리입니다.

Django를 사용할 경우 전용 ORM 모듈이 있으나(사실 이 또한 SQLAlchemy의 포크입니다),

FastAPI, Flask를 사용하거나 단순한 Python 실행 파일에서 DB와 연결이 필요할 경우

거의 무조건 쓰게 되는 라이브러리가 됩니다.

애석하게도 Python backend는 java spring에 비하면 비주류에 속하고,

그 작은 파이 안에서도 절대적 다수는 아직까지 Django입니다.

그렇기 때문에 SQLAlchemy에 대한 정보는 찾기가 쉽지 않은 편이죠.

[공식 문서](https://www.sqlalchemy.org/)도 있으나, 당연히 영어 버전밖에 없습니다.(그와중에 공식문서 테마가 심히 y2k스럽습니다.) 

FastAPI를 깊게 파면서, 당연히 SQLAlchemy도 깊게 팔 수밖에 없었고,

이를 통해 알게 된 정보들을 포스팅하고자 합니다.

<br>

## Session Maker를 활용한 다양한 연결 방식

### **1. Try-Yield-Finally 블럭활용**

[FastAPI는 다음과 같은 연결 방식](https://fastapi.tiangolo.com/ko/tutorial/sql-databases/#main-fastapi-app)을 권장합니다.

```python
from sqlalchemy import create_engine, Integer
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DB_URL = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
engine = create_engine(url=DB_URL)
session_maker = sessionmaker(bind=engine, autoflush=False)

# ==== 핵심입니다. =======
async def get_db():
    db = session_maker()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
# =====================

class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ == "items"
    item_id = Column(Integer, primary_key = True)

@app.get('/item')
async def get_item(n, db = Depends(get_db)):
    
    item = db.query(Item).get(n)

    return item
```

DB연결 정보를 담은 `engine`을 바탕으로 `session_maker`객체를 생성합니다.

`session_maker` 객체는 펑션 콜이 발생할 시, 새로운 세션(db)를 반환합니다.

FastAPI의 DI용 함수인 Depends를 통해 get_db 함수 자체를 객체로써 파라미터에 넣으면

해당 요청 내에서 db와 연결된 세션을 얻는 것이죠.

`Depends(get_db)`같은 의존성 주입 방식이 아닌 다른 방식을 쓸 수도 있습니다.

함수 내에서 session_maker의 펑션 콜을 직접 시행해도 괜찮습니다.

### **2. with 블럭을 통한 생명주기 자동 관리**

마치 file open을 `with`를 통해 안전하게 실행하는 것처럼,

`session`도 다음과 같이 `with`블럭을 통해 만들 수 있습니다.

```python
@app.get("/item")
async def get_item(n):
    with session_maker() as db:
        item = db.query(Item).get(n)
    # with 블럭 밖에서도 db 객체 사용이 가능하지만, 하면 안 됩니다!
    
    return item
```

`with`블럭에서 생성한 `session` 객체는 `with`블럭 밖에서도 사용이 가능합니다만,

사실상 **강제로 새 세션을 생성한 것**이므로, `with` __블럭의 자동 생명 주기 관리 범위를 벗어나게 되어 문제__가 발생합니다.

### **3. 그냥 만들기**

대단히 복잡해져 로직 상 문제가 생길 여지가 많아지고,

쓸 데 없는 반복으로 코드가 길어질 것이며,

한 번의 실수가 매우 치명적으로 다가오는 방법입니다.

```python
@app.get("/item")
async def get_item(n):
    db = session_maker()
    item = db.query(Item).get(n)
    db.close()
```

이 방법 자체를 쓰지 않았으면 하지만, 만약 쓴다면 세션 사용이 끝난 후에 반드시 `.close()`로 세션을 마쳐줘야 합니다.

그러지 않을 경우, session 객체가 DB와 Sqlalchemy의 소통 창구인 커넥션을 계속 점유하기 때문에 문제가 발생합니다.

이 문제는 다음 번에 다뤄보도록 하겠습니다!

## 요약

개인적으로는 session_maker를 쓸 경우 1번 방법을 가장 권하는 편입니다.

session_maker 방식이 아닌, engine.connect()를 통한 직접 연결 방식도 있으나,

웹 서버를 개발하고자 한다면 session_maker를 쓰는 게 훨씬 효율적이고 객체지향적입니다.

처음에는 3번을 사용하다가, 2번을 써보고, 1번으로 정착하게 되면서 확실히 느꼈습니다.

1번을 씁시다!