from dataclasses import dataclass, field
from typing import List
from .experience_entity import ExperienceEntity
from .contact_entity import ContactEntity

@dataclass
class PersonEntity:
    id: int = None
    first_name: str = ""
    last_name: str = ""
    phone: str = ""
    experiences: List[ExperienceEntity] = field(default_factory=list)
    contacts: List[ContactEntity] = field(default_factory=list)

    def add_experience(self, experience: ExperienceEntity):
        experience.person_id = self.id
        self.experiences.append(experience)

    def add_contact(self, contact: ContactEntity):
        contact.owner_id = self.id
        self.contacts.append(contact)

    def __str__(self):
        experiences_str = "\n".join(str(exp) for exp in self.experiences)
        contacts_str = "\n".join(str(contact) for contact in self.contacts)
        return f"{self.first_name} {self.last_name} ({self.phone})\n\nExperiences:\n{experiences_str}\n\nContacts:\n{contacts_str}"
