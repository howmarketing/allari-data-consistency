from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class ExperienceEntity:
    id: int
    title: str
    company: str
    person_id: int
    start_date: datetime
    end_date: Optional[datetime] = None

    def __str__(self):
        start = datetime.strptime(self.start_date, '%Y-%m-%d')
        end = datetime.strptime(self.end_date, '%Y-%m-%d') if self.end_date else "Present"
        self.start_date = start;
        self.end_date = end if type(end) == datetime else None
        return f"{self.title} at {self.company} ({self.start_date.strftime('%Y-%m-%d')} - {end})"
