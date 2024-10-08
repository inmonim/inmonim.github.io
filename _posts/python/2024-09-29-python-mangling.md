---
layout: post
title: "[python] 파이썬은 접근 제어자가 없다? - 맹글링"
date: 2024-09-29 10:15:18 +0900
categories: python python이론
tag: [python, 파이썬, 객체지향]
---

# **Python은 접근 제어자가 없다.**

애석하게도, 파이썬으로 작성한 코드는 어디서든 접근할 수 있습니다.

숨기는 것과 "__이 요소에는 접근하지 마시오__" 라고 명시하는 것은 가능하지만, 여전히 접근은 가능합니다.

Java에서 `public`, `private` 등의 접근 제어자를 활용해 요소 마다 접근 가능 범위를 수 있는 것과는 대비되죠.

그럼에도, 숨기기 정도와 접근하지 마라고 일러주는 것까지는 가능합니다.

## **언더 스코어를 통한 접근 제어 표기**

Python에서 클래스 내부 요소를 숨기기 위해서 보통 언더 스코어(언더바, `_`)를 활용합니다.

이를 활용한 네이밍 컨벤션은 클래스 내부 값 뿐만 아닌 함수와 내부 클래스에도 적용이 가능합니다.

변수, 함수, 클래스 모두 1급 객체이므로 취급이 같기 때문이죠.

### **_ 한 개로 시작하는 요소**

>클래스 내부와 해당 클래스를 상속받은 클래스의 내부 요소로만 사용하기를 권고
{: .prompt-warning}

어떠한 강제도 없고, 코드 상 제약도 없는 그저 권고의 의미일 뿐이다.

Java와 비교하자면, `protected` 접근 제어와 유사한 범위를 의미한다고 볼 수 있다.

### **__ 두 개로 시작하는 요소 (mangling)**

>클래스 내부에서만 사용하기를 어느정도 강제
{: .prompt-danger}

Java의 `private` 접근 제어자와 동일한 범위를 뜻합니다.

이 경우, 런타임 단계에서 name mangling이 되어 **직접 접근을 막아줍니다**.

이를 통해 상곡 관계에서 이름의 충돌을 막아주는 역할도 합니다.

```python
class Spam:

    def __init__(self):
        self.x = 1
        self._y = 2
        self.__z = 3

spam = Spam()

spam.x     # 1
spam._y    # 2 / 강제성이 없다.
spam.__z   # AttributeError: type object 'Spam' has no attribute '__z'
```

이렇듯, `_y`에는 문제없이 접근 가능하지만, `__z`는 직접적인 접근 자체가 막힙니다.

다만, IDE를 사용하거나 내부 코드를 뜯어 요소를 확인할 수 있고, 이를 알면 **우회적으로 접근**할 수 있습니다.

```python
class Spam:

    def __init__(self):
        self.x = 1
        self._y = 2
        self.__z = 3

spam = Spam()

spam._Spam__z  # 에러가 발생하지 않는다.
```

`class`.`_class``접근할 요소` 와 같은 식으로 만들면 외부에서도 접근할 수는 있습니다.

물론, 코드 설계자의 의도에 완전히 반하는 행동인만큼, **쓰지 맙시다!**

### **그럼 __class__ 이건 뭐예용?**

>매직 메서드입니다.
{: .prompt-info}

클래스 내부에서 자동으로 생성되어 일반적으로는 `__init__`과 `__repr__` 말고는 잘 쓸 일이 없습니다.

일반적이지 않은 특수한 동작을 원할 경우 이를 오버라이드하여 만들 수 있습니다.

예를 들어 인스턴스의 대표명을 출력하고 싶은 경우,

클래스 내부에 `__repr__` 메서드를 생성(사실상 오버라이드)하여 내 맘대로 바꿀 수 있죠.

```python
class Spam:
    
    def __repr__(self):
        return "언제부터 내가 스팸일 거라고 생각했지?"
    
spam = Spam()
print(spam)  # 언제부터 내가 스팸일 거라고 생각했지?
```

따라서, 앞뒤로 언더스코어 2개가 오는 경우는 접근 제어의 의미는 아닙니다.

**물론 둘 다 멋대로 가져다 쓰다가 낭패보기 쉽다는 건 같으니, 잘 알아보고 써야합니다!**