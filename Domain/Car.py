from dataclasses import dataclass
from Domain.Entity import Entity


@dataclass(init=True)
class Car(Entity):

    nume: str
    an_achizitie: int
    nr_km: float
    garantie: str
