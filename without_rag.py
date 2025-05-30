import asyncio
import logging
from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import JobContext, WorkerOptions, cli
from livekit.agents.llm import (
    ChatContext,
    ChatMessage,
)
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import deepgram, openai, silero

logging.basicConfig(level=logging.DEBUG)
load_dotenv(dotenv_path=".env.local")

# The code snippet is reading the content of a text file located at
# your folder and storing it in the variable `prompt_data`. The
# `strip()` method is used to remove any leading or trailing whitespaces or newline characters from
# the content read from the file.
prompt_file = "UPLOAD PROMPT FILE"
with open(prompt_file, 'r') as file:
    prompt_data = file.read().strip()

prompt = prompt_data



async def entrypoint(ctx: JobContext):
    """
    This Python async function sets up a voice assistant for a chat room, greets users, and waits for
    messages while connected.
    
    :param ctx: The `ctx` parameter in the `entrypoint` function seems to be an instance of
    `JobContext`. It is used to manage the context of the job being executed, including connecting to a
    room and handling messages within that room. The `ctx` object likely contains information about the
    room, such
    :type ctx: JobContext
    """

    await ctx.connect()
    print(f"Connected to room: {ctx.room.name}")

    initial_ctx = ChatContext(
        messages=[
            ChatMessage(
                role="system",
                content=(prompt
                ),
            )
        ]
    )


    assistant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=deepgram.STT(),
        llm=openai.LLM(model="gpt-4o-mini"),
        chat_ctx=initial_ctx,
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