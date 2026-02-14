# config_data.py
md5_path = "./md5.text"

# 向量数据库配置
collection_name = "rag"
persist_directory = "./chroma_db"

# 分块配置
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", ".", "!", "?", "。", "？", "！", " ", ""]

# 块分词器配置
max_spliter_char_number = 1000

# 向量检索配置
similarity_threshold = 2

embedding_model_name = "text-embedding-v4"
chat_model_name = "qwen3-max"

chat_history_path = "./chat_history"

session_config = {
    "configurable":{
        "session_id": "user_001",
    }
}