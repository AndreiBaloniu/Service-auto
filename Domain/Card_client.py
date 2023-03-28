from dataclasses import dataclass
from Domain.Entity import Entity


@dataclass(init=True)
class Card_client(Entity):

    nume: str
    prenume: str
    CNP: int
    data_nasterii: str
    data_inregistrarii: str
