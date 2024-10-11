---
layout: post
title: "Python은 근본 웃음벨이다"
date: 2024-10-10 16:44:18 +0900
categories: programming_trivia
tag: [python, 파이썬]
---

![python-semi-colon](python_semicolon.jpg){: width="350px"}
_세미콜론없다고ㅋㅋㅋㅋㅋㅋ_

프로그래밍의 역사에서 가끔 천재들이 심심해서 나온 것들이 있습니다.

![tovals_f](torvalds_f.webp){: width="350px"}
_Nvidia를 향해 엿을 날리는 리누스 토발즈_

이 아저씨가 만든 `linux`와 `Git`이나 오늘 이야기할

# 근본 웃음벨 Python 입니다.

![monty_python](monty_python.jpeg){: width="350px"}
_진짜 파이썬 맞습니다_

Python은 현재 2018년 은퇴를 번복하고 MS에서 Python 개발을 맡고 있는 귀도 반 로섬에 의해 창시되었습니다.

![guido](guido.jpeg){: width="350px"}
_귀도 반 로섬(Guido van rossum, 1956~, 네덜란드)_

대학시절부터 엘리트였던 귀도는 암스테르담 대학교에서 수학과 컴퓨터 과학을 공부하였으며

졸업 후, 네덜란드 국립수학정보학연구소(`CWI`, Centrum Wiskunde & Informatica)에서 근무했습니다.

**귀도는 1989년 크리스마스 휴가를 보내던 중, 심심해서 Python을 만들기 시작했습니다.**

2년 후인 1991년, `Python 1.0`이 탄생했습니다.

![python-hatchling](python-hatchling.jpeg){: width="350px"}
_파이썬이 탄생하는 역사적 광경입니다_

취미로 만든 언어다보니, 언어 자체에 많은 유머가 함축되어 있습니다.

그 중 가장 대표적인 건 `Python`이란 이름 그 자체입니다.

Python의 로고는 비단뱀(학명: Pythonidae, 영명 : Python)을 형상화해서 만들었습니다.

![quido](python_python.jpeg){: width="350px"}
_근데 얘가 비단뱀이 맞긴 한가?_

대체 왜 프로그래밍 언어가 뱀으로부터 시작했지? 싶지만, 개발자가 이름 대충 짓는 건 예삿일이니 그런갑다 하겠죠.

물론 여느 프로그래밍 관련 이름들이 그렇듯, 비단뱀은 후에 짜맞춘 것일 뿐입니다.

진짜 이름의 유래는

![quido](monty_python2.jpg){: width="350px"}

영국의 6인조 코미디 그룹 몬티 파이선(발음 상 파에톤, 파이튼 등으로도 불립니다)으로부터 유래했습니다.

유명한 작품으로는 전설적인 코미디 영화 몬티 파이선의 성배가 있습니다.

![quido](holy_grail.jpg){: width="350px"}
_진짜 50년 지난 지금 봐도 꿀잼입니다_

즉, Python이라는 작명부터가 근본 웃음벨인 것이죠.

그렇기에 python 커뮤니티나 근-본을 따르는 예제에서는 몬티 파이선의 스케치에서 등장하는 소재들이 자주 등장합니다.

여타 대부분의 언어나 커뮤니티, 예제에서 foo, bar가 쓰이는 것과는 대조되게

spam, egg, Knights who say Ni(니라고 말하는 기사) 등이 쓰이는 것을 자주 볼 수 있습니다.

_(사실 foo, bar도 고치지 못할 정도로 망했다는 뜻인 FUBAR(F**ked Up Beyond All Recognition)에서 유래했다는 설이 있긴 합니다...)_

## 왜 만들어졌을까?

사실 심심해서는 조금 과장된 얘기고 CWI에서 근무하던 시절, `ABC` 언어 프로젝트에 참여하며 확장성과 실용성에서 부족함을 느꼈다고 합니다.

이를 보완함과 동시에, 보다 쉽고 재미있는 프로그래밍 경험을 줄 수 있는 스크립트 언어를 개발하고자 마음먹은 것이죠.

당시에는 비슷한 목적을 가지고 개발된 `Perl`도 있었지만,

두 언어의 설계 철학을 보면 아무래도 귀도는 Perl의 방식이 그다지 맘에 들진 않았던 모양입니다.

### 진주 vs 비단뱀

한국은 물론이고 전 세계적으로도 사실상 Python이 압도적으로 많이 쓰이고 있으나,

둘 다 이것저것 다 할 수 있는 만능 스크립트 언어라는 점에서 항상 논쟁의 주제가 되곤 합니다.

앞서 귀도는 perl의 방식이 맘에 들지 않았다고 했었는데, 두 언어의 설계 철학을 먼저 봐야 합니다.

펄의 철학은 다음과 같습니다.

>어떠한 일에는 여러 가지 방법이 존재한다.<br> There is more than one way to do it.

그에 반해 파이썬은 다음과 같은 원칙을 중요하게 생각합니다.

>명확한, 그리고 가급적이면 유일하면서 명백한 방법이 있을 것이다.<br> There should be one-- and preferably only one --obvious way to do it.

여기서 "유일하면서 명백한" 방법이란, 무조건적인 하나의 답이 있으며 그 외에는 오답이다라는 의미는 아닙니다.

**개발자의 의도가 분명하게 드러나며 파이썬 코드 컨벤션에 맞는(당연히 비효율적이지도 않은) 코드를 지향하라는 의미**입니다.

물론, 앞서 언급했듯 귀도는 어디까지나 ABC 언어에서 Python을 만들겠다는 영감을 얻었습니다.

**Perl은 그저 같은 시대에 태어난 범부일 뿐입니다.**

더 자세하고 많은 Python 철학은 PEP 20 문서에서 찾을 수 있습니다.

### PEP?

```python
import this
```

위 코드를 통해서 Python의 설계 철학인 PEP 20 문서의 `The Zen of Python`을 출력시킬 수 있습니다.

```
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```

이러한 PEP는 `Python Enhancement Proposal`의 약자로,

직역 그대로 Python에 대한 개선 제안서입니다.

python의 발전과 개선을 위해 새로운 기능을 추가하거나,

정보를 제공하고 표준을 정의하는 데에 쓰인 토론장 및 보고서라고 할 수 있습니다.

또한 공식 레퍼런스로도 쓰이죠.

앞서 설명한 `The Zen of Python`은 `PEP`의 20번째 문서고,

VScode로 Python 코드를 작성하는 사람들에겐 자동으로 깔리는 `autopep8`이라는 포매터 익스텐션 역시

파이썬의 코드 스타일 가이드라인인 `PEP-8`을 기반으로 만들어진 것입니다.

PEP는 파이썬 생태계에 매우 중요한 역할입니다.

### 결국 쓰기 쉽고 재밌는 거

위의 The Zen of Python는 언뜻보면 대단한 의미를 가진 선언처럼 보이지만,

프로그래밍을 조금만 알아도 '당연한 말 아닌가?'싶은 부분들을 말하고 있습니다.

그러면서 지키기 어려운, 마치 클린코드나 초등학교 도덕과 같은 지침들을 말하고 있습니다.

이러한 지침은 상당히 모호해서 사실 시작할 때부터 반드시 지켜야지 하면서 지킬 수 있는 것은 아닙니다.

무엇보다 **파이썬은 애초에 선수 지식이 필요 없는 개발 언어**입니다.

국문과 출신인 저조차도 일주일동안 입문서 하나 읽고 로또 번호 생성기와 추첨기를 만들 정도였으니까요.

**'재미'** 그 자체를 추구했기에, **언어 자체도 근본 웃음벨이며, 이를 사용해 코딩하는 경험 또한 재미있습니다.**

사실 파이썬만 하는 것은 쉽지만, 이외의 언어를 접하는 건 상당히 어려워집니다.

_대부분 언어는 '모든 것이 객체는 아닌' 언어이며,_

_또한 '들여쓰기는 단지 가독성을 위한' 언어이고,_

_'중괄호와 세미콜론이 필수적인' 언어_ 이기 때문이죠.

이외에도 개발자의 편의를 위해 여타 언어들(심지어 같은 부모가 같은 C언어 기반 계열도)과 다른 문법이 매우 많습니다.

이 때문에 파이썬은 C계열, JAVA 개발자들에게 웃음벨로 통하곤 합니다.

![leaning_python_after_c++](leaning_python_after_c++.jpg){: width="350px"}
_제가 C++을 배우지 않는 이유입니다._

![im_using_python](im_using_python.webp){: width="350px"}
_Python 개발자는 땀흘릴 일이 없기 때문이죠_

그럼에도 파이썬은 현재 매우 사랑받은 언어임이 틀림없습니다.

작고(사실 겁나 큼) 소중한 우리의 언어, 파이썬이 꼭 사랑받았으면 합니다.

![using_the_python](using_the_python.jpg){: width="350px"}