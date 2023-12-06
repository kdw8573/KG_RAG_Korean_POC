from nebula3.gclient.net import ConnectionPool
from nebula3.Config import Config
import os
from llama_index import (
    KnowledgeGraphIndex,
    ServiceContext,
    SimpleDirectoryReader,
)
from llama_index.storage.storage_context import StorageContext
from llama_index.graph_stores import NebulaGraphStore
from llama_index.prompts import PromptTemplate
from llama_index.llms import HuggingFaceLLM
from langchain.embeddings import HuggingFaceEmbeddings
from korre import KorRE

korre = KorRE()

def extract_triplets_korre(text):
    output = []
    for line in text.split('\n'):
        print(line)
        triplets = korre.infer(line)
        count = 0
        for subject, object_, relation in triplets:
            if subject != '' and relation != '' and object_ != '':
                output.append((subject.strip(), relation.strip(), object_.strip()))
                count += 1
            if count > 3:
                break
    print(output)
    return output

os.environ["GRAPHD_HOST"] = "127.0.0.1"
os.environ["NEBULA_USER"] = "root"
os.environ["NEBULA_PASSWORD"] = "nebula" 
os.environ["NEBULA_ADDRESS"] = "127.0.0.1:9669" 

config = Config()
config.max_connection_pool_size = 10
connection_pool = ConnectionPool()
connection_pool.init([('127.0.0.1', 9669)], config)

session = connection_pool.get_session('root', 'nebula')
session.execute('CREATE SPACE IF NOT EXISTS phillies_rag(vid_type=FIXED_STRING(256), partition_num=1, replica_factor=1);')
session.execute(':sleep 10')
session.execute('USE phillies_rag;')
session.execute(':sleep 10')
session.execute('CREATE TAG IF NOT EXISTS entity(name string);')
session.execute(':sleep 10')
session.execute('CREATE EDGE IF NOT EXISTS relationship(relationship string);')
session.execute(':sleep 10')
session.execute('CREATE TAG INDEX IF NOT EXISTS entity_index ON entity(name(256));')

space_name = "phillies_rag"
edge_types, rel_prop_names = ["relationship"], ["relationship"]
tags = ["entity"]

graph_store = NebulaGraphStore(
    space_name=space_name,
    edge_types=edge_types,
    rel_prop_names=rel_prop_names,
    tags=tags,
)
storage_context = StorageContext.from_defaults(graph_store=graph_store)

documents = SimpleDirectoryReader("./data/").load_data()

query_wrapper_prompt = PromptTemplate("사용자가 한 말을 읽고 그에 질문에 답하거나 명령에 응답하는 비서입니다.\n\n{query_str}\n\n비서:")

llm = HuggingFaceLLM(
    context_window=2048,
    max_new_tokens=256,
    generate_kwargs={"temperature":0.25, "do_sample": True},
    query_wrapper_prompt=query_wrapper_prompt,
    tokenizer_name="Minirecord/Mini_DPO_7b_01",
    model_name="Minirecord/Mini_DPO_7b_01",
    device_map="auto",
)
embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
service_context = ServiceContext.from_defaults(chunk_size=512, llm=llm, embed_model=embed_model)

kg_index = KnowledgeGraphIndex.from_documents(
    documents=documents,
    kg_triplet_extract_fn=extract_triplets_korre,
    storage_context=storage_context,
    max_triplets_per_chunk=15,
    service_context=service_context,
    space_name=space_name,
    edge_types=edge_types,
    rel_prop_names=rel_prop_names,
    tags=tags,
    include_embeddings=True,
)
kg_index.set_index_id("demo_kg_index")
kg_index.storage_context.persist(persist_dir='./storage_graph')


session.release()