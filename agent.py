import json
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, RunContext, function_tool
from livekit.plugins import (
    groq,
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from prompts import INSTRUCTIONS,WELCOME_MESSAGE
from booking_storage import store_booking
from calendar_storage import create_event
load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=INSTRUCTIONS)

    @function_tool(
        name="store_booking",
        description=(
            "Create a booking after the user CONFIRMS all details. "
            "Args: service(str), date(YYYY-MM-DD), time(HH:MM 24h, America/Chicago). "
            "Returns the saved booking JSON."
        ),
    )
    async def tool_store_booking(
        self,
        context: RunContext,
        service: str,
        date: str,
        time: str,
    ) -> dict:
        booking = store_booking(service=service, date=date, time=time)
        # Keep the LLM informed with a compact, structured response
        return {
            "status": "ok",
            "booking": booking,
            "speak": f"Booked {booking['service']} on {booking['date']} at {booking['time']}."
        }

    @function_tool(
        name="create_calendar_event",
        description=(
            "Schedule the confirmed booking into Google Calendar. "
            "Args: service(str), date(YYYY-MM-DD), time(HH:MM). "
            "Returns the created event JSON."
        ),
    )
    async def tool_create_calendar_event(
        self,
       context: RunContext,
        service: str,
        date: str,
        time: str,
    ) -> dict:
        event = create_event(service=service, date=date, time=time)
        link = event.get("htmlLink", "")
        return {
            "status": "ok",
            "event": event,
            "speak": f"I’ve added {service} on {date} at {time} to your Google Calendar."
        }
    



async def entrypoint(ctx: agents.JobContext):

    session = AgentSession(
        stt=deepgram.STT(model="nova-3", language="multi"),
        llm=groq.LLM(model="llama-3.3-70b-versatile"),
        tts=cartesia.TTS(model="sonic-2", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02"),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(), 
        ),
    )

    await session.generate_reply(
        instructions=WELCOME_MESSAGE
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))

