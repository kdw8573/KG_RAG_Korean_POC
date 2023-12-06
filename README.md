# KnowledgeGraph 기반 RAG 모델

## NebulaGraph 설치 및 설정

1. NebulaGraph 설치

```sh
wget https://oss-cdn.nebula-graph.com.cn/package/3.6.0/nebula-graph-3.6.0.ubuntu2004.amd64.tar.gz
tar -xvzf nebula-graph-3.6.0.ubuntu2004.amd64.tar.gz
```

2. NebulaGraph 설정

```sh
cd nebula-graph-3.6.0.ubuntu2004.amd64/etc
mv nebula-graphd.conf.default nebula-graphd.conf
mv nebula-metad.conf.default nebula-metad.conf
mv nebula-storaged.conf.default nebula-storaged.conf
```

3. NebulaGraph 서비스 시작

```sh
cd nebula-graph-3.6.0.ubuntu2004.amd64/script
./nebula.service start all
```

4. NebulaGraph 콘솔 설치 및 접속

```sh
wget https://github.com/vesoft-inc/nebula-console/releases/download/v3.6.0/nebula-console-linux-amd64-v3.6.0
mv nebula-console-linux-amd64-v3.6.0 nebula-console
chmod 111 nebula-console
./nebula-console -addr 127.0.0.1 -port 9669 -u root -p nebula
(nebula-console) ADD HOSTS 127.0.0.1:9779
```

## 패키지 설치

```sh
pip install llama_index nebula3-python llama-hub whoosh word2word g2p-en kss marisa-trie
pip install fairseq easydict wget
pip install sentence-transformers pororo --no-deps
```

## 한글 문서 준비

```sh
mkdir data
```

- data 폴더 내에 한글 문서 생성

## 실행

```sh
python rag_make_triplet.py
python rag_query.py
```

## Example

```
query: 수원FC에 대해 상세하게 알려줘
output: 수원FC는 대한민국 수원시에 기반을 둔 프로 축구 클럽입니다. 2012년에 창단된 이 클럽은 축구를 실천하는 클럽입니다. 수원FC는 수원월드컵경기장에서 홈 경기를 치르며 한국프로축구연맹(K리그1)에서 활동하고 있습니다.
```
