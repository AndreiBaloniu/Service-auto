from Domain.Tranzactie import Tranzactie
from Repositories.RepositoryJson import RepositoryJson
from utils import clear_file


def test_tranzactie_repository():
    """
    Functie test tranzactie repository
    :return:
    """
    filename = 'test_tranzactii.json'
    clear_file(filename)
    tranzactie_repository = RepositoryJson(filename)
    added = Tranzactie('1', '1', '1',
                       200, 250,
                       '11.10.2020', '15:51', 0)
    tranzactie_repository.create(added)
    assert tranzactie_repository.read(added.id_entity) == added
