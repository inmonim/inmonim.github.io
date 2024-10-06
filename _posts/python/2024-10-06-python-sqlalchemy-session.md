---
layout: post
title: "[python] SQLAlchemy - session.close()"
date: 2024-09-30 06:15:18 +0900
categories: python python이론
tag: [python, 파이썬, SQLAlchemy]
---

# **Session.close()**

>sqlalchemy.exc.TimeoutError: QueuePool limit of size 5 overflow 10 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
{: .prompt-danger}

>session.close()는 sqlalchemy에서 매우 중요한 명령어입니다.
{: .prompt-tip}

## 기본적으로 Python에서 .close()는 매우 중요합니다.

Python에서 txt 파일같은 여러 파일들을 가져다 쓸 때는 매우 중요한 과정입니다.

`with` 블럭이나 `.close()`메서드를 통해 반드시 자동(또는 명시적)으로 파일이 점유한 메모리를 해제해줘야 합니다.

Python의 가비지 컬렉터의 방식에 따라 참조 카운트(`reference count`)가 사라지면 자동으로 메모리를 해제하여 해주긴 합니다만

버퍼에 담긴 데이터를 close() 펑션 콜이 이루어진 순간 디스크에 저장한다는 특성 상,

close()가 명시적으로 이루어지지 않으면, 원본 데이터의 소실이나 원치 않는 변경이라는 문제가 생길 수도 있습니다.

그렇기에 with 블럭이나 try-finally를 통해 자동으로 파일을 close하는 과정이 필요합니다.

## SQLAlchemy의 Session도 마찬가지입니다.

```python
engine = create_engine()

Session = sessionmaker(bind=engine)

with Session() as db:
    # OR
  
db = Session()
db.add(...)
db.commit()
db.close()
```

세션 팩토리를 `펑션 콜` 하는 순간 `Session`이 `open()`되고, `with` 블럭을 탈출하는 순간 `session.close()`가 이루어집니다.

또는 후자의 방식대로 **명시적인** `close()`를 해줘야 합니다.

`session(db)`의 사용을 마친 뒤, 이를 닫지 않으면 문제가 발생하게 되는데요.

**커넥션 풀링 방식을 쓰는 SQLAlchemy는 DB와의 커넥션을 한번 쓰고 삭제하지 않습니다.**

커넥션은 유지하되, 요청이 들어올 때마다 **session은 커넥션 풀에 존재하는 미점유 상태의 커넥션을 가져와 사용**합니다.

원활한 쿼리를 위해서는 session사용이 끝난 뒤, 커넥션에 대한 점유를 해제하여 커넥션 풀로 빠르게 돌려보내야 하는 것이죠.

그렇지 않는다면 session은 요청이 끝난 뒤에도 계속 커넥션을 붙잡고 있기 때문에

**새로운 요청이 들어왔을 때 사실상 놀고 있는(무의미하게 점유당한) 커넥션을 사용하지 못합니다.**

그렇기 때문에

### Session을 닫지 않으면 커넥션을 계속 생성합니다.

커넥션에도 당연히 최대 개수가 존재하고, 이는 SQLAlchemy나 MySQL같은 DBMS에도 존재하죠.

MySQL의 경우, 151개로 상대적으로 넉넉한 편이지만,

별 다른 설정이 없는 경우 SQLAlchemy는 다음과 같은 설정을 가집니다.

```python
pool_size=5,       # 기본 커넥션 수
max_overflow=10,   # 추가로 생성할 수 있는 임시 커넥션 수
pool_timeout=30    # 사용할 수 있는 커넥션이 없을 때, 기다리는 시간(초)
```

```
# 세션을 닫지 않은 채로 계속해서 DB에 쿼리를 보내는 요청을 보내고 그 결과를 프린팅하고 있습니다.
Pool size: 5  Connections in pool: 3 Current Overflow: 10 Current Checked out connections: 12
INFO:     127.0.0.1:50423 - "GET / HTTP/1.1" 200 OK
Pool size: 5  Connections in pool: 2 Current Overflow: 10 Current Checked out connections: 13
INFO:     127.0.0.1:50423 - "GET / HTTP/1.1" 200 OK
Pool size: 5  Connections in pool: 1 Current Overflow: 10 Current Checked out connections: 14
INFO:     127.0.0.1:50423 - "GET / HTTP/1.1" 200 OK
Pool size: 5  Connections in pool: 0 Current Overflow: 10 Current Checked out connections: 15
```

5개의 요청이 빠르게 들어오면 서버 쪽에서는 기본 커넥션 풀의 크기를 채워버립니다.

또한 추가로 생성하는 임시 커넥션도 10개 밖에 안 되므로, 매우 빠르게 임시 풀도 차버립니다.

총 15개의 세션이 모두 차버린 채로 새 요청을 받게 되면, 30초간 세션을 기다립니다.

그리고 30초의 시간이 지날 때까지 세션을 가져오지 못할 경우

>sqlalchemy.exc.TimeoutError: QueuePool limit of size 5 overflow 10 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
{: .prompt-danger}

에러가 발생하는 것이죠.

당연하지만 커넥션을 닫지 않았기 때문에 연결된 DB에도 커넥션이 무의미하게 존재하고 있습니다.

### **반드시 with, finally를 통해서 close()를 시켜줍시다.**

방법은 여러가지가 있지만, FastAPI가 공식 Docs에서 권장하는 방법이 매우 좋습니다.

[FastAPI는 다음과 같은 연결 방식](https://fastapi.tiangolo.com/ko/tutorial/sql-databases/#main-fastapi-app)을 권장합니다.

```python
from sqlalchemy import create_engine, Integer
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DB_URL = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
engine = create_engine(url=DB_URL)
session_maker = sessionmaker(bind=engine, autoflush=False)

async def get_db():
    db = session_maker()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

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

세션을 요청마다 주입받아 사용하고, 요청이 끝날 경우 강제로 `close()`를 호출하는 것이죠.