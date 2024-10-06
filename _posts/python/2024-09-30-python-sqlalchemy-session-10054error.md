---
layout: post
title: "[python] SQLAlchemy - 10054 Error & 2006 Error"
date: 2024-09-30 06:15:18 +0900
categories: python python이론
tag: [python, 파이썬, SQLAlchemy]
---

# **SQLAlchemy + MySQL 10054 Error & MySQL 2006 Error**

>Lost connection to MySQL system error: 10054 An existing connection was forcibly closed by the remote host
{: .prompt-danger}

>Error Code: 2006 - MySQL server has gone away
{: .prompt-danger}

SQLAlchemy와 FastAPI 또는 Flask를 활용하여 백엔드 서버를 구축할 때, 어쩌면 한 번쯤은 만났을 수도 있는 에러입니다.

**문제는 어쩌다가 딱 한 번 발생하고, 한 번 발생한 후에는 문제없이 서버가 동작한다는 것입니다.**

에러 자체는 여러 환경에서 발생할 수 있지만, `SQLAlchemy`를 사용한다면 하나의 대표적인 원인을 꼽을 수 있습니다.

**DB에서는 폐기한 Connection을 SQLAlchemy(server)에서 사용하려 했기 때문입니다.**

## **Connection Pooling**

SQLAlchemy는 DB와의 통신을 위해 `Connection Pooling` 방식을 사용합니다.

`Connection`은 DB와 Server가 각각 연결한 대상에 대한 정보입니다.

이러한 Connection은 생성 시에 연결, 인증, 권한확인 등, 여러 절차를 거쳐야 하기에 오버헤드가 큰 작업입니다.

모든 query마다 Connection의 생성/삭제를 거칠 경우 안 그래도 심한 병목현상이 심해지겠죠.

이를 위해, 변경 사항이 없을 경우 일종의 캐시처럼 **한번 연결된 Connection을 재사용**합니다.

그리고 SQLAlchemy 또한 이러한 Connection을 생성한 뒤 Pool에 넣어두고,

요청마다 Pool에 존재하는 Connection을 가져와 사용하는 것입니다.

요청이 정상적으로 수행되고 session을 close()하면 Connection은 다시 Pool로 반환됩니다.

마치 프로세스가 CPU를 점유하는 것처럼, session은 Connection을 점유하는 것입니다.

여기서, 두 가지 대표적인 문제가 발생합니다.

**1. close()를 수행하지 않아, session이 connection을 반환하지 못하고 계속 점유하는 경우**

**2. sqlalchemy와 DB의 connection 유지 기간이 달라 통신 에러가 발생하는 경우.**

이번 포스팅에서는 `2번 문제`를 다루도록 하겠습니다.

**## Connection의 유지 기간**

먼저, SQLAlchemy의 Connection의 특징을 짚고 넘어가겠습니다.

1. 풀에 사용할 수 있는 커넥션이 없을 경우, db에 커넥션 생성 요청을 보내고 정상적으로 생성이 된 경우 이 커넥션 정보를 풀에 넣는다. 

2. 사용할 수 있는(비어있는, 점유 가능한) 커넥션이 있을 경우, 이를 활용해 db에 접근한다. 

3. 커넥션은 별도의 설정이 없는 경우 영구히 유지된다.

**4. SQLAlchemy(Python)과 DB는 서로의 상태를 모른다.**

3번과 4번 때문에 문제가 발생합니다.

MySQL(MariaDB)의 Connection 타임 아웃은 `8시간(28800초)`입니다.

다만, 타임 아웃 전에 한 번이라도 사용될 경우 타임 아웃이 초기화됩니다.

그런데 SQLAlchemy의 경우, 별도의 설정이 없으면 Connection은 영구히 유지됩니다.

**즉, DB와 연결된 서버를 8시간 이상 열어놓지만 요청이 없어, DB측 커넥션이 타임아웃 된 경우에 문제가 발생합니다.**

DB는 이미 폐기한 Connection을 SQLAlchemy가 사용했기 때문에

>Lost connection to MySQL system error: 10054 An existing connection was forcibly closed by the remote host
{: .prompt-warning}

이렇게 원격 연결을 DB측에서 닫아버린 것이죠.

10054에러를 반환 받았으니 SQLAlchemy도 Connection을 Pool에서 제거합니다.

그러나 **이러한 문제가 발생했음에도 SQLAlchemy는 다시 요청을 보내지 않습니다.**

다음 요청에서는 커넥션 풀을 새로 생성해서 통신하기 때문에 문제가 발생하지 않는 것이죠.

이제 문제를 파악했으니 해결해봅시다.

## 해결 방법

해결 방법은 여러 가지가 있습니다.

먼저 **SQLAlchemy 단에서 해결**하는 방법입니다.

### 1. pool_pre_ping

```python
engine = create_engine("mysql+pymysql://user:pw@host/db", pool_pre_ping=True)
```

**모든 요청마다 먼저 "Select 1"과 같은 쿼리를 던져 Connection 상태를 확인**

그야말로 돌다리도 두들겨보고 건넌다는 느낌입니다.

아무리 가벼운 쿼리여도 쿼리를 보내는 수 자체가 많아지면 오버헤드가 될 수 있다는 단점이 있습니다.

### **2. pool_recycle**

```python
engine = create_engine("mysql+pymysql://user:pw@host/db", pool_recycle=3600)
```

**Connection에 타임 아웃을 설정해 자동으로 새 Connection을 생성**

커넥션이 생성된 뒤, 요청 없이 3600초(1시간)이 지나면 타임아웃시키고 새 커넥션을 생성합니다.

이를 통해 커넥션이 오랜 기간 대기하며 발생하는 문제를 줄일 수 있습니다.

이 방법이 가장 좋은 방법이라 생각합니다.

**### 3. 크론잡/배치를 활용한 강제 갱신**

DB의 Connection timeout이 일어나기 전, 크론잡 등을 활용해 자동으로 쿼리를 던져 커넥션을 갱신하는 방식입니다.

1번 방법과 2번 방법을 적절히 섞은 방법이긴 한데, 굳이?인 방법입니다.

개인적으로는 2번 방법을 선호하는 편입니다.

### 1. wait_timeout 설정

```sql
SHOW VARIABLES LIKE 'wait_timeout';
```

MySQL(MariaDB)에서는 위의 명령어를 통해 타임아웃을 확인할 수 있습니다.

당연히 재설정도 가능하니, 이 시간을 보다 길게 잡아 커넥션의 유지 시간 자체를 늘리는 것도 방법입니다만,

그다지 좋은 방법은 아닌 것 같습니다...