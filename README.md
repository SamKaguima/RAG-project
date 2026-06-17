# RAG Project

A Retrieval-Augmented Generation (RAG) system that allows you to upload PDF documents and ask questions about their content. The system uses vector embeddings to retrieve relevant context from PDFs and leverages OpenAI's GPT-4 to generate accurate answers based on the retrieved context.

## Features

- **PDF Ingestion**: Upload and process PDF documents with automatic text chunking
- **Vector Embeddings**: Uses OpenAI's text-embedding-3-large model to create semantic embeddings
- **Vector Storage**: Stores embeddings in Qdrant for efficient similarity search
- **AI-Powered Q&A**: Leverages GPT-4o-mini to answer questions based on document context
- **Web UI**: Streamlit-based interface for easy PDF upload and querying
- **Event-Driven Architecture**: Uses Inngest for reliable event-driven workflows

## Architecture

### Components

- **FastAPI Backend** (`main.py`): Provides API endpoints and manages Inngest workflows
  - `RAG: Ingest PDF`: Handles PDF ingestion, chunking, embedding, and storage
  - `RAG: Query PDF`: Processes user queries and generates AI responses

- **Streamlit Frontend** (`streamlit_app.py`): User-friendly web interface
  - PDF upload functionality with local file storage
  - Q&A form with configurable context retrieval (top-k)
  - Real-time result display with source attribution

- **Data Processing** (`data_loader.py`): PDF parsing and text embeddings
  - Loads PDFs using LlamaIndex file readers
  - Chunks text using SentenceSplitter (1000 char chunks with 200 char overlap)
  - Creates embeddings using OpenAI's text-embedding-3-large model

- **Vector Database** (`vector_db.py`): Qdrant-based vector storage
  - CRUD operations for vectors and metadata
  - Similarity search with configurable top-k results
  - Cosine distance metric for semantic similarity

- **Type Definitions** (`custom_types.py`): Pydantic models for type safety

## Requirements

- Python 3.13+
- OpenAI API key
- Qdrant instance running (default: http://localhost:6333)
- Inngest service for local development

## Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd RAG-project
```

### 2. Install dependencies
Using `uv` (recommended):
```bash
uv sync
```

Or using `pip`:
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
INNGEST_API_BASE=http://127.0.0.1:8288/v1  # Local dev server default
```

### 4. Start services

**Qdrant Vector Database:**
```bash
docker run -p 6333:6333 qdrant/qdrant:latest
```

**Inngest Local Service** (in a separate terminal):
```bash
inngest run
```

## Usage

### Start the Streamlit app
```bash
streamlit run streamlit_app.py
```

The app will be available at `http://localhost:8501`

### Using the web interface

1. **Upload PDF**: Select a PDF file to ingest. The system will:
   - Parse the PDF content
   - Split text into chunks for better context retrieval
   - Create vector embeddings
   - Store in Qdrant

2. **Ask Questions**: Enter your question and select how many context chunks to retrieve (1-20)
   - The system will search for semantically similar content
   - GPT-4o-mini will generate an answer using the retrieved context
   - Results display the answer with source attribution

### Running the backend directly

The FastAPI backend is available at `http://localhost:8000` (when running with Uvicorn):
```bash
uvicorn main:app --reload
```

You can trigger workflows via API events to Inngest.

## Workflow Details

### PDF Ingestion Workflow
1. Event: `rag/ingest_pdf` with pdf_path and optional source_id
2. Load and chunk PDF
3. Embed text chunks using OpenAI
4. Generate deterministic IDs for deduplication
5. Store in Qdrant with metadata (source, text)

### Query Workflow
1. Event: `rag/query_pdf_ai` with question and top_k
2. Embed the query
3. Search Qdrant for most similar chunks
4. Pass context to GPT-4o-mini
5. Return answer with sources and number of contexts used

## Dependencies

Key dependencies are listed in `pyproject.toml`:
- **fastapi**: Web framework
- **inngest**: Event orchestration
- **llama-index**: Document loading and text splitting
- **openai**: LLM and embeddings
- **qdrant-client**: Vector database client
- **streamlit**: Web UI framework
- **uvicorn**: ASGI server

## Development

- The project uses Python 3.13+ with `uv` for dependency management
- Type hints are used throughout with Pydantic models
- Configuration is handled via environment variables

## License

[Add license information here]

## Contributing

[Add contributing guidelines here]