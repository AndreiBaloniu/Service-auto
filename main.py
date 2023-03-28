from Domain.CarValidator import CarValidator
from Domain.CardValidator import CardValidator

from Domain.TranzactieValidator import TranzactieValidator
from Repositories.RepositoryJson import RepositoryJson

from Services.CarService import CarService
from Services.CardService import CardService
from Services.TranzactieService import TranzactieService
from Services.Cautare_full_text import Search
from Services.Random_generator import Generator
from Services.Afisare_cars_dupa_suma_manopera import cars_by_handworksum
from Services.Afisare_carduri_dupa_discount import card_by_discount
from Services.Delete_cascada import Delete_Cascada
from Services.UndoRedoService import UndoRedoService

from UserInterface.Console import Console

from Tests.test_car_repository import test_car_repository
from Tests.test_card_repository import test_card_repository
from Tests.test_tranzacitie_repository import test_tranzactie_repository
from Tests.test_domain import all_tests_domain
from Tests.test_cautare_full_text import test_cautare_text
from Tests.test_Cars_By_Handwork import test_cars_by_handwork_sum
from Tests.tests import test_sorted_clone, test_undo_redo, \
    test_update_garantie, test_delete_from_interval_of_time


def main():
    undo_redo_service = UndoRedoService()

    car_repository = RepositoryJson('cars.json')
    car_validator = CarValidator()
    car_service = CarService(car_repository,
                             car_validator,
                             undo_redo_service)

    card_repository = RepositoryJson('card.json')
    card_validator = CardValidator()
    card_service = CardService(card_repository,
                               card_validator,
                               undo_redo_service)

    tranzactie_repository = RepositoryJson('tranzactie.json')
    tranzactie_validator = TranzactieValidator()
    tranzactie_service = TranzactieService(tranzactie_repository,
                                           tranzactie_validator,
                                           car_repository, card_repository,
                                           undo_redo_service)
    generator = Generator()
    search = Search(car_service, card_service)
    cars_by_handork_sum = cars_by_handworksum(tranzactie_service, car_service)
    cc_by_discount = card_by_discount(card_service, tranzactie_service)
    delete_cas = Delete_Cascada(car_repository, car_service,
                                tranzactie_repository,
                                tranzactie_service, undo_redo_service)
    console = Console(car_service, card_service, tranzactie_service, search,
                      generator, cars_by_handork_sum, cc_by_discount,
                      delete_cas, undo_redo_service)
    console.run_console()


if __name__ == '__main__':
    all_tests_domain()
    test_car_repository()
    test_card_repository()
    test_tranzactie_repository()
    test_cautare_text()
    test_cars_by_handwork_sum()
    test_sorted_clone()
    test_undo_redo()
    test_update_garantie()
    test_delete_from_interval_of_time()
    main()
