import os
import json
from groq import Groq
from utils.message_bus import MessageBus, Message, message_bus


class BaseAgent:
    """Base class for all agents. Uses Groq instead of Google Gemini."""

    # Groq's fast open-source model — change to "llama-3.3-70b-versatile"
    # for higher quality or "mixtral-8x7b-32768" for longer context needs.
    MODEL = "llama-3.1-8b-instant"

    def __init__(self, name: str, bus: MessageBus = message_bus):
        self.name = name
        self.bus = bus
        self.bus.register(name)
        self._client = Groq(api_key=os.environ["GROQ_API_KEY"])

    def _chat(self, system: str, user: str, temperature: float = 0.2) -> str:
        """Send a chat completion request to Groq and return the text response."""
        response = self._client.chat.completions.create(
            model=self.MODEL,
            max_tokens=4096,        # increased from 1000 to prevent truncation
            temperature=temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        choice = response.choices[0]
        if choice.finish_reason == "length":
            raise RuntimeError(
                f"[{self.name}] Response was cut off (finish_reason=length). "
                "Try switching to llama-3.3-70b-versatile in base_agent.py."
            )
        return choice.message.content.strip()

    def _chat_json(self, system: str, user: str, temperature: float = 0.1) -> dict:
        """Like _chat but parses the response as JSON. Strips markdown fences."""
        raw = self._chat(system, user, temperature)
        # Strip ```json ... ``` fences if the model wraps its output
        clean = raw.strip()
        if clean.startswith("```"):
            clean = clean.split("```", 2)[1]
            if clean.startswith("json"):
                clean = clean[4:]
            if clean.endswith("```"):
                clean = clean[:-3]
        clean = clean.strip()
        # If the JSON is still somehow truncated, attempt a best-effort close
        try:
            return json.loads(clean)
        except json.JSONDecodeError:
            # Close any open array or object so json.loads has a chance
            open_braces  = clean.count("{") - clean.count("}")
            open_brackets = clean.count("[") - clean.count("]")
            clean += "}" * max(open_braces, 0) + "]" * max(open_brackets, 0)
            return json.loads(clean)

    async def send(self, recipient: str, content, message_type: str):
        await self.bus.send(Message(
            sender=self.name,
            recipient=recipient,
            content=content,
            message_type=message_type,
        ))

    async def receive(self, timeout: float = 30.0) -> Message:
        return await self.bus.receive(self.name, timeout=timeout)
