# Graph RAG 정리

## ToDo

- [ ] 다양한 LLM 모델을 이용한 성능 및 속도 비교
- [ ] 한글 문장 내 관계 추출 모델 고도화

## RAG

- 기존 Pre-train 된 model들은 parameter안에 지식을 저장하여, 특정 도메인에 대한 정보를 외부 접근 없이 알 수 있다. 그러나 많은 양의 파라미터를 학습하는데 소요되는 비용 문제와 hallucination 문제가 발생한다.
- 검색 증강 생성(Retrieval Augmented Generation.RAG)은 non-parametric memory을 이용해 이러한 문제들을 해결하고자 했다.
- RAG model은 기본적으로 `input sequence x`를 input으로 받게 되면, 이를 이용하여 외부 documents로부터 관련성이 높은 `document d`를 k개 retrieve 한다. 이후 LLM에서 x와 d를 이용하여 `target sequence y`를 generate하게 된다.
  ![RAG figure](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fcu77eM%2FbtscQaJ0rOg%2FoCvPXGa1z6vuqfZrs7fvTK%2Fimg.png)

## Knowledge Graph

- 지식 그래프는 개체, 이벤트, 상황 또는 추상적 개념과 같은 개체의 상호 연결된 설명을 저장하는 동시에 사용된 용어의 기본 의미 체계를 인코딩하는 데 자주 사용된다(출처: 위키백과).
- 빅데이터를 컴퓨터가 읽을 수 있는 방식으로 저장할 수 있는 데이터 모델 중 하나이다.
- 지식을 그래프 형태로 구축한 것이며, 두 가지 구성요소인 node와 edge가 있고 node가 `entity`, edge가 `relationship`이 된다.
- 그래프의 데이터 기본 단위는 triplet 형태로 표현된다. `(𝒉, 𝙧, 𝒕) = 𝒉(head entity), 𝙧(relation), 𝒕(tail entity)`.
- Knowledge Graph database는 triplet을 이용함으로써, 효율적으로 Graph에 data를 저장하고 질의할 수 있다.
- NebulaGraph는 Knowledge Graph database의 오픈소스 중 하나이다.
  ![knowledge graph](https://pbs.twimg.com/media/FEi6QMNXoAAUHZJ?format=jpg&name=large)_Knowledge Graph 예시_
  ![triplet](https://velog.velcdn.com/images%2Fjbeen2%2Fpost%2Ff002cfb0-23d5-4fde-ab85-2168e9b900e9%2Fimage.png)_triplet 예시_

## LlamaIndex

- RAG pipeline을 구성하게 도와주는 python 라이브러리.
- Knowledge Base를 준비하는 `indexing stage`와 Knowledge Base에서 쿼리와 관련성이 높은 node를 검색하여 쿼리와 함께 node를 LLM에 전달하는 `query stage`로 이루어진다.

  ![RAG workflow](https://i0.wp.com/www.usefulparadigm.com/wp-content/uploads/2023/09/LlamaIndex_workflow.png?w=720&ssl=1)

- indexing stage
  1. 데이터 소스를 Data Loader를 통해 Document 형태로 읽어온다.
  2. Documents를 chunk size만큼 parsing하여 node 단위로 나눈다.
  3. 데이터가 검색되기 쉬운 형식으로 색인화(indexing)를 진행. 대표적으로 vector indexing이 존재하며, node를 embedding model을 사용해서 embedding을 한뒤, vector형식으로 저장.
  4. 메모리에 있는 index를 다양한 storage backends(local, S3, ...)에 저장한다.
     ![indexing stage](https://velog.velcdn.com/images/daejang_jang_lee/post/5be44ba9-2b41-409f-aa6e-114e15c4392b/image.png)_indexing stage 과정_
- query stage
  1. Retrievers: 구축된 index에서 관련 node들을 효율적으로 검색. KnowldegeGraph index에서는 entity 단위로 vector similarity를 이용해 관련성이 높은 node를 찾는다.
  2. Node postprocessors: 검색된 node를 특정 로직에 따라 필터링 및 리랭킹.
  3. Response Synthesizers: 사용자 쿼리와 함께 검색된 node들을 사용해 LLM에서 최종 응답을 생성.
     ![query stage](https://velog.velcdn.com/images/daejang_jang_lee/post/aa1ec8ee-576f-4cb3-a78c-9d612dfb4a2a/image.png)_query stage 과정_

## KG Query Engine

```python
query_engine = kg_index.as_query_engine()
```

- KG entities with vector similarity, pulls in linked text chunks and optionally explores relationships.

```python
kg_keyword_query_engine = kg_index.as_query_engine(
# setting to false uses the raw triplets instead of adding the text from the corresponding nodes
    include_text=False,
    retriever_mode="keyword",
    response_mode="tree_summarize",
)
```

- keywords from the query to retrieve relevant KG entities, pulls in linked text chunks, and optionally explores relationships.
- `include_text=False`: the query engine will only use the raw triplets for queries.
- `response_mode="tree_summarize"`: The tree_summarize response mode is useful for summarization tasks, such as providing a high-level overview of a topic or answering a question that requires a comprehensive response.

```python
kg_hybrid_query_engine = kg_index.as_query_engine(
    include_text=True,
    response_mode="tree_summarize",
    embedding_mode="hybrid",
    similarity_top_k=3,
    explore_global_knowledge=True,
)
```

- The KG hybrid entity retrieval uses keywords to find relevant triplets. Then, it also uses vector-based entity retrieval to find similar triplets based on semantic similarity.
- `include_text=True`: the query engine will use text from the corresponding nodes in the response.
- `similarity_top_k=3`: it will retrieve the top three most similar results based on the embeddings.
- `explore_global_knowledge=True`:When explore_global_knowledge=True is set, the query engine will not limit its search to the local context (i.e., the immediate neighbors of a node) but will also consider the broader, global context of the knowledge graph.
  ![query pros & cons](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*0UsLpj7v2GO67U-99YJBfg.png)

## 출처

- https://arxiv.org/abs/2005.11401
- https://gbdai.tistory.com/67
- https://dining-developer.tistory.com/64
- https://velog.io/@jbeen2/CS224W-17.-Reasoning-over-Knowledge-Graph
- https://betterprogramming.pub/getting-started-with-llamaindex-part-2-a66618df3cd
- https://betterprogramming.pub/getting-started-with-llamaindex-169bbf475a94
- https://www.usefulparadigm.com/2023/09/05/llamaindex%F0%9F%A6%99%EC%99%80-rag%EC%9D%98-%EA%B8%B0%EB%B3%B8-%EA%B0%9C%EB%85%90/
- https://velog.io/@daejang_jang_lee/LlamaIndex%EC%9D%98-%EA%B8%B0%EB%B3%B8-%EA%B0%9C%EB%85%90
- https://nanonets.com/blog/llamaindex/
- https://www.youtube.com/watch?v=bPoNCkjDmco
- https://www.nebula-graph.io/posts/Knowledge-Graph-and-LlamaIndex
