---
layout: post
title: "C언어는 Computer 언어가 아님."
date: 2024-09-22 16:44:18 +0900
categories: C trivia
tag: [python, python-version, 파이썬]
---

# C != Computer Language

> Computer 언어라서 C 언어 아님?
{. :prompt-info}

보통 프로그래밍을 배운 적 없는 사람들(또는 이런 잡다한 것에 관심없는 사람들)은 흔히 위와 같이 생각합니다.

학위라곤 문학사 학위 밖에 없는 저 또한 처음엔 그렇게 생각했습니다.

그리고 이건 정말 프로그래밍을 꽤 배운 사람들도 모르는 경우가 많은데,

### C언어는 최초의 고급 프로그래밍 언어 또한 아닙니다.

고급 언어는 저급 언어(사실 상 기계어와 어셈블리 둘 뿐)를 추상화하여 쓰고 읽기 쉽게 만든 언어입니다.

C언어는 1972년 발표되었고, 이보다 15년도 전에 사실상 최초의 고급 언어라고 불리는 Fortran이 발표되었습니다.

엄밀히 말하자면 Fortran 이전에도 개념이 제시되고 실제로 구현된 고급 언어가 있었지만, 통상적으론 Fortran이 최초의 고급 언어로 인정받고 있습니다.

최초의 고급 언어와 15년이란 간극이 있는만큼,

C언어 이전에도 많은 고급 언어가 있었음에도 사람들은 어째서 C를 최초의 고급 언어라고 무의식 중에 생각하게 되는 것일까요?

## C언어는 중급 언어?

최초의 고급 언어라고 무의식 중에 생각하는 것과 더불어,

C언어에 대해서 어떤 사람들은 저급 언어, 고급 언어도 아닌 중급 언어다! 라고 주장하기도 합니다.

일반적으로 저급 언어는 하드웨어를 직접적으로, 즉 메모리와 레지스터를 직접적으로 제어할 수 있는 언어를 의미합니다.

이 경우 하드웨어의 종류나 사용하는 아키텍쳐에 따라 문법이 달라지며, 프로그래머는 그에 맞춰 코드를 작성해야 합니다.

그에 반해 고급 언어는 저급 언어를 추상화하여, 코드를 작성할 때는 하드웨어에 종속되지 않고 해당 언어의 문법에만 맞춰 작성하면 됩니다.

하드웨어와 아키텍쳐에 따라 자동으로 알맞은 저급 언어로 번역되어 작동하기 때문이죠.

그렇다면, C는 어째서 중급 언어라고 불리는 걸까요?

### Unix 개발을 위한 초석

C언어는 현대적인 프로그래밍 언어 분류 상으론 고급 언어가 맞습니다.

다만 제작 목적성 자체가 상당히 독특하기 때문에 중급 언어라는 요상한 포지션을 가질 수 있었던 겁니다.

바로 C언어가 Unix의 커널 설계를 위해 만들어진 언어이기 때문이죠.

대부분의 언어는 특정 도메인의 문제 해결이나 프로그래밍 생산성 향상 또는 개발자가 심심해서(?) 만들어지는 경우가 많습니다.

따라서 그러한 고급 언어들은 제작 목적이나 방향성 부터가 하드웨어에 직접 접근해 메모리를 할당, 해제하는 작업에 맞춰져있지 않습니다.

가비지 컬렉션이 매우 강력한 Java와 Python 등 현대적인 프로그래밍 언어는 메모리를 코드 수준에서 직접 관리하는 일이 거의 없고,

그러한 언어들은 보통 일반 컴퓨터 사용자(비 개발자)를 위한 웹, 응용 프로그램 제작에 사용됩니다.

그에 반해 C는 Unix의 커널 설계를 위해 만들어진 만큼, 하드웨어를 직접적으로 조작하는 것을 염두로 만들어졌습니다.

그렇기에 언어 개발의 목적성 자체가 여타 고급 언어보단 저급 언어와 어셈블리어에 조금 더 밀접한 것입니다.

## C의 설계와 개발

Unix는 1960년대, 켄 톰슨과 데니스 리치, 브라이언 커니핸 등, 전설적인 프로그래머들이 벨 연구소에서 개발하고 있었습니다.

초창기에는 어셈블리어로 모든 개발이 이루어지고 있었으나,

앞서 언급했듯 어셈블리어는 하드웨어마다 아키텍쳐가 달랐기에 유지보수와 이식에 있어 대단히 큰 한계가 존재했습니다.

이에 대한 대안으로 BCPL(Basic Combined Programming Language)를 사용했는데,

켄 톰슨(Ken Thompson)은 BCPL을 필수 기능만 남겨 경량화시킨 B언어를 만들었습니다.

그리고 나서 더욱 본격적으로 Unix를 개발하던 1970년대 초, B언어가 가진 자료 구조의 한계 때문에 다시 새로운 언어를 만들고자 합니다.

그리하여 C언어의 설계가 시작되었고, 이는 전설적인 프로그래머, 데니스 리치(Dennis Ritchie)의 주도 하에 이루어졌습니다.

### 그래서 중급 언어?

즉, 제작 목적 자체가 Unix 커널 설계였기 때문에, 목적성만 따지면 저급 언어에 가까운 언어입니다.

C언어의 차시자 데니스 리치와 Unix 커널 설계자 브라이언 커니핸의 전설적인 C언어 교범 The C Programming Language<sup>[1)](#ref1)</sup>에서는 서문에서 다음과 같이 말하고 있습니다.

>C is a relatively "low level" language. This characterization is not pejorative; it simply means that C deals with the same sort of objects that most computers do, namely characters, numbers, and addresses. ......... Again, because the language reflects the capabilities of current computers, C programs tend to be efficient enough that there is no compulsion to write assembly language instead. ......... Although C matches the capabilities of many computers, it is independent of any particular machine architecture, and so with a little care it is easy to write "portable" programs...

요컨대, 저수준 언어에 가까우며 이식성있는 어셈블리어를 목표로 설계된 언어라는 것입니다.

현대적인 프로그래밍 언어의 분류로는 C는 분명 고급 언어가 맞지만, 저급 언어의 한 단계 위에서 작동하는 조금 추상화된 저급 언어라는 목적으로 개발되었기 때문에 중급 언어라는 묘한 포지션에 위치하는 것이죠.

### C언어 이름의 유래

B 언어의 후속작이므로, 알파벳 순서 상에 따라 C언어가 되었습니다.(열린 결말이지만 이게 가장 유력합니다.)

프로그래머들이 가장 어려워하는 작업이 변수명 짓기인 것처럼, 과거의 천재 개발자들도 이름을 짓는 건 여간 어려운 게 아니었나봅니다.

~~아니면 그냥 공돌이답게 네이밍 센스가 바닥이던가~~

이에 대한 레퍼런스는 c언어의 탄생에 대해 데니스 리치가 직접 설명한 논문

[The Development of the C Language](https://www.bell-labs.com/usr/dmr/www/chist.html)<sup>[2)](#ref2)</sup>에서 확인할 수 있습니다.

> I decided to follow the single-letter style and called it C, leaving open the question whether the name represented a progression through the alphabet or through the letters in BCPL. <br><br> 저는 단일 문자를 사용하는 스타일을 따르기로 결정했고, 그 이름을 C라고 지었습니다. 이 이름이 알파벳의 순서를 따른 것인지, 아니면 BCPL의 문자에서 따온 것인지는 열어둔 상태로 남겼습니다.


## 전설이 된 이유

그렇다면 어째서 Computer 언어를 줄여서 C언어인 것이라고 생각할 만큼 프로그래밍 언어의 대명사가 된 것일까요?

Unix는 Linux, MacOS와 같은 컴퓨터용 OS는 물론, Android, Ios같은 스마트폰의 OS의 모태이기도 합니다.

이러한 운영체제의 커널 역시 C언어와 C를 모태로 발전한 언어들이 사용되고 있습니다.

Windows 또한 Unix를 계승한 것은 아니지만 커널을 조작하는 데에 C언어를 사용하기 때문에, Unix를 넘어서도 C언어가 사용되고 있는 것이죠.

즉, C는 프로그래밍 역사에서 가장 중요하며, 큰 파급력을 가진 언어 중 하나입니다.

그리고 시스템 소프트웨어 설계라는 목적성과 달리, 응용 프로그램 설계에도 충분히 활용할 수 있는 전천후 언어입니다.

프로그래밍을 처음 접하는 사람들에게 처음으로 배워야 할 언어로 C언어를 꼽으며, 대부분의 컴퓨터공학과에서도 1학년 1학기에 무조건 배우는 편이라고 하니,(이걸 처음부터 배웠다면 전 아마 개발을 관뒀을 겁니다) 개발을 잘 모르는 사람들게에도 인지도가 높을 수 밖에 없던 것이죠.

---

## Ref)

1. <a id="ref1"></a>Kernighan, Brian W., and Dennis M. Ritchie. The C Programming Language. 1978.

2. <a id="ref2"></a>Ritchie, Dennis M. “The Development of the C Language.” Bell Labs, 1993, https://www.bell-labs.com/usr/dmr/www/chist.html.