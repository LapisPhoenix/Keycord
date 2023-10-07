from dataclasses import dataclass
from typing import AsyncIterable
from src.api.types import KeycordObject
from src.api.types.channel import GuildChannel
from src.api.http import AHttpClient


@dataclass
class Guild(KeycordObject):
    """
    A Discord Guild/Server
    """

    name: str
    description: str = ""
    owner_id: int = -69
    count_id: int = -69

    async def load_guild_information(self):
        r = await AHttpClient.get(f"/guilds/{self.id}")

        self.description, self.owner_id = (
            r["description"], r["owner_id"]
        )

    async def load_guild_channels(self) -> AsyncIterable[GuildChannel]:
        r = await AHttpClient.get(f"/guilds/{self.id}/channels")

        for channel in filter(lambda c: c["type"] == 0, r):
            yield GuildChannel(
                id=channel["id"], name=channel["name"], messages=[]
            )
