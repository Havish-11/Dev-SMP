from dataclasses import dataclass, field
from typing import Any
from datetime import datetime
import asyncio


@dataclass
class Message:
    sender: str
    recipient: str
    content: Any
    message_type: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class MessageBus:
    def __init__(self):
        self._queues: dict[str, asyncio.Queue] = {}
        self._history: list[Message] = []

    def register(self, agent_name: str):
        if agent_name not in self._queues:
            self._queues[agent_name] = asyncio.Queue()

    async def send(self, message: Message):
        self._history.append(message)
        if message.recipient in self._queues:
            await self._queues[message.recipient].put(message)

    async def receive(self, agent_name: str, timeout: float = 30.0) -> Message:
        queue = self._queues.get(agent_name)
        if not queue:
            raise ValueError(f"Agent '{agent_name}' not registered on message bus")
        return await asyncio.wait_for(queue.get(), timeout=timeout)

    def get_history(self) -> list[Message]:
        return self._history.copy()


# Singleton
message_bus = MessageBus()
