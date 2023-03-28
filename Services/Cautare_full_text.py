from Services.CarService import CarService
from Services.CardService import CardService


class Search:
    def __init__(self, car_service: CarService,
                 card_service: CardService):
        self.car_service = car_service
        self.card_service = card_service

    def search_full_text(self, text):
        """
        Cautare text dat in lista de masini si de carduri
        :param text:
        :return:
        """
        cars_cautate = self.cautare_cars(text)
        cards_cautate = self.cautare_cards(text)
        return {"masini": cars_cautate, "carduri": cards_cautate}

    def cautare_cars(self, text):
        """
        Cautare text dat in lista de masini
        :param text:
        :return:
        """
        cars = self.car_service.get_cars()

        searched_cars = []
        for car in cars:
            if text in car.nume or text in str(car.nr_km) \
                    or text in str(car.an_achizitie):
                searched_cars.append(car)
        return searched_cars

    def cautare_cards(self, text):
        """
        Cautare text dat in lista de carduri
        :param text:
        :return:
        """

        cards = self.card_service.get_cards()

        searched_cards = []
        for card in cards:
            if text in card.nume or text in card.prenume \
                    or text in str(card.CNP) or text in card.data_nasterii \
                    or text in card.data_inregistrarii:
                searched_cards.append(card)

        return searched_cards
