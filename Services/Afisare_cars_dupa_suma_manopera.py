from Services.CarService import CarService
from Services.Sorted_clone import sorted_clone
from Services.TranzactieService import TranzactieService


class cars_by_handworksum:

    def __init__(self,
                 tranzactie_service: TranzactieService,
                 car_service: CarService):
        self.car_service = car_service
        self.tranzactie_service = tranzactie_service

    def cars_desc_by_handwork(self):
        """
        Ordoneaza tranzactiile descrescator dupa costul manoperei
        :return:
        """

        transactions = self.tranzactie_service.get_transactions()

        transactions_sorted = \
            sorted_clone(transactions,
                         lambda tranzactie: tranzactie.suma_manopera,
                         True)

        return transactions_sorted
