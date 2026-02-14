import os
import hashlib

from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

import config_data as config


def check_md5(md5_str: str):
    """检查传入的md5是否已经被处理"""
    if not os.path.exists(config.md5_path):
        open(config.md5_path, 'w', encoding='utf-8').close()
        return False
    else:
        for line in open(config.md5_path, 'r', encoding='utf-8').readlines():
            line = line.strip()
            if line == md5_str:
                return True

        return False


def save_md5(md5_str: str):
    """将传入的md5字符串记录到文件内部"""
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + '\n')


def get_string_md5(input_str: str, encoding='utf-8'):
    """将传入的字符串转换为md5字符串"""

    # 将字符串转换为字节数组
    str_bytes = input_str.encode(encoding)

    # 创建md5对象
    md5_obj = hashlib.md5(str_bytes)

    # 计算md5
    md5_obj.update(str_bytes)

    # 返回md5字符串
    return md5_obj.hexdigest()


class KnowledgeBaseService(object):
    def __init__(self):
        # 向量存储实例
        os.makedirs(config.persist_directory, exist_ok=True)

        self.chroma = Chroma(
            collection_name=config.collection_name,  # 数据库名称
            embedding_function=DashScopeEmbeddings(model=config.embedding_model_name),  # 模型
            persist_directory=config.persist_directory,
        )

        # 文本切分实例
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len,
        )

    def upload_by_str(self, data: str, filename):
        md5_hex = get_string_md5(data)
        if check_md5(md5_hex):
            return "[跳过]内容已经存在知识库中"

        if len(data) > config.max_spliter_char_number:
            knowledge_chunks: list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "ycc"
        }

        self.chroma.add_texts(
            texts=knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks],
        )

        save_md5(md5_hex)

        return "[成功]内容成功载入向量库"


