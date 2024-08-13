---
layout: post
title: "[JPA] 1:1 식별 관계에서 JPA는 어떻게 동작할까"
date: 2024-08-13 17:00:00 +0900
categories: backend spring
tag: [JPA, Spring]
---

>Kotlin 기반의 설명입니다.
{: .prompt-info}

# 1:1 식별 관계에서 JPA는 요상하게 동작한다.

`User`와 `Profile`이 존재한다.

User 엔티티에는 로그인 및 이름과 같은 필수 정보가,

Profile 엔티티에는 프로필 사진, 성별 등등의 부가적인 정보가 들어간다.

즉, Profile은 User의 기본키(user_id)를 외래키이자 기본키로 쓰는 `식별 관계`가 된다.

User 엔티티는 관계의 주인이 되고, Profile은 그를 따라가게 된다.

간단하게 코드를 짜본다면 다음과 같아진다.

```kotlin
// User Entity
@Entity
@Table(name = "user")
class User(
  @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
  val userId : Long? = null,

  val loginId : String,

  ...

  @OneToOne(mappedBy = "user")
  val profile : Profile? = null,
)

// Profile Entity
@Entity
@Table(name = "profile")
class Profile(
  @Id
  val userId : Long? = null,

  @MapsId
  @OneToOne
  @JoinColumn(name = "userId")
  var user : User,

  var photoUrl : String,
  
  ...
)
```

`User` 엔티티는 `Profile` 엔티티를 프로퍼티로 가지고, maapedBy를 `Profile에 선언된 User 즉, 자기 자신`으로 해놓는다.

`Profile` 엔티티 또한 `User`를 프로퍼티로 가지는데, `@MapsId`를 통해 `Profile`의 식별자인 userId를 자신의 식별자로 삼는다.

## 실제로 사용한다면?

```kotlin
val user = User(...)

val savedUser = userRepository.save(user)

val profile = Profile(savedUser.userId, savedUser, ...)

// 여기서 기본키에는 null이 들어갈 수 없다는 에러가 발생한다.
profileRepository.save(profile)
```

대부분의 JAVA 기반 자료나 GPT도 위와 같은 코드를 알려주고 있으나,

hibernates 수준에서 null identifier 에러가 발생한다.

```kotlin
val profile = Profile(savedUser.userId, savedUser, ...)
```

이렇게 직접 ID와 User를 지정해 객체를 생성했음에도, save 과정에서 에러가 터진다.

## 해결책

가장 간단한 해결책은 다음과 같다.

```kotlin
val profile = Profile(savedUser.userId, savedUser, ...)

savedUser.profile = profile

return ...
```

savedUsre의 profile에 값을 넣어주면, 더티 체킹을 통해 트랜잭션이 끝날 때 Profile에 값이 알아서 저장된다.

굉장히 비직관적인 코드인데, 이러한 사단이 나는 이유는 위에서 말한 바 때문이다.

## 원인?

>User 엔티티의 Profile 프로퍼티의 mappedBy 대상을 Profile에 선언된 User 즉, 자기 자신으로 한다.
{: .prompt-info}

`mappedBy`의 대상은 `user.profile.user`가 되는 셈이다.

그러나 위의 코드에서 `profile` 객체가 저장되는 시점에는, `profile`에 주입된 `user`객체에는 `user.profile`이 존재하지 않는다.

`profile`이 참조해야 하는 `Id`는 `user.profile.user.userId` 이기 때문이다... (이게 뭔...)

따라서, `profile` 엔티티 본체는 user 객체의 프로퍼티로써 존재하는 `profile`이다.

그렇기 떄문에 `user.profile`에 값이 추가되면 더티 체킹을 통해 트랜잭션이 완료될 때 `Profile` 데이터가 입력된다.

다시 코드를 보자.

```kotlin
val user = User(...)

val savedUser = userRepository.save(user)

val profile = Profile(savedUser.userId, savedUser, ...)

// 즉, 이 시점에서는 profile.user.profile이 없으므로, save를 실시하면 id가 null이라고 에러를 뱉는 것이다. 것이다.(...)
// profileRepository.save(profile)

// 그리고 User 객체에만 profile을 추가해줘도 profile 값이 DB에 저장된다.
savedUser.profile = profile

return ...
```

### 또 다른 해결책?

굳이 profileRepository.save(profile)로 명시적으로 저장을 하고 싶다면, 다음처럼 할 수도 있다...

```kotlin
val user = User(...)

val savedUser = userRepository.save(user)

val profile = Profile(savedUser.userId, savedUser)

savedUser.profile = profile

val newSavedUser = userRepository.save(savedUser)

profile.user = savedUser

profileRepository.save(profile)

return ...
```

다만, 이 경우 `newSavedUser`를 선언하는 단계에서 불필요한 db 조회가 일어나기 때문에 비추천한다.