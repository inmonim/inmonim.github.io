<!-- ---
layout: post
title: "[python] SQLAlchemy를 통한 DB session 연결"
date: 2024-04-30 17:15:18 +0900
categories: python python이론
tag: [python, 파이썬, SQLAlchemy]
--- -->

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

## Session Maker와 Session 연결 방식

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

@app.get('/')
async def hello(db = Depends(get_db)):
    
    item = db.query(Item).get(1)
    return ...
```

DB연결 정보를 담은 `engine`을 바탕으로 `session_maker`객체를 생성합니다.

`session_maker` 객체는 펑션 콜이 발생할 시, 새로운 세션(db)를 반환합니다.

FastAPI의 DI용 함수인 Depends를 통해 get_db 함수 자체를 객체로써 파라미터에 넣으면

해당 요청 내에서 db와 연결된 세션을 얻는 것이죠.

`Depends(get_db)`같은 의존성 주입 방식이 아닌 다른 방식을 쓸 수도 있습니다.

함수 내에서 session_maker의 펑션 콜을 직접 시행해도 괜찮습니다.

다만, 이 경우 다음과 같이 반드시 처리해줘야 합니다.

```python
with session_maker() as db:
    db.query(Item).get(n)
# with 블럭 밖에서도 db 객체 사용이 가능하지만, 하면 안 됩니다!
```

위와 같이 with 블럭을 사용하여 세션(db)의 생명 주기를 관리해주거나

```python
db = session_maker()

item = db.query(Item).get(1)

db.close()
```

이처럼 세션 사용이 끝난 후에 반드시 `.close()`로 세션을 마쳐줘야 합니다.

### session은 뭐지?

SQLAlchemy는 커넥션 풀링 방식으로 DB와 소통합니다.

python에서 정상적으로 세션 사용을 마친 경우(`db.close()` 또는 `with`문)에

python은 이 때 열어둔 세션을 `sleep`으로 두고, 다음 요청이 들어왔을 때 다시 사용하려 한다.

DB에서는 해당 세션을 `sleep` 상태로 둔 뒤 `Timeout` 시간까지 쭉 유지된다. (MySQL의 경우 기본적으로 3600초로 설정)

둘 다 세션을 완전히 삭제하지 않고 비활성 상태로 두는 것이다.

새로운 요청이 들어올 경우, python과 db 모두 `sleep` 상태의 연결을 깨워 재사용한다.

해당 session의 미사용 시간이 Timeout 시간을 넘겨 버리면 DB에서 session을 완전히 삭제해버린다.

문제는 여기서 발생한다.

SQLAlchemy가 사용할 수 있는 세션이 없음을 인지하고 있는 경우, 새 세션을 만들지만

**DB에서 timeout으로 세션을 닫아버리면 SQLAlchemy는 새로운 요청을 보내기 전까진 세션이 닫혔는지 알 수 없다.**

SQLAlchemy 입장에서는 '어 원래 다니던 길이 없어졌네' 하면서 주저 앉아버려 `DB는 10054에러`를 반환한다.

<br>

## 반드시 사용을 마친 뒤 닫아주자.



`with` 문을 쓰거나, `close()`를 통해 명시적으로 닫아주자.

그렇지 않으면 실제 이전에 생성한 session은 sleep 상태이지만,

SQLAlchemy는 해당 세션을 '사용 중'으로 파악하여, 새로운 세션을 만들게 된다.

그렇게 sleep 상태의 세션이 쌓이면서 DB에도 부하와 에러를 야기하고,

SQLAlchemy 또한 관리 가능한 세션 수를 초과한다고 생각하여(실제로 쓰이는 세션은 전혀 없는데도)

서버를 멈춰버리게 만드는 수가 있다.

<br>

## TimeOut의 해결방법

세션이 주기적으로 사용되면 timeout까지의 시간이 계속 초기화 되어 문제가 발생할 확률이 줄어들긴 한다.

또한 에러가 timeout으로 인한 에러가 발생해도,

한 번 더 요청을 날리면 새로운 세션이 생성되어 곧장 사용할 수 있다.

그럼에도 그 한 번의 에러는 분명 무시 못하는 버그다.

```python
engine = create_engine("mysql+pymysql://user:pw@host/db", pool_pre_ping=True)
```

`pool_pre_ping`은, 세션에 접근하기 전에, 세션 쪽으로 미리 돌을 던져본다 생각하면 되겠다.

`SELECT 1` 같은 매우 간단한 SQL을 통해 세션의 유지 여부를 파악하는 것이다.

다만, 이 방법은 정말 모든 요청마다 돌을 던져대는 것이니, **살짝이어도 오버헤드가 발생한다.**

```python
engine = create_engine("mysql+pymysql://user:pw@host/db", pool_recycle=3600)
```

이 방법은 3600초마다 session의 연결을 **의도적으로 끊어버린다.**

SQLAlchemy가 끊는 것이므로, 당연히

'다니던 길이 없어졌다!' 가 아니라 '길을 다 엎었댔으니 다시 깔자'가 되어

에러가 발생하지 않고 새로운 세션을 연결할 수 있도록 한다.