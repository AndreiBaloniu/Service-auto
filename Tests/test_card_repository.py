from Domain.Card_client import Card_client
from Repositories.RepositoryJson import RepositoryJson
from utils import clear_file


def test_card_repository():
    """
    Functie test card repository
    :return:
    """
    filename = 'test_cards.json'
    clear_file(filename)
    card_repository = RepositoryJson(filename)
    added = Card_client('1', 'Baloniu',
                        'Andrei', 1234567890123,
                        '11.06.2002', '12.11.2020')
    card_repository.create(added)
    assert card_repository.read(added.id_entity) == added
