---
layout: post
title: "[python] SQLAlchemy를 통한 DB session 연결"
date: 2024-01-29 17:15:18 +0900
categories: python python이론
tag: [python, 파이썬, SQLAlchemy]
---

# SQLAlchemy란

Java의 JPA와 같이, Python의 `ORM` 라이브러리다.

Django를 사용할 경우, 전용 ORM 모듈이 있으나,

FastAPI, Flask를 사용하거나 단순한 Python 실행 파일에서 DB와 연결이 필요할 경우

거의 무조건 쓰게 되는 라이브러리다.

애석하게도 Python backend는 한국에서는 비주류에 속하고,

그 작은 파이 안에서도 Django가 현재로써는 가장 큰 부분을 차지한다.

즉, SQLAlchemy는 한국어로 제작, 번역된 자료가 별로 없다...

공식 문서의 번역본 또한 당연히 없다...

최근 FastAPI로 백엔드를 구축하면서, 어려움과 의아함을 느낀 부분이 있어 포스팅하고자 한다.

<br>

## Session Maker와 Session 연결 방식

일반적으로 SQLAlchemy와 RDB의 연결은 다음과 같은 방식이다.

```python
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

DB_URL = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

engine = create_engine(url=DB_URL)

Session = sessionmaker(bind=engine)

app = FastAPI()

@app.get('/')
def hello():
    with Session() as db:
        ...
    return ...
```

`engine`객체에 DB의 연결 정보를 담아 객체를 만들고, `sessionmaker` 객체를 생성한다.

이는 DB 연결을 위한 `세션 팩토리`의 기능을 한다.

sessionmaker에 engine 정보를 config으로 담은 뒤, `call`하게 되면 세션이 연결된다.

여기서 주의할 내용은,

**Python 단에서 생성되고 사용을 마친 세션은 DB 상에서도 완전히 삭제되는 것이 아니다.**

`sleep` 상태로 `Timeout` 시간까지 쭉 유지된다. (MySQL의 경우 기본적으로 3600초로 설정)

만약 새로운 요청이 들어올 경우, sleep 상태의 연결을 꺠워 재사용한다.

해당 session의 미사용 시간이 Timeout 시간을 넘겨 버리면 DB에서 session을 완전히 삭제해버린다.

SQLAlchemy가 사용할 수 있는 세션이 없음을 인지하고 있는 경우, 새 세션을 만들지만

DB에서 timeout으로 세션을 닫아버리면 SQLAlchemy는 **새로운 요청을 보내기 전까진 세션이 닫혔는지 알 수 없다.**

SQLAlchemy 입장에서는 '어 원래 다니던 길이 없어졌네' 하면서 주저 앉아버려 `500에러(DB는 10054)`를 반환한다.

<br>

## 반드시 사용을 마친 뒤 닫아주자.

FastAPI에서는 자체적으로 `try`, `finally`를 활용한 DB 세션 연결 방법을 [안내해주고 있다.](https://fastapi.tiangolo.com/ko/tutorial/sql-databases/#main-fastapi-app)

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