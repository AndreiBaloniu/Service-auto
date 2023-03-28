from Domain.Tranzactie import Tranzactie
from Domain.TranzactieValidator import TranzactieValidator
from Repositories.RepositoryJson import RepositoryJson
from Services.TranzactieService import TranzactieService
from Services.UndoRedoService import UndoRedoService
from utils import clear_file


def test_cars_by_handwork_sum():
    """
    Functie test pentru masini dupa suma manopera
    :return:
    """
    filename_car = 'test_car_by_handwork.json'
    clear_file(filename_car)
    car_repository = RepositoryJson(filename_car)
    undo_redo_service = UndoRedoService()

    filename_card = 'test_clientcard_for_cars_by_handwork.json'
    clear_file(filename_card)
    clientcard_repository = RepositoryJson(filename_card)

    transaction_validator = TranzactieValidator()
    filename_tranz = 'st_transaction_for_cars_by_handwork.json'
    clear_file(filename_tranz)
    transaction_repository = \
        RepositoryJson(filename_tranz)

    transaction_service = TranzactieService(transaction_repository,
                                            transaction_validator,
                                            car_repository,
                                            clientcard_repository,
                                            undo_redo_service)

    added = Tranzactie('100',
                       '100',
                       'none',
                       1000,
                       1000,
                       '12.12.2016',
                       '12:00',
                       0)

    transaction_repository.create(added)

    added = Tranzactie('200',
                       '200',
                       'none',
                       1000,
                       1200,
                       '12.12.2015',
                       '14:12',
                       0)

    transaction_repository.create(added)

    added = Tranzactie('300',
                       '300',
                       'none',
                       1000,
                       900,
                       '12.12.2021',
                       '15:15',
                       0)

    transaction_repository.create(added)

    assert transaction_service.ord_descending_by_handwork() == \
           [
               Tranzactie('200',
                          '200',
                          'none',
                          1000,
                          1200,
                          '12.12.2015',
                          '14:12',
                          0),
               Tranzactie('100',
                          '100',
                          'none',
                          1000,
                          1000,
                          '12.12.2016',
                          '12:00',
                          0),
               Tranzactie('300',
                          '300',
                          'none',
                          1000,
                          900,
                          '12.12.2021',
                          '15:15',
                          0)
           ]
