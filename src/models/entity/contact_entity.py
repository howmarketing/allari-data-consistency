from dataclasses import dataclass

@dataclass
class ContactEntity:
    nickname: str
    phone_number: str
    id: int = None
    owner_id: int = None

    def __str__(self):
        return f"{self.nickname} ({self.phone_number})"
