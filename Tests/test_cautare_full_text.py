from Domain.Card_client import Card_client
from Domain.CardValidator import CardValidator
from Domain.Car import Car
from Domain.CarValidator import CarValidator

from Repositories.RepositoryJson import RepositoryJson
from Services.CarService import CarService
from Services.Cautare_full_text import Search
from Services.CardService import CardService
from Services.UndoRedoService import UndoRedoService
from utils import clear_file


def test_cautare_text():
    filename_car = 'test_car_repository.json'
    clear_file(filename_car)
    filename_card = 'test_card_repository.json'
    clear_file(filename_card)

    undo_redo_service = UndoRedoService()
    car_repository = RepositoryJson(filename_car)
    car_validator = CarValidator()
    car_service = CarService(car_repository, car_validator, undo_redo_service)

    card_repository = RepositoryJson(filename_card)
    card_validator = CardValidator()
    card_service = CardService(card_repository, card_validator,
                               undo_redo_service)

    car = Car('1', 'Dacia Logan', 2018, 20000, 'da')
    car_repository.create(car)

    card = Card_client('1', 'Baloniu', 'Andrei', 1234567890111,
                       '11.06.2002', '22.07.2021')
    card_repository.create(card)

    cautare = Search(car_service, card_service)
    assert cautare.search_full_text('a') == {'masini': [car],
                                             'carduri': [card]}
    assert cautare.search_full_text('1') == {'masini': [car],
                                             'carduri': [card]}
