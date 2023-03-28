from dataclasses import dataclass
from Domain.Entity import Entity


@dataclass(init=True)
class Tranzactie(Entity):

    id_masina: str
    id_card_client: str
    suma_piese: float
    suma_manopera: float
    data: str
    ora: str
    discount: float
