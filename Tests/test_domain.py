from Domain.Car import Car
from Domain.Card_client import Card_client
from Domain.Tranzactie import Tranzactie


def test_car_domain():
    """
    Functie test domain car
    """
    car = Car('1',
              'bmw',
              2016,
              40000,
              'da')

    assert car.id_entity == '1'
    assert car.nume == 'bmw'
    assert car.an_achizitie == 2016
    assert car.nr_km == 40000
    assert car.garantie == 'da'


def test_card_domain():
    """
    Functie test domain card
    """
    card_client = Card_client('1',
                              'Baloniu',
                              'Andrei',
                              1234567890111,
                              '11.05.2016',
                              '05.02.2021')

    assert card_client.id_entity == '1'
    assert card_client.nume == 'Baloniu'
    assert card_client.prenume == 'Andrei'
    assert card_client.CNP == 1234567890111
    assert card_client.data_nasterii == '11.05.2016'
    assert card_client.data_inregistrarii == '05.02.2021'


def test_tranzactie_domain():
    """
    Functie test domain tranzactie
    """
    trazactie = Tranzactie('1',
                           '1',
                           '1',
                           1000,
                           1000,
                           '12.12.2012',
                           '12:12:12',
                           0)

    assert trazactie.id_entity == '1'
    assert trazactie.id_masina == '1'
    assert trazactie.id_card_client == '1'
    assert trazactie.suma_piese == 1000
    assert trazactie.suma_manopera == 1000
    assert trazactie.data == '12.12.2012'
    assert trazactie.ora == '12:12:12'


def all_tests_domain():
    """
    Funcite test tot domain-ul
    """
    test_car_domain()
    test_card_domain()
    test_tranzactie_domain()
