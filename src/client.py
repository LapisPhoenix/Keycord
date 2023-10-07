from typing import AsyncIterable, Optional, Generator
from src.api.http import AHttpClient
from src.api.types import KeycordID
from src.api.types.user import User
from src.api.types.guild import Guild
from src.api.types.channel import MessageChannel, Channel


class Client:
    """
    A (very) simple Discord API wrapper
    """

    def __init__(self, token: str):
        self.selected_channel: Optional[Channel] = None
        self.selected_guild: Optional[Guild] = None
        self.token = token
        self.user = None

    def initalize(self):
        try:
            self.user = self.__user
        except KeyError:
            return False
        return True

    async def guilds_sync(self) -> AsyncIterable[Guild]:
        r = await AHttpClient.get("/users/@me/guilds")

        for guild in r:
            yield Guild(id=guild["id"], name=guild["name"])

    async def channels_sync(self) -> AsyncIterable[MessageChannel]:
        r = await AHttpClient.get("/users/@me/channels")

        for channel in filter(lambda c: len(c["recipients"]) == 1, r):
            user = User(
                id=channel["recipients"][0]["id"],
                username=channel["recipients"][0]["username"],
                discriminator=channel["recipients"][0]["discriminator"] if channel["recipients"][0]["discriminator"] else 0
            )

            last_message_id = channel["last_message_id"] or KeycordID(0)

            yield MessageChannel(
                id=channel["id"],
                recipient=user,
                messages=[],
                last_message_id=last_message_id
            )
