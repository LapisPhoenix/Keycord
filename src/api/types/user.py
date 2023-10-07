from dataclasses import dataclass
from src.api.types import KeycordObject


@dataclass
class User(KeycordObject):
    """
    Discord User
    """
    username: str
    # Since discord is removing discriminators it is (usually) represented with #0
    # We can account for that.

    discriminator: int = None   # * When Discord eventually fully removes this, remove it from here

    discriminator = None if discriminator is None or discriminator == 0 else discriminator

    def __str__(self) -> str:
        return f"{self.username}" + f"#{self.discriminator}" if self.discriminator else ''
