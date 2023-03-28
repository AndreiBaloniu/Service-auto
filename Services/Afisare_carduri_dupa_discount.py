from Services.CardService import CardService
from Services.Sorted_clone import sorted_clone
from Services.TranzactieService import TranzactieService


class card_by_discount:

    def __init__(self,
                 card_service: CardService,
                 tranzactie_service: TranzactieService):
        self.card_service = card_service
        self.tranzactie_service = tranzactie_service

    def cards_by_discount(self):
        """
        Ordoneaza tranzactiile dupa cantitatea de reduceri aplicata
        :return:
        """

        transactions = self.tranzactie_service.get_transactions()

        transactions_with_card = []
        costumer_card_discount = []

        for tranzactie in transactions:

            if tranzactie.id_card_client is not None:

                transactions_with_card.append(tranzactie)

        transactions_with_card = sorted_clone(transactions_with_card,
                                              lambda trans:
                                              (10*tranzactie.suma_manopera)/9,
                                              True
                                              )

        for tranzactie in transactions_with_card:

            costumer_card_discount.append(self.card_service.
                                          get_card
                                          (tranzactie.id_card_client))

        return costumer_card_discount
