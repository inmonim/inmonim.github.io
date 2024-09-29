---
layout: post
title: "[python] Class 속성과 객체 속성"
date: 2024-06-17 15:15:18 +0900
categories: python python이론
tag: [python, 파이썬, 객체지향]
---

# Python의 class의 속성과 객체의 속성은 별개다.

<br>

## 선요약

class의 `__init__` 즉, 생성자에서 할당하는 것이 아닌,

class 자체에 선언된 속성은 `instance.attribute`가 아니라 `intance.__class__.attribute`에 존재한다.

다만 `instance.attribute`에 무언가를 할당한 상태가 아니라면, `instance.attribute`를 통해 접근이 가능하다.

**class로 생성할 객체마다 변하기 쉬운 기본 속성을 주고 싶다면, 클래스 속성이 아닌 인스턴스 생성자에 기본값을 설정하자.**

<br>

## class 하나를 만들어보자.

```python
class Cat:
    race = 'Domestic Shot hair'

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def change_race(self, race):
        self.race = race
```

클래스의 기본 속성으로 도메스틱 숏 헤어라는 종 분류가 들어간다.

생성자에서 이름과 나이를 설정할 수 있으며,

메서드를 통해 `race`를 `변경 할 수 있는 것`처럼 만들어놨다.

**위와 같은 코드는 만들면 안 된다**

<br>

### change_race 메서드는 과연 어떻게 동작할까?

```python
bonk_cat = Cat('bonk', 2)
ha_cat = Cat('ha', 3)

bonk_cat.change_race('american shot hair')
```

과연 위의 코드는 어떤 동작을 의미할까?

1. Cat 클래스의 클래스 속성인 race 값이 변하여, ha_cat의 race도 바뀌었다.

2. bonk_cat 객체(인스턴스)의 race 값만 변한다. ha_cat은 그대로다.

3. 둘 다 아니다.

정답은 `3번`이다.

겉으로 드러나는 부분만 보면 `2번`이 될 수도 있지만, 파고 들면 아예 다르다.

<br>

### class 속성은 모든 인스턴스가 공유한다.

매우 중요한 개념이다. class의 속성은 class의 인스턴스 **전체**가 공유하는 변수다.

```python
# 위의 코드에서 이어진다.

print(bonk_cat.race)
print(ha_cat.race)

# ======
american shot hair
domestic shot hair
```

보다시피 Cat 클래스의 두 객체의 race는 다르다.

Python의 class에 대해 잘 안다면 이것이 잘못되었다는 걸 알 수 있다.

**Python의 클래스 속성은 해당되는 모든 객체가 똑같이 가져야 한다.**

**단순히 값이 같은 수준`(==)`이 아닌, 하나의 메모리를 공유하는 하나의 객체`(is)`가 되어야 한다.**

<br>

### 어째서 같은 클래스인데 클래스 속성이 다른가?

chage_race 메서드는 race 값을 바꾼 것이 아닌, 새로운 스페이스에 값을 생성한 것이기 때문이다.

클래스 속성과 객체 속성은 다른 스페이스에 선언되어 있다.

클래스 속성에 보다 명시적으로 접근하기 위해서는, `class.__class__.attribute`로 접근해야 한다.

**같은 변수명으로 객체 속성을 선언하지 않는 이상**, `class.attribute`는 `class.__class__.attribute`를 불러온다.

코드로 설명하면 다음과 같다.

```python
bonk_cat = Cat('bonk', 2)
ha_cat = Cat('ha', 3)

print(bonk_cat.race is bonk_cat.__class__.race) # True
print(bonk_cat.race is ha_cat.race) # True
print(bonk_cat.__class__.race is ha_cat.__class__.race) # True

bonk_cat.change_race('american shot hair')

print(bonk_cat.race is bonk_cat.__class__.race) # False
print(bonk_cat.race) # american shot hair
print(bonk_cat.__class__.race) # domestic shot hair
print(ha_cat.race) # domestic shot hair

print(bonk_cat.__class__.race is ha_cat.__class__.race) # True
```

bonk_cat의 change_race 메서드로 같은 변수명을 공유하는 객체 속성을 생성한 뒤에는, 객체 속성을 먼저 호출하게 바뀐다.

이 때문에 클래스 속성과 객체 속성을 혼동하는 경우가 잦은 것 같다.

이러한 클래스 코드를 짜는 이유는, 클래스로 생성할 객체의 기본 속성을 주고자 하는 마음 때문인 것 같다.

실제로 필자도 클래스를 처음 배울 때는 이러한 개념이 없어 자주 헷갈리는 부분이었다.

클래스 속성은 모든 인스턴스가 공유해야만 하는 값, 하나가 바뀌면 모든 값이 바뀌는 값이 들어가야 한다.

Cat 클래스를 예로 든다면, 모든 고양이 객체가 변함 없이 공유하는 `평균 수명`, `학명` 정도가 되겠다.

(물론 세부 품종마다 다를 수는 있으니, 단순 예시다.)

위의 클래스를 조금 더 올바르게 수정한다면 다음과 같겠다.

```python
class Cat:
    avg_life_span = 15
    scientific_name = 'Felis catus'

    def __init__(self, name, age, race = 'Domestic Shot hair'):
        self.name = name
        self.age = age
        self.race = race

    def change_race(self, race):
        self.race = race
```

클래스의 속성은 객체 전체가 공유하는 값으로 바꾸고,

race(품종)의 경우, 기본값은 Domestic shot hair로 하되, 클래스 생성 시 값이 들어올 경우 해당 값으로 할당한다.

<br>

### 그렇다면 클래스 속성은 어떻게 바꾸지?

`@classmethod` 데코레이터를 활용하여 클래스 속성을 다룰 수 있는 메서드를 만들어야 한다.

```python
class Cat:
    avg_life_span = 15
    scientific_name = 'Felis catus'

    def __init__(self, name, age, race = 'Domestic Shot hair'):
        self.name = name
        self.age = age
        self.race = race

    @classmethod
    def change_avg_life_span(cls, new_value):
        cls.avg_life_span = new_value
```

classmethod로 선언된 메서드의 경우, 인스턴스를 나타내는 self 대신 클래스를 나타내는 cls가 첫 번째 인자로 들어간다.

이 방법으로는 `class.__class__` 내에 존재하는 클래스 속성을 바꿀 수 있는 것이다.

<br>

### 그럼 이것도 되는 거 아니냐?

```python
bonk_cat.__class__.avg_life_span = 50
```

![bonk_cat](/jjal/bonkcat.jpg)

코드의 일관성과 가독성을 심히 망치고, Python의 의도를 완전히 비켜나가는 방법이다.

setter를 만들어 쓰자.