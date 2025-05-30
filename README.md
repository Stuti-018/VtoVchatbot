# LiveKit Voice Assistant with RAG Support

A real-time voice assistant built with LiveKit that supports both RAG (Retrieval-Augmented Generation) and standard conversation modes. The assistant is specifically configured as a Health Assistant for Tata One MG.

## Features

- **Real-time Voice Interaction**: Uses LiveKit for real-time audio streaming
- **Dual Mode Operation**: 
  - RAG-enabled mode with document retrieval using LlamaIndex
  - Standard conversation mode without RAG
- **Advanced Speech Processing**: 
  - Speech-to-Text via Deepgram
  - Text-to-Speech via Deepgram
  - Voice Activity Detection via Silero
- **AI-Powered Responses**: OpenAI GPT-4o-mini integration
- **Document Knowledge Base**: Pre-loaded with health-related documentation

## Project Structure

```
├── rag_llama_index.py     # Main RAG-enabled voice assistant
├── without_rag.py         # Standard voice assistant without RAG
├── requirement.txt        # Python dependencies
├── .env.local            # Environment variables (create from env_example.txt)
├── env_example.txt       # Environment variables template
├── prompt.txt            # System prompt configuration
├── rag_data/             # Knowledge base documents (clinicians-guide-to-laboratory-medicine)
│   ├── cglm_chapter1.txt
│   ├── cglm_chapter2.txt
│   └── ... (chapters 1-9)
├── rag_data.zip          # Compressed knowledge base
└── knowledge-storage/    # Vector index storage (auto-generated)
```

## Prerequisites

- Python 3.11
- LiveKit server access
- OpenAI API key
- Deepgram API key

## Installation

1. **Clone the repository** (or ensure you're in the project directory)

2. **Install dependencies**:
   ```bash
   pip install -r requirement.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp env_example.txt .env.local
   ```
   
   Edit `.env.local` with your actual API keys:
   ```
   LIVEKIT_URL=your_livekit_server_url
   LIVEKIT_API_KEY=your_api_key
   LIVEKIT_API_SECRET=your_api_secret
   OPENAI_API_KEY=your_openai_api_key
   DEEPGRAM_API_KEY=your_deepgram_api_key
   ```

4. **Prepare the prompt file**:
   - Update the `prompt_file` variable in both Python files to point to your actual prompt file
   - Currently set to `"UPLOAD PROMPT FILE"` - replace with your actual file path

## Usage

### RAG-Enabled Mode (Recommended)

Run the RAG-enabled voice assistant that can answer questions based on the knowledge base:

```bash
python rag_llama_index.py
```

**Features:**
- Access to document knowledge base in `rag_data/`
- Vector similarity search with top-k=5
- Chat memory buffer (15,000 tokens)
- Context-aware responses

### Standard Mode

Run the basic voice assistant without RAG capabilities:

```bash
python without_rag.py
```

**Features:**
- Direct OpenAI GPT interaction
- No document retrieval
- Simpler conversation flow

## How It Works

### RAG Mode (`rag_llama_index.py`)

1. **Knowledge Base Setup**: 
   - Loads documents from `rag_data/` directory
   - Creates/loads vector index for similarity search
   - Persists index in `knowledge-storage/` directory

2. **Chat Engine Configuration**:
   - Uses OpenAI GPT-4o-mini model
   - Implements context-based chat mode
   - Maintains conversation memory
   - Retrieves relevant documents for context

3. **Voice Assistant Pipeline**:
   - Voice Activity Detection → Speech-to-Text → LLM Processing → Text-to-Speech

### Standard Mode (`without_rag.py`)

1. **Direct LLM Integration**: Uses OpenAI directly without document retrieval
2. **Simpler Chat Context**: Basic system prompt without RAG enhancement
3. **Same Voice Pipeline**: Identical audio processing chain

## Key Dependencies

- **LiveKit**: Real-time communication framework
- **LlamaIndex**: RAG and document indexing
- **OpenAI**: Language model API
- **Deepgram**: Speech-to-Text and Text-to-Speech
- **Silero**: Voice Activity Detection

## Configuration

### Customizing the Assistant

1. **Update System Prompt**: Modify the prompt file referenced in the Python scripts
2. **Add Knowledge Documents**: Place new documents in the `rag_data/` directory
3. **Adjust RAG Parameters**: Modify `similarity_top_k`, `temperature`, and memory settings
4. **Change Greeting**: Update the greeting message in the `entrypoint` function

### Performance Tuning

- **Token Limit**: Adjust `token_limit` in `ChatMemoryBuffer`
- **Similarity Search**: Modify `similarity_top_k` for more/fewer retrieved documents
- **Model Selection**: Change the OpenAI model in the `OpenAI()` constructor

## Troubleshooting

1. **Connection Issues**: Verify LiveKit server URL and credentials
2. **API Errors**: Check OpenAI and Deepgram API keys and quotas
3. **Audio Problems**: Ensure proper microphone/speaker setup
4. **Knowledge Base**: Verify documents are in `rag_data/` directory
5. **Missing Prompt**: Update `prompt_file` variable to point to actual prompt file

## Development

To extend the assistant:

1. **Add New Knowledge**: Place documents in `rag_data/` and restart
2. **Modify Responses**: Update the system prompt
3. **Change Voice Settings**: Adjust TTS/STT configurations
4. **Add Features**: Extend the `entrypoint` function
