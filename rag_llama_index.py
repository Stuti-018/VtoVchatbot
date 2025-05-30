import asyncio
from typing import Annotated
import os
import logging
from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import JobContext, WorkerOptions, cli, tokenize, tts
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import deepgram, silero, llama_index
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine.types import ChatMode
from llama_index.llms.openai import OpenAI
from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)

logging.basicConfig(level=logging.DEBUG)
load_dotenv(dotenv_path=".env.local")

# Initialize RAG components
# The code snippet you provided is responsible for initializing the knowledge storage directory and
# loading the knowledge index. Here's a breakdown of what it does:
PERSIST_DIR = "./knowledge-storage"
if not os.path.exists(PERSIST_DIR):
    # Load knowledge documents and create index
    documents = SimpleDirectoryReader("rag_data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # Load existing knowledge index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

# The code snippet you provided is reading the contents of a text file located at
# your folder and storing the content in the variable
# `prompt_data`. The `strip()` method is used to remove any leading or trailing whitespaces or newline
# characters from the text read from the file.
prompt_file = "UPLOAD PROMPT FILE"
with open(prompt_file, 'r') as file:
    prompt_data = file.read().strip()

prompt = prompt_data


# The code snippet you provided is setting up a conversational chat engine using the RAG
# (Retrieval-Augmented Generation) model from OpenAI. Here's a breakdown of what each component is
# doing:
llm = OpenAI(model="gpt-4o-mini", temperature=0)
memory = ChatMemoryBuffer.from_defaults(token_limit=15000)
hih_query_engine = index.as_chat_engine(use_async=True,
                                            chat_mode=ChatMode.CONTEXT,
                                            llm=llm,
                                            memory=memory,
                                            system_prompt=(prompt),
                                            similarity_top_k=5,)



async def entrypoint(ctx: JobContext):
    """
    This Python async function sets up a voice assistant for a chat room, greets users, and waits for
    messages while connected.
    :param ctx: The `ctx` parameter in the `entrypoint` function is of type `JobContext`. It is used to
    provide context and information related to the job being executed. In this case, it is used to
    establish a connection to a room, access the room's name, and manage the conversation with
    :type ctx: JobContext
    """

    await ctx.connect()
    print(f"Connected to room: {ctx.room.name}")

    combined_llm = llama_index.LLM(
        chat_engine=hih_query_engine
    )

    assistant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=deepgram.STT(),
        llm=combined_llm,
        tts=deepgram.TTS(),
    )

    assistant.start(ctx.room)
    await assistant.say("""Hello! I'm Health Assistant of Tata One MG. How can I help you today?""", allow_interruptions=True)
    logging.info("Greeting message sent.")

    while ctx.room.connection_state == rtc.ConnectionState.CONN_CONNECTED:
        logging.info("Waiting for messages...")
        await asyncio.sleep(1)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))