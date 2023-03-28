from datetime import datetime

from Domain.AddOperation import AddOperation
from Domain.DeleteOperation import DeleteOperation
from Domain.Tranzactie import Tranzactie
from Domain.TranzactieValidator import TranzactieValidator
from Domain.UpdateOperation import UpdateOperation
from Repositories.Exceptions import NoSuchIdError
from Repositories.Repository import Repository
from Services.Sorted_clone import sorted_clone
from Services.UndoRedoService import UndoRedoService


class TranzactieService:

    def __init__(self,
                 tranzactieRepository: Repository,
                 tranzactieValidator: TranzactieValidator,
                 carRepository: Repository,
                 cardRepository: Repository,
                 undo_redo_service: UndoRedoService
                 ):
        self.tranzactieValidator = tranzactieValidator
        self.tranzactieRepository = tranzactieRepository
        self.carRepository = carRepository
        self.cardRepository = cardRepository
        self.undo_redo_service = undo_redo_service

    def add(self, id: str, id_masina: str,
            id_card_client: str,
            suma_piese: float,
            suma_manopera: float,
            data: str,
            ora: str,
            discount: float
            ):
        """
        Functie adaugare tranzactie
        :param id: id-ul tranzactiei
        :param id_masina: id-ul masinii
        :param id_card_client: id-ul cardului clientului
        :param suma_piese: suma pieselor
        :param suma_manopera: suma manoperei
        :param data: data
        :param ora: ora
        :param discount: discount-ul aplicat
        :return:
        """

        car = self.carRepository.read(id_masina)
        if id_card_client != 'none':
            card = self.cardRepository.read(id_card_client)
            if id_card_client is None:
                raise NoSuchIdError('Nu exista un card cu acest id!')

        if car is None:
            raise NoSuchIdError('Nu exista o masina cu acest id!')

        if car.garantie == 'da':
            discount = discount + suma_piese
            suma_piese = 0

        if id_card_client is not None:
            discount = discount + suma_manopera / 10
            suma_manopera = suma_manopera - suma_manopera / 10

        tranzactie = Tranzactie(id,
                                id_masina,
                                id_card_client,
                                suma_piese,
                                suma_manopera,
                                data,
                                ora,
                                discount)
        self.tranzactieValidator.validate(tranzactie)
        self.tranzactieRepository.create(tranzactie)

        self.undo_redo_service.clear_redo_list()
        tranz_add_op = AddOperation(self.tranzactieRepository, tranzactie)
        self.undo_redo_service.add_operation(tranz_add_op)

    def update(self, id: str, id_masina: str,
               id_card_client: str,
               suma_piese: float,
               suma_manopera: float,
               data: str, ora: str, discount: float):
        """
        Functie update tranzactie
        :param id: id-ul tranzactiei
        :param id_masina: id-ul masinii
        :param id_card_client: id-ul cardului clientului
        :param suma_piese: suma pieselor
        :param suma_manopera: suma manoperei
        :param data: data
        :param ora: ora
        :param discount: discount-ul aplicat
        :return:
        """

        car = self.carRepository.read(id_masina)
        if id_card_client is not None:
            card = self.cardRepository.read(id_card_client)
            if card is None:
                pass
                raise NoSuchIdError('Nu exista acest id de card!')

        if car.garantie == 'da':
            discount = discount + suma_piese
            suma_piese = 0

        if id_card_client is not None:
            discount = discount + suma_manopera / 10
            suma_manopera = suma_manopera - suma_manopera / 10

        tranz_before_update = self.get_transaction(id)
        tranzactie = Tranzactie(id,
                                id_masina,
                                id_card_client,
                                suma_piese,
                                suma_manopera,
                                data,
                                ora,
                                discount)
        self.tranzactieValidator.validate(tranzactie)
        self.tranzactieRepository.create(tranzactie)
        tranz_update_op = UpdateOperation(self.carRepository,
                                          tranz_before_update,
                                          tranzactie)
        self.undo_redo_service.clear_redo_list()
        self.undo_redo_service.update_operation(tranz_update_op)

    def delete(self, id: str):
        """
        Functie delete tranzactie
        :param id: id-ul tranzactiei ce trebuie stearsa
        :return:
        """
        tranzactie = self.tranzactieRepository.read(id)
        self.tranzactieRepository.delete(id)

        tranz_del_op = DeleteOperation(self.tranzactieRepository, tranzactie)
        self.undo_redo_service.clear_redo_list()
        self.undo_redo_service.delete_operation(tranz_del_op)

    def get_transactions(self):
        """
        Functie afisare toate tranzactii
        :return:
        """
        return self.tranzactieRepository.read()

    def get_transaction(self, id: str):
        """
        Functie afisare o tranzactie
        :param id: id-ul tranzactiei dorite a fi afisata
        :return:
        """
        return self.tranzactieRepository.read(id)

    def all_transactions_from_an_interval(self, start: float, finish: float,
                                          tranzactii: list,
                                          transactions_list: list, index: int):
        """
        Returneaza o lista formata din tranzactiile cu suma totala a costurilor
        aflata intr-un interval
        :param start: capatul inferior al intervalului
        :param finish: capatul superior al intervalului
        :return:
        """

        if index in range(len(tranzactii)):

            if start < tranzactii[index].suma_manopera + \
                    tranzactii[index].suma_piese < finish:
                transactions_list.append(tranzactii[index])

            return self.all_transactions_from_an_interval(start, finish,
                                                          tranzactii,
                                                          transactions_list,
                                                          index + 1)
        else:
            return transactions_list

    def delete_from_interval_of_time(self, date_1: str, date_2: str):

        """
        Sterge toate tranzactiile dintr-un interval de timp
        :param date_1:
        :param date_2:
        :return:
        """
        transactions = self.tranzactieRepository.read(None)

        date_1 = datetime.strptime(date_1, '%d.%m.%Y')
        date_1 = datetime.date(date_1)
        date_2 = datetime.strptime(date_2, '%d.%m.%Y')
        date_2 = datetime.date(date_2)

        operations = []

        self.undo_redo_service.clear_redo_list()

        for transaction in transactions:

            transaction_date = datetime.strptime(transaction.data,
                                                 '%d.%m.%Y')
            transaction_date = datetime.date(transaction_date)

            if date_1 < transaction_date < date_2:
                transaction_op = AddOperation(self.tranzactieRepository,
                                              transaction)
                operations.append(transaction_op)
                self.tranzactieRepository.delete(transaction.id_entity)
                self.undo_redo_service.delete_from_interval_of_time(operations)

    def ord_descending_by_handwork(self):
        """
        Ordoneaza tranzactiile descrescator dupa costul manoperei
        :return:
        """

        transactions = self.get_transactions()

        transactions_sorted = \
            sorted_clone(transactions,
                         lambda tranzactie: tranzactie.suma_manopera,
                         True)

        return transactions_sorted
