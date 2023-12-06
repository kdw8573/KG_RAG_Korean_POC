# Graph RAG 정리

## RAG

- 기존 Pre-train 된 model들은 parameter안에 지식을 저장하여, 특정 도메인에 대한 정보를 외부 접근 없이 알 수 있다. 그러나 많은 양의 파라미터를 학습하는데 소요되는 비용 문제와 hallucination 문제가 발생한다.
- 검색 증강 생성(Retrieval Augmented Generation.RAG)은 non-parametric memory을 이용해 이러한 문제들을 해결하고자 했다.
- RAG model은 기본적으로 `input sequence x`를 input으로 받게 되면, 이를 이용하여 외부 documents로부터 관련성이 높은 `document d`를 k개 retrieve 한다. 이후 LLM에서 x와 d를 이용하여 `target sequence y`를 generate하게 된다.
  ![RAG figure](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fcu77eM%2FbtscQaJ0rOg%2FoCvPXGa1z6vuqfZrs7fvTK%2Fimg.png)

## Knowledge Graph

- 지식 그래프는 개체, 이벤트, 상황 또는 추상적 개념과 같은 개체의 상호 연결된 설명을 저장하는 동시에 사용된 용어의 기본 의미 체계를 인코딩하는 데 자주 사용된다(source 위키백과).
- 빅데이터를 컴퓨터가 읽을 수 있는 방식으로 저장할 수 있는 데이터 모델 중 하나이다.
- 지식을 그래프 형태로 구축한 것이며, 두 가지 구성요소인 node와 edge가 있고 node가 `entity`, edge가 `relationship`이 된다.
- 그래프의 데이터 기본 단위는 triplet 형태로 표현된다. `(𝒉, 𝙧, 𝒕) = 𝒉(head entity), 𝙧(relation), 𝒕(tail entity)`.
- Knowledge Graph database는 triplet을 이용함으로써, 효율적으로 Graph에 data를 저장하고 질의할 수 있다.
- NebulaGraph는 Knowledge Graph database의 오픈소스 중 하나이다.
  ![knowledge graph](https://pbs.twimg.com/media/FEi6QMNXoAAUHZJ?format=jpg&name=large)_Knowledge Graph 예시_
  ![triplet](https://velog.velcdn.com/images%2Fjbeen2%2Fpost%2Ff002cfb0-23d5-4fde-ab85-2168e9b900e9%2Fimage.png)_triplet 예시_

## LlamaIndex

-

## 출처

- https://arxiv.org/abs/2005.11401
- https://gbdai.tistory.com/67
- https://dining-developer.tistory.com/64
- https://velog.io/@jbeen2/CS224W-17.-Reasoning-over-Knowledge-Graphs
