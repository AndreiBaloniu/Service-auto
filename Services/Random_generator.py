import random
import jsonpickle


class Generator:

    def generate_id(self) -> str:
        """
        Aceasta functie creeaza un id random pt fiecare masina
        :return:
        """
        file = open("cars.json")
        json_str = file.read()
        list = []
        try:
            cars = jsonpickle.decode(json_str)
            for i in cars.keys():
                list.append(cars[i].id_entity)
        except Exception:
            pass

        file.close()

        while True:
            id = str(random.randint(1, 150))
            if id in list:
                continue
            else:
                return id

    def generate_nume(self) -> str:
        """
        Aceasta functie alege un nume random dintr-o lista predefinita
        :return:
        """
        nume_posibile = ['Mercedes', 'Dacia', 'Porsche',
                         'Lamborghini', 'BMW', 'WW',
                         'Audi', 'Ford',
                         'Hyundai', 'Fiat']
        return random.choice(nume_posibile)

    def generate_an(self) -> int:
        """
        Aceasta functie alege un an random dintr-o lista predefinita
        :return:
        """

        an_posible = [2012, 2013, 2014, 2015,
                      2016, 2017, 2018, 2019,
                      2020, 2021]
        return random.choice(an_posible)

    def generate_km(self) -> float:
        """
        Aceasta functie alege un numare de km random dintr-o lista predefinita
        :return:
        """
        km_posible = [12342.0, 10000.0, 250.0, 0, 5004.0, 300213.0,
                      100, 25000.0, 75000.0, 99.0, 14234.0]
        return random.choice(km_posible)

    def generate_garantie(self) -> str:
        """
        Aceasta functie alege daca masina are sau nu garantie
        :return:
        """
        garantie = ['da', 'nu']
        return random.choice(garantie)
