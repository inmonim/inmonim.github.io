---
layout: post
title: Jekyll collections - _posts말고 다른 디렉토리에 글쓰기
date: 2023-12-27 16:44:18 +0900
categories: jekyll blog collections
---

# Jekyll - Collections란?

{: .prompt-tip }
> **Jekyll 기반의 Git blog에서 정적 페이지의 변환 과정에 _posts 디렉토리 이외에도 <br> `추가로 포함시킬 디렉토리를 지정해주는 기능`이라 할 수 있겠다.**

## 1. 공식 문서

<br>

**[Jekyll 한국어 공식 문서 - 컬렉션](https://jekyllrb-ko.github.io/docs/collections)**

부분부분 어색한 문장과 번역이 이루어지지 않은 부분이 보이나

필요한 부분에 대해 충분히 설명이 잘 이루어져있다.

아래의 내용부터는 내가 겪은 문제들과 이를 해결한 방법에 대한 설명들이다.

<br>

<hr>

<br>


## 2. _posts 디렉토리의 포화

<br>

사실 아직 제대로 작성한 포스팅도 없지만, jekyll 패키지를 열어본 순간부터 들었던 고민이었다.

![_posts 폴더](/assets/img/posting/_posts_directory.png)

이 단 하나의 폴더 안에 앞으로의 모든 포스팅이 들어가야 한다는 것이다...

포스팅의 개수가 10개만 되어도 대단히 복잡할 것인데, 수 백 개의 포스팅은 어떻게 감당할 수 있겠는가...

심지어 포스팅할 markdown 파일은 제목을 반드시 yyyy-MM-dd-Title 형식을 준수하여야 하므로 이 문제가 더욱 크게 와닿았다.

그래서 디렉토리를 분할하는 방법을 찾던 중, Collections 기능을 찾게 되었다.

<br>

<hr>

<br>

## 3. Collections 사용

Git blog 자체도 처음이기 때문에, liquid 엔진이나 chirpy 테마에서 만들어둔 서식들에 익숙해지고 싶었다.

chirpy 테마는 친절하게 다양한 튜토리얼을 포스팅으로 만들어 두었다.

![chirpy 튜토리얼](/assets/img/posting/chirpy_tutorial.png)
_chirpy 테마를 처음 실행하면 보이는 화면이며, 4개의 튜토리얼이 준비되어있다_

해당 파일들은 chirpy 테마 위에서만 제대로 변환되기 때문에, vscode 등의 환경에서는 제대로 보이지 않는다.

즉, 블로그에서 튜토리얼을 없애면 튜토리얼을 볼 수 없어진다는 것이다...

그래서 해당 팁들을

1. _posts디렉토리가 아닌 다른 디렉토리로 분리하고 [#](/posts/Jekyll-블로그-collections-_posts말고-다른-디렉토리에-글쓰기/#3-1-_posts-이외의-디렉토리-추가)

2. 포스팅 목록에서는 보이지 않지만

3. url을 통해서 접근할 수 있도록 만들 예정이었다.

기회가 된다면 한국어로 번역해서 따로 올려보도록 해야지.

<br>

### 3-1. _posts 이외의 디렉토리 추가

#### 먼저 루트 디렉토리에 추가할 디렉토리를 생성해주자.

나는 tip이 들어갈 디렉토리인만큼, `_tips`로 지정했다.

> 반드시 디렉토리 이름 앞에 `_`를 붙여줘야 인식할 수 있다.
{: .prompt-info }

![tips_directory](/assets/img/posting/_tips_directory.png)
_후술하겠지만, 여기서 `2번 항목`이 해결되었다_

<br>

2- _config 파일로 접속해, collections을 추가(또는 수정) 해주자.

![collections](/assets/img/posting/collections.png)

위의 설정에서 볼 수 있듯, chirpy 테마에서는 `taps`, 즉 패키지에 포함된 `_taps` 디렉토리 또한 collections 기능을 통해 추가로 인식시킨 디렉토리인 것을 확인할 수 있다.

위의 빨간 박스 안의 내용 처럼 추가해주자. 여기선 `_`를 삭제하여 넣자.

`output: true` 옵션은 `컨텐츠를 보여줄 것인가?`인데, 그냥 `true`로 설정해주자.

*`false`를 설정할 경우, 그냥 안 한 것과 똑같아진다...*

이외에도 정렬기준을 추가하는 등의 여러 옵션이 있으니, [공식 docs](https://jekyllrb-ko.github.io/docs/collections/#%EB%AC%B8%EC%84%9C-%EC%88%9C%EC%84%9C-%EC%A1%B0%EC%A0%95)에서 확인해보자.

이제 jekyll은 `_tips`와 하위 파일들을 인식할 수 있게 되었다.

build 결과물인 `_site` 디렉토리를 확인해보면 아래와 같이 `tips`디렉토리와와 마크다운 파일들이 정적파일로 변환된 것을 확인할 수 있다.

![site_tips](/assets/img/posting/_site.png)

하지만 이를 배포했을 때는, 호스팅할 url을 지정해주지 않아 해당 파일에 대한 접근이 사실상 불가능하다.

>로컬 호스팅 환경에서 실행했을 때는, 127.0.0.1/{collection_title}/{file_title}로 접근할 수 있으나 <br>github에서 배포할 시에는 해당 방법을 통한 접근이 불가능하다.
{: .prompt-warning}

<br>

### 3-2. 포스팅 목록에서 숨기기

<br>

>포스트 목록에 드러나지 않고<br>다른 포스팅과 상호작용(연관 포스트, 이전 또는 다음 포스트 등등)이 없는 포스트를 작성할 수 있는 방법이기도 하다.
{: .prompt-tip}

매우 간단하다. 포스팅 Markdown 파일의 타이틀 컨벤션을 지키지 않으면 된다.

![tips_directory](/assets/img/posting/_tips_directory.png)
_이처럼 말이다_

이렇게 할 경우, 포스트로 인식하지 못해 포스트로써 지원되는 기능들을 쓸 수 없고, 목록 및 모아보기에서도 제거된다.

다만 유의할 점도 있는데,

<br>

1- 해당 문서에만 존재하는 태그 및 카테고리를 YAML Front Matter에서 삭제해야 한다.

태그가 포함되거나 카테고리에 속한 포스트를 모아보는 기능이 있는 경우,

태그와 카테고리는 존재하나 게시글은 없는 것으로 인식한다.

이럴 경우 github 빌드 및 테스트에서 문제가 발생할 수 있다.


2- 반드시 YAML Front Matter에서 layout을 설정해주어야 한다.

_config 파일을 확인하면, defaults에서 post로 인식된 파일들은 기본적으로 `layout: post`의 속성이 붙도록 설계되어 있다.

포스팅 컨벤션을 지키지 않은 md파일은 layout 속성이 지정되지 않아, 해당 테마에서 설정한 형식의 포스트 정적 파일이 아닌,

어떠한 레이아웃도 없이 MD파일만 덩그러니 변환된 정적파일로 변환되므로

YAML Front Matter에서 직접 입력해주어야 한다.

3- 반드시 permalink를 지정해주어야 한다.

<br>

### 3-3. 접근할 수 있도록 URL을 지정해주자

<br>

3-2의 3번 문제는 각각의 포스트(md파일)의 YAML Front Matter에서 해결할 수 있다.

![yamlfrontmatter](/assets/img/posting/yamlfrontmatter.png)

`layout: post`와 같이, `permalink: {collection_title}/{file_title}`정도로 설정해주면 된다.

이렇게 될 경우, 정적파일의 url이 명시적으로 생기기 때문에 포스팅 목록에 없어도 접근할 수 있게 된다!