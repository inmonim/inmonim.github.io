---
layout: post
title: "[Jekyll] _posts 말고 다른 디렉토리에 글쓰기"
date: 2023-12-27 16:44:18 +0900
categories: jekyll blog collections
tag: [Jekyll, Blog, 지킬]
---

# Jekyll - Collections란?

{: .prompt-tip }
> **Jekyll 기반의 Git blog에서 정적 페이지의 변환 과정에 _posts 디렉토리 이외에도 <br> `빌드 시 추가로 포함시킬 디렉토리를 지정해주는 기능`이라 할 수 있겠다.**

## **[핵심만 보고 싶으신 분들은 3-1로 이동하자](/posts/Jekyll__posts_말고_다른_디렉토리에_글쓰기/#3-1-_posts-이외의-디렉토리-추가)**

## **1. 공식 문서**

<br>

**[Jekyll 한국어 공식 문서 - 컬렉션](https://jekyllrb-ko.github.io/docs/collections)**

부분부분 어색한 문장과 번역이 이루어지지 않은 부분이 보이나

필요한 부분에 대해 충분히 설명이 잘 이루어져있다.

아래의 내용부터는 내가 겪은 문제들과 이를 해결한 방법에 대한 설명들이다.

<br>

<hr>


## **2. _posts 디렉토리의 포화**

<br>

~~사실 아직 제대로 작성한 포스팅도 없지만, jekyll 패키지를 열어본 순간부터 들었던 고민이었다.~~

![_posts 폴더](/posting/_posts_directory.png)

~~이 단 하나의 폴더 안에 앞으로의 모든 포스팅이 들어가야 한다는 것이다...~~

~~포스팅의 개수가 10개만 되어도 대단히 복잡할 것인데, 수 백 개의 포스팅은 어떻게 감당할 수 있겠는가...~~

~~심지어 포스팅할 markdown 파일은 제목을 반드시 yyyy-MM-dd-Title 형식을 준수하여야 하므로 이 문제가 더욱 크게 와닿았다.~~

~~그래서 디렉토리를 분할하는 방법을 찾던 중, Collections 기능을 찾게 되었다.~~

>그냥 MD파일의 타이틀 컨벤션만 잘 지키면<br>`_posts`에 하위 디렉토리를 추가해도 정상적으로 인식 한다...
{: .prompt-tip}

![posts 계층](/posting/tree.png)
_그냥 하면 되는 거였다..._

GPT를 믿었던 내가 바보였다.

<br>

<hr>

## **3. Collections 사용**

Git blog 자체도 처음이기 때문에, liquid 엔진이나 chirpy 테마에서 만들어둔 서식들에 익숙해지고 싶었다.

chirpy 테마는 친절하게 다양한 튜토리얼을 포스팅으로 만들어 두었다.

![chirpy 튜토리얼](/posting/chirpy_tutorial.png)
_chirpy 테마를 처음 실행하면 보이는 화면이며, 4개의 튜토리얼이 준비되어있다_

해당 파일들은 chirpy 테마 위에서만 제대로 변환되기 때문에, vscode 등의 환경에서는 제대로 보이지 않는다.

즉, 블로그에서 튜토리얼을 없애면 튜토리얼을 볼 수 없어진다는 것이다...

**하지만 이 튜토리얼들이 내 블로그 포스팅 목록에서는 보이지 않게 만들고 싶다!**

그래서 해당 팁들을

1. _posts디렉토리가 아닌 다른 디렉토리로 분리하고 [#](/posts/Jekyll__posts_말고_다른_디렉토리에_글쓰기/#3-1-_posts-이외의-디렉토리-추가)

2. url을 통해서 접근할 수 있도록 만들 예정이었다. [#](/posts/Jekyll__posts_말고_다른_디렉토리에_글쓰기/#3-2-접근할-수-있도록-url을-지정해주자)

3. 포스팅 목록에 뜨지 않게 만드는 것은 상당히 쉬웠다.

기회가 된다면 한국어로 번역해서 따로 올려보도록 해야지.

<br>

### **3-1. _posts 이외의 디렉토리 추가**

#### 1. 먼저 루트 디렉토리에 추가할 디렉토리를 생성해주자.

나는 tip이 들어갈 디렉토리인만큼, `_tips`로 지정했다.

> 반드시 디렉토리 이름 앞에 `_`를 붙여줘야 인식할 수 있다.
{: .prompt-info }

![tips_directory](/posting/_tips_directory.png)
_후술하겠지만, 여기서 `2번 항목`이 해결되었다_

<br>

#### 2. _config 파일로 접속해, collections를 추가(또는 수정) 해주자.

![collections](/posting/collections.png)
_위의 설정에서 볼 수 있듯, chirpy 테마에서는 `taps`, 즉 패키지에 포함된 `_taps` 디렉토리 또한 collections 기능을 통해 추가로 인식시킨 디렉토리인 것을 확인할 수 있다._

위의 빨간 박스 안의 내용 처럼 추가해주자.

**여기선 `_`를 삭제하여 넣자.**

> `output: true` 옵션은 **컨텐츠를 보여줄 것인가?**인데, 그냥 `true`로 설정해주자. <br>`false`는 해당 collection을 숨기는 것과 마찬가지다... ~~왜 있는 거야~~
{: .prompt-info}

>이외에도 정렬기준을 추가하는 등의 여러 옵션이 있으니 <br> [Jekyll 공식 docs - collections의 여러 옵션](https://jekyllrb-ko.github.io/docs/collections/#%EB%AC%B8%EC%84%9C-%EC%88%9C%EC%84%9C-%EC%A1%B0%EC%A0%95)에서 확인해보자.
{: .prompt-tip }

이제 jekyll은 `_tips`와 하위 파일들을 인식할 수 있게 되었다.

build 결과물인 `_site` 디렉토리를 확인해보면 아래와 같이 `tips`디렉토리와와 마크다운 파일들이 정적파일로 변환된 것을 확인할 수 있다.

![site_tips](/posting/_site.png)

하지만 이를 배포했을 때는, 호스팅할 url을 지정해주지 않아 해당 파일에 대한 접근이 사실상 불가능하다.

>로컬 호스팅 환경에서 실행했을 때는, 127.0.0.1/{collection_title}/{file_title}로 접근할 수 있으나 <br>github에서 배포할 시에는 해당 방법을 통한 접근이 불가능하다.
{: .prompt-warning}

### **3-2. 접근할 수 있도록 URL을 지정해주자**

<br>

두 가지의 방법이 있다.

#### 1. 각각의 MD 파일마다 직접 링크를 달아주는 방법이 있다.

각각의 포스트(md파일)의 YAML Front Matter에서 해결할 수 있다.

![yamlfrontmatter](/posting/yamlfrontmatter.png)

`layout: post`와 같이, `permalink: {collection_title}/{file_title}`정도로 설정해주면 된다.

이렇게 될 경우, 정적파일의 url이 명시적으로 생기기 때문에 포스팅 목록에 없어도 접근할 수 있게 된다!

#### 2. _config에서 default 설정 변경을 통한 일괄 처리

![default](/posting/default.png)

`type` 속성에 `_`를 제외한 collection의 이름을 넣어준 뒤,

layout을 정해주고 YAML Front Matter처럼 공통으로 쓰일 URL을 지정해주면 된다.

위의 `:title`의 경우, 각 MD 파일의 YAML Front Matter에 지정된 title 속성이 아니라,

실제 MD 파일의 타이틀 (컨벤션을 지켰을 경우, 날짜를 제외한 파일의 제목)을 말한다!

<br>

---

이것으로 `_posts` 디렉토리 이외의 커스텀 디렉토리를 Jekyll에게 인식시키고 들어가는 것이 끝났다.

마지막으로, 기본적인 설정에 따르면 `_posts` 디렉토리 이외의 디렉토리에 존재하는 MD파일은

`layout`이 `post`라고 해도 포스팅 목록에 포함되지 않는 모양이다!

즉, 따로 해줄 것이 없다...