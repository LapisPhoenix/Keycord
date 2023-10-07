from dataclasses import dataclass
from src import client
from src.api.types import KeycordObject
from src.api.types.user import User


@dataclass
class Message(KeycordObject):
    """
    A Discord Message
    """
    author: User
    content: str
    timestamp: str
    date: str

    @property
    def _content(self) -> str:
        return self.content

    def display(self):
        # TODO: Add color to author messages

        is_capped = True if self.author == client.user else False

        message = (
            f"{self.author.username.upper() if is_capped else self.author.username}"
            f"Posted {self.date} at {self.timestamp}"
            f"\n{self.content}\n"   # * Might need to change this
        )

        return message
