---
layout: post
title: "[python] 컴프리헨션을 써야하는 이유"
date: 2024-10-31 04:15:18 +0900
categories: python python이론
tag: [python, 파이썬, SQLAlchemy]
---

# **컴프리헨션(Comprehension)?**

>**Python이 강력히 권고하는 복합 자료형(list, dict, set)의 생성 방식입니다.**
{: .prompt-info}

Python Docs에서는 함수형 프로그래밍 언어 `Haskell`에서 빌린 표기법이라고 합니다.(빌린..?)

간단하게, `0`부터 `1억-1`까지의 값을 순차적으로 넣은 리스트를 생성한다고 가정해봅시다.

```python
lst = []

for i in range(100_000_000): # 천의 단위마다 끊어서 보기 좋게 표현합니다.
    lst.append(i)
```

이러한 방식을 쓰는 것에도 딱히 문제는 없지만, 생각보다 비효율적입니다.

## **초기 배열을 append로 생성하는 것은 느리다**

Python의 `List`는 기본적으로 동적 배열입니다.

초기에는 일정한 메모리를 할당하고 값의 추가로 인해 해당 메모리의 한계를 초과하면,

보다 큰 새로운 메모리 공간을 할당하여 기존 값을 복사해 넣습니다.

즉, 0의 길이로 시작한 리스트에 값이 하나씩 추가되면

<u>할당된 메모리의 한계에 도달할 때마다, 새로운 메모리 공간을 할당하여 기존 값을 복사하는 과정이 일어납니다.</u>

이 한계의 확장과 메모리 이동은 당연히 **오버헤드**를 발생시킵니다.

또한, 컴프리헨션은 하나의 표현식이므로, 바이트코드로 변환될 때 보다 최적화되어 빠른 성능을 보여줍니다.

문자열에서 특정 문자를 찾을 때 `find` 메서드를 사용하는 것과

`for루프`와 `equals`를 통해 구현하는 것이 상당한 성능차이가 나는 것도 이와 같은 이유입니다.

<br>

## **컴프리헨션을 쓴다면?**

```python
lst = [i for i in range(100_000_000)]
```

결과적으로 같은 lst를 만들지만, 코드도 간단하고 훨씬 직관적입니다.

또한, <u>리스트를 초기화하는 과정에서 몇 개의 요소를 넣을지 미리 알 수 있기 때문에</u>

처음부터 해당 요소를 모두 넣을 수 있는 메모리를 할당합니다.

즉, **빈번한 메모리 확장(재할당) 및 복사가 이루어지지 않으므로**

append 방식보다 효율적이죠.

```python
import time

# append 방식

lst = []
start = time.time()

for i in range(100_000_000):
    lst.append(i)

end = time.time()
print(round(end-start,4)) # 2.860

# 컴프리헨서

start2 = time.time()

lst2 = [i for i in range(100_000_000)]

end2 = time.time()

print(round(end2-start2, 4)) # 1.282
```

보시다시비 시간이 약 45퍼센트 수준으로 단축된 걸 확인할 수 있습니다.

그러나 실제 백엔드 서버에서 이러한 코드를 짤 일은 별로 없죠...

혹시라도 있다 해도 그 때는 `Numpy/Pandas`가 압도적인 효율을 내줍니다.

기본 Python만 쓸 수 있는 코딩 테스트로 넘어가서,

0으로 초기화된 2차원 배열을 만들어 봅시다!

<br>

### 2차원 배열

```python
start3 = time.time()
lst3 = []

for _ in range(10_000):
    tmp_lst = []
    for _ in range(10_000):
        tmp_lst.append(0)
    lst3.append(tmp_lst)

end3 = time.time()

print(round(end3-start3, 4)) # 3.047


start4 = time.time()

lst4 = [[0 for _ in range(10_000)] for _ in range(10_000)]

end4 = time.time()

print(round(end4-start4, 4)) # 1.555
```

역시 **두 배 가까이 차이**가 나는 것을 알 수 있습니다.

온몸 비틀기라도 필요한 시점이라면, 꽤나 유용하게 쓸 수 있을 겁니다!

~~숏코딩에도 당연히 필요합니다~~

<br>

### **조건식이 달려도 여전합니다.**

```python
lst = []
start = time.time()

for i in range(100_000_000):
    if i//2 == 0:
        lst.append(i)
    
end = time.time()

print(round(end-start,4)) # 3.508


start2 = time.time()

lst2 = [i for i in range(100_000_000) if i//2 == 0]

end2 = time.time()

print(round(end2-start2, 4)) #2.645
```

물론, 이 경우에는 컴프리헨션도 최종 리스트의 길이를 알지 못하기 때문에, 메모리를 동적으로 늘려나가야 합니다.

다만 최대 길이는 알고 있으므로 보다 최적화된 동적 메모리 할당이 가능합니다.

그리고 표현식 자체가 여전히 최적화된 바이트코드로 변환 가능하므로, 빠릅니다.

**가능하고, 의도에 맞다면 컴프리헨션을 적극적으로 사용하는 걸 추천드립니다.**

<br>

## **다른 복합 자료형들도 가능합니다.**

```python
# dict
d = {i : 1 for i in range(100)}

# set
d = {s for s in range(100)}
```

혹시라도 `소괄호()`로 감싸면 튜플 컴프리헨션 아니냐? 하실 수 있겠으나, 이건

<br>

### **제네레이터 표현식**

입니다!

리스트 컴프리헨션과 상당히 다른 표현식입니다.

모든 객체를 생성해서 메모리에 로드하는 것이 아니라,

**객체에 접근하는 시점에 해당 인덱스의 표현식에 따라 값을 계산**하는 `지연 평가(lazy evaluation)`을 사용합니다.

즉, <u>제네레이터 자체는 메모리를 적게 사용하나, 값을 읽는 속도는 비교적 느립니다.</u>

코테 용도라면, 대부분의 경우 메모리보다 속도가 중요하므로(그리고 애초에 리스트에 표현식을 넣을 일이 없으므로)

리스트 컴프리헨션을 써야 합니다.

간단히 정리하자면 다음과 같습니다.

| **리스트 컴프리헨션** | **제너레이터 표현식** |
|---|---|
| []로 감싸서 작성됨 | ()로 감싸서 작성됨 |
| 모든 요소를 한 번에 메모리에 로드 | 요소를 필요할 때마다 하나씩 생성 |
|더 빠른 접근과 반복 작업 가능 | 메모리 사용이 적고 대용량 데이터 처리에 적합 |