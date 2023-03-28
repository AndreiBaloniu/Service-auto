from Domain.Car import Car
from Domain.CarValidator import CarValidator
from Domain.Card_client import Card_client
from Domain.Tranzactie import Tranzactie
from Domain.TranzactieValidator import TranzactieValidator
from Repositories.RepositoryJson import RepositoryJson
from Services.CarService import CarService
from Services.Sorted_clone import sorted_clone
from Services.TranzactieService import TranzactieService
from Services.UndoRedoService import UndoRedoService
from utils import clear_file


def test_undo_redo():
    undo_redo_service = UndoRedoService()

    filename = 'test_undo_redo.json'
    clear_file(filename)
    car_repository = RepositoryJson(filename)
    car_validator = CarValidator()
    car_service = CarService(car_repository,
                             car_validator,
                             undo_redo_service)

    car_id = "1"
    name = "Golf IV"
    an_achizitie = 2000
    nr_km = 30000
    garantie = "da"

    car_service.add(car_id, name, an_achizitie, nr_km, garantie)

    assert len(car_service.get_cars()) == 1

    undo_redo_service.undo()

    assert len(car_service.get_cars()) == 0

    undo_redo_service.redo()

    assert len(car_service.get_cars()) == 1

    car_service.delete("1")

    undo_redo_service.undo()

    assert len(car_service.get_cars()) == 1

    undo_redo_service.redo()

    assert len(car_service.get_cars()) == 0

    undo_redo_service.undo()


def test_sorted_clone():
    random_list = [3, 1, 2]

    ord_list = sorted_clone(random_list, lambda x: x, True)

    assert ord_list == [3, 2, 1]


def test_update_garantie():
    """
    Test pentru actualizarea tuturor garantiilor si
    undo/redo pentru aceeasi functionalitate.
    :return:
    """

    filename = 'test_cars.json'
    clear_file(filename)

    undo_redo_service = UndoRedoService()

    car_repository = RepositoryJson(filename)
    car_validator = CarValidator()
    car_service = CarService(car_repository, car_validator,
                             undo_redo_service)
    added = Car("1", "golf", 2001, 300, "da")

    car_repository.create(added)

    added = Car("2", "audi A4", 2019, 70000, "da")

    car_repository.create(added)

    car_service.update_warranty()

    assert car_repository.read(None) == \
           [
               Car("1", "golf", 2001, 300, "nu"),
               Car("2", "audi A4", 2019, 70000, "nu")
           ]

    undo_redo_service.undo()

    assert car_repository.read(None) == \
           [
               Car("1", "golf", 2001, 300, "da"),
               Car("2", "audi A4", 2019, 70000, "da")
           ]

    undo_redo_service.redo()

    assert car_repository.read(None) == \
           [
               Car("1", "golf", 2001, 300, "nu"),
               Car("2", "audi A4", 2019, 70000, "nu")
           ]


def test_ord_descending_by_the_amount_of_discounts_applied():
    filename = 'test_ord_desc_by_cost_of_labor.json'
    clear_file(filename)

    undo_redo_service = UndoRedoService()

    transaction_repository = RepositoryJson(filename)
    transaction_validator = TranzactieValidator()

    costumer_card_repository = RepositoryJson('test_costumer_card.json')
    clear_file('test_costumer_card.json')

    car_repository = RepositoryJson('test_cars.json')
    clear_file('test_cars.json')

    transaction_service = TranzactieService(transaction_repository,
                                            transaction_validator,
                                            costumer_card_repository,
                                            car_repository,
                                            undo_redo_service
                                            )
    added = Car("1", "Golf IV", 2001, 300, "nu")
    car_repository.create(added)
    added = Car("2", "Audi A5", 20015, 50000, "da")
    car_repository.create(added)
    added = Car("3", "Toyota Avensis", 2020, 1000, "da")
    car_repository.create(added)

    added = Card_client("1", "Popescu", "George", 5020513070025,
                        "13-05-2002", "20-07-2020")
    costumer_card_repository.create(added)

    added = Card_client("2", "Mihai", "Ifrim", 5020513070039,
                        "19-03-2000", "20-06-2020")
    costumer_card_repository.create(added)

    added = Card_client("3", "Iulian", "Marcescu", 5020513090018,
                        "20-10-2001", "20-07-2021")
    costumer_card_repository.create(added)

    added = Tranzactie("1", "1", "1", 421.32, 250, "17.06.2020", "12:23",
                       0)

    transaction_repository.create(added)

    added = Tranzactie("2", "2", "2", 421.32, 400, "17.05.2020", "12:23",
                       0)

    transaction_repository.create(added)

    added = Tranzactie("3", "3", "3", 421.32, 500, "17.05.2020", "12:23",
                       0)

    transaction_repository.create(added)

    assert transaction_service.ord_descending_by_handwork() == \
           [

               Card_client("3", "Iulian", "Marcescu", 5020513090018,
                           "20.10.2001", "20.07.2021"),
               Card_client("2", "Mihai", "Ifrim", 5020513070039,
                           "19.03.2000", "20.06.2020"),
               Card_client("1", "Popescu", "George", 5020513070025,
                           "13.05.2002", "20.07.2020")

           ]


def test_delete_from_interval_of_time():
    """
    Test pentru stergerea tuturor tranzactiilor dintr-un interval si
    undo/redo pentru aceeasi functionalitate.
    :return:
    """

    filename = 'test_ord_desc_by_cost_of_labor.json'
    clear_file('test_ord_desc_by_cost_of_labor.json')

    undo_redo_service = UndoRedoService()

    transaction_repository = RepositoryJson(filename)
    transaction_validator = TranzactieValidator()

    costumer_card_repository = RepositoryJson('test_costumer_card.json')
    clear_file('test_costumer_card.json')

    car_repository = RepositoryJson('test_cars.json')
    clear_file('test_cars.json')

    transaction_service = TranzactieService(transaction_repository,
                                            transaction_validator,
                                            costumer_card_repository,
                                            car_repository,
                                            undo_redo_service
                                            )

    added = Car("1", "Golf IV", 2001, 300, "nu")
    car_repository.create(added)
    added = Car("2", "Audi A5", 20015, 50000, "da")
    car_repository.create(added)
    added = Car("3", "Toyota Avensis", 2020, 1000, "da")
    car_repository.create(added)

    added = Tranzactie("1", "1", "1", 421.32, 250, "17.06.2020", "12:23",
                       0)

    transaction_repository.create(added)

    added = Tranzactie("2", "2", "2", 421.32, 400, "17.05.2020", "12:23",
                       0)

    transaction_repository.create(added)

    added = Tranzactie("3", "3", "3", 421.32, 500, "17.05.2020", "12:23",
                       0)

    transaction_repository.create(added)

    transaction_service.delete_from_interval_of_time("01.01.2000",
                                                     "12.12.2020")
