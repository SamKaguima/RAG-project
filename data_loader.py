from openai import OpenAI
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
from dotenv import load_dotenv
from typing import List

load_dotenv()

client = OpenAI()
EMBED_MODEL = "text-embedding-3-large"
EMBED_DIM = 3072

# correct parameter name: chunk_size
splitter = SentenceSplitter(chunk_size=1000, chunk_overlap=200)


def load_and_chunk_pdf(path: str) -> List[str]:
    docs = PDFReader().load_data(file=path)
    texts = [d.text for d in docs if getattr(d, "text", None)]
    chunks: List[str] = []
    for r in texts:
        chunks.extend(splitter.split_text(r))
    return chunks


def embed_texts(text: List[str]) -> List[List[float]]:
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=text,
    )
    return [r.embedding for r in response.data]