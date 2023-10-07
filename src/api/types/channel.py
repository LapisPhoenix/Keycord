import re
from dataclasses import dataclass
from typing import AsyncIterable, List
from src.api.types import KeycordObject, KeycordID
from src.api.types.user import User
from src.api.types.message import Message
from src.api.http import AHttpClient


TIME_PATTERN = r"(?P<date>\d{4}\-\d{2}\-\d{2})T(?P<hour>\d{2}\:\d{2}\:\d{2})"


@dataclass
class Channel(KeycordObject):
    messages: List[Message]

    def __init__(self):
        if isinstance(self.__class__, (GuildChannel, MessageChannel)):
            raise NotImplementedError(f'You cant create this class')

    async def send_message(self, content: str):
        """
        Send a message to a current channel
        :param content: Message Content
        :return:
        """
        await AHttpClient.post(
            f"channels/{self.id}/messages", data={"content": content}
        )

    async def load_messages(self, limit: int = 100) -> AsyncIterable[Message]:
        """
        Load Channel Messages
        :param limit: Number of messages to load
        :return:
        """

        r = await AHttpClient.get(f"channels/{self.id}/messages?limit={limit}")

        try:
            if r["code"] == 50001:
                yield "You don't have permission to view this channel."

            return
        except TypeError:
            pass

        for message in r:
            author = User(
                id=message["author"]["id"],
                username=message["author"]["username"],
                discriminator=message["author"]["discriminator"] if message["author"]["discriminator"] else 0
            )

            raw_timestamp = message["timestamp"]

            parsed_timestamp = re.search(TIME_PATTERN, raw_timestamp)

            if parsed_timestamp is None:
                continue

            yield Message(
                id=message["id"],
                author=author,
                timestamp=parsed_timestamp.group("hour"),
                date=parsed_timestamp.group("date"),
                content=message["content"]
            )


@dataclass
class MessageChannel(Channel):
    recipient: User
    last_message_id: KeycordID


@dataclass
class GuildChannel(Channel):
    name: str

    allow_reading: bool = True
    allow_writing: bool = True
