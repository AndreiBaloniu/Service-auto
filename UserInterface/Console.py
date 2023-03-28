from datetime import datetime
from Repositories.Exceptions import DuplicatieId
from Services.CarService import CarService
from Services.CardService import CardService
from Services.TranzactieService import TranzactieService
from Services.Random_generator import Generator
from Services.Cautare_full_text import Search
from Services.Afisare_cars_dupa_suma_manopera import cars_by_handworksum
from Services.Afisare_carduri_dupa_discount import card_by_discount
from Services.Delete_cascada import Delete_Cascada
from Services.UndoRedoService import UndoRedoService


class Console:

    def __init__(self,
                 car_service: CarService,
                 card_service: CardService,
                 tranzactie_service: TranzactieService,
                 search: Search,
                 generator_random: Generator,
                 cars_by_handwork: cars_by_handworksum,
                 cards_by_discount: card_by_discount,
                 delete_cascada: Delete_Cascada,
                 undo_redo_service: UndoRedoService):
        self.carService = car_service
        self.cardService = card_service
        self.tranzactieService = tranzactie_service
        self.search = search
        self.generator = generator_random
        self.cars_by_handwork = cars_by_handwork
        self.card_by_discount = cards_by_discount
        self.delete_cascada = delete_cascada
        self.undo_redo_service = undo_redo_service

    def show_menu(self):
        print('a[car|card|tranz - adaugare masina sau card sau tranzactie')
        print('d[car|card|tranz - detele masina sau card sau tranzactie')
        print('u[car|card|tranz - update masina sau card sau tranzactie')
        print('s[car|card|tranz - showall masina sau card sau tranzactie')
        print('so[car|card|tranz - showone masina sau card sau tranzactie')
        print('r. random car generator')
        print('1. Căutare mașini și clienți. Căutare full text.')
        print('2. Afișarea tuturor tranzacțiilor cu\
 suma cuprinsă într-un interval dat')
        print('3. Afișarea mașinilor ordonate descrescător după\
 suma obținută pe manoperă.')
        print('4. Afișarea cardurilor client ordonate descrescător\
 după valoarea reducerilor obținute.')
        print('5. Ștergerea tuturor tranzacțiilor dintr-un\
 anumit interval de zile.')
        print('6. Actualizarea garanției la fiecare mașină: o mașină este\
 în garanție dacă și numai dacă are maxim 3 ani de la achiziție\
 și maxim 60 000 de km.')
        print('z. Undo ultima operatie.')
        print('y. Redo ultima operatie.')
        print('s. Stergere cascada.')
        print('x. Iesire.')

    def run_console(self):
        while True:
            self.show_menu()
            opt = input('Alegeti optiunea: ')

            if opt == 'acar':
                self.handle_add_car()
            elif opt == 'acard':
                self.handle_add_card()
            elif opt == 'atranz':
                self.handle_add_tranzactie()
            elif opt == 'dcar':
                self.handle_delete_car()
            elif opt == 'dcard':
                self.handle_delete_card()
            elif opt == 'dtranz':
                self.handle_delete_tranzactii()
            elif opt == 'ucar':
                self.handle_update_car()
            elif opt == 'ucard':
                self.handle_update_card()
            elif opt == 'utranz':
                self.handle_update_tranzactii()
            elif opt == 'scar':
                self.handle_show_all(self.carService.get_cars())
            elif opt == 'scard':
                self.handle_show_all(self.cardService.get_cards())
            elif opt == 'stranz':
                self.handle_show_all(self.tranzactieService.get_transactions())
            elif opt == 'socar':
                self.handle_show_car()
            elif opt == 'socard':
                self.handle_show_clientcard()
            elif opt == 'sotraz':
                self.handle_show_tranzactie()
            elif opt == '1':
                self.search_full_text()
            elif opt == '2':
                self.handle_show_all_transactions_by_sum()
            elif opt == '3':
                self.handle_descending_cars_by_handwork()
            elif opt == '4':
                self.handle_cards_by_discount()
            elif opt == '5':
                self.handle_delete_from_interval_of_time()
            elif opt == '6':
                self.handle_update_garantie()
            elif opt == 'r':
                self.random_generator()
            elif opt == 's':
                self.handle_delete_cascada()
            elif opt == 'z':
                self.undo_redo_service.undo()
            elif opt == 'y':
                self.undo_redo_service.redo()
            elif opt == 'x':
                break
            else:
                print('Comanda invalida, reincearca.')

    def handle_show_all(self, objects):
        """
        Afisare toate obiectele (masina/ card/ tranzactie)
        :param objects:
        :return:
        """
        for obj in objects:
            print(obj)

    def handle_show_car(self):
        """
        Afisare o masina
        :return:
        """
        car_id = input('Dati id-ul masinii pe care doriti sa o vedeti: ')
        print(self.carService.get_car(car_id))

    def handle_show_clientcard(self):
        """
        Afisare un card client
        :return:
        """
        clientcard_id = input('Dati id-ul cardului '
                              'pe care doriti sa-l vedeti: ')
        print(self.cardService.get_card(clientcard_id))

    def handle_show_tranzactie(self):
        """
        Afisare o tranzactie
        :return:
        """
        transaction_id = input('Dati id-ul tranzactiei '
                               'pe care doriti sa o vedeti: ')
        print(self.tranzactieService.get_transaction(transaction_id))

    def handle_add_car(self):
        """
        Adaugare masina
        :return:
        """
        try:
            id = input('Dati id-ul masinii: ')
            nume = input('Dati numele masinii: ')
            an_achizitie = int(input('Dati anul achizitiei masinii: '))
            nr_km = float(input('Dati numarul de kilometri masinii: '))
            garantie = input('Este in garantie masina? ')

            self.carService.add(id,
                                nume,
                                an_achizitie,
                                nr_km,
                                garantie)

        except DuplicatieId as ve:
            print('ID Duplicat: ', ve)

    def handle_add_card(self):
        """
        Adaugare card
        :return:
        """
        try:
            id = input('Dati id-ul cardului: ')
            nume = input('Dati numele proprietarului cardului: ')
            prenume = input('Dati prenumele proprietarului cardului: ')
            CNP = int(input('Dati CNP-ul proprietarului cardului: '))
            data_nasterii = input('Data nasterii (dd.mm.yyyy): ')
            data_inregistrarii = input('Data inregistrarii (dd.mm.yyyy): ')

            self.cardService.add(id,
                                 nume,
                                 prenume,
                                 CNP,
                                 data_nasterii,
                                 data_inregistrarii)

        except ValueError as ve:
            print('Eroare', ve)

    def handle_add_tranzactie(self):
        """
        Adaugare tranzactie
        :return:
        """
        try:
            id = input('Dati id-ul tranzactiei: ')
            id_masina = input('Dati id-ul masinii: ')
            id_card_client = input('Dati id-ul cardului: ')
            suma_piese = float(input('Suma piese: '))
            suma_manopera = float(input('Suma manopera: '))
            data = input('Data (dd.mm.yyyy): ')
            ora = input('Ora (hh:mm): ')
            discount = 0

            self.tranzactieService.add(id, id_masina,
                                       id_card_client,
                                       suma_piese,
                                       suma_manopera,
                                       data,
                                       ora,
                                       discount)
        except ValueError as ve:
            print('Eroare', ve)

    def handle_delete_car(self):
        """
        Stergere masina
        :return:
        """
        try:
            id = input('Dati id-ul masinii: ')

            self.carService.delete(id)
        except ValueError as ve:
            print('Eroare', ve)

    def handle_delete_card(self):
        """
        Stergere card
        :return:
        """
        try:
            id = input('Dati id-ul cardului: ')

            self.cardService.delete(id)
        except ValueError as ve:
            print('Eroare', ve)

    def handle_delete_tranzactii(self):
        """
        Stergere tranzactie
        :return:
        """
        try:
            id = input('Dati id-ul tranzactiei: ')

            self.tranzactieService.delete(id)
        except ValueError as ve:
            print('Eroare', ve)

    def handle_update_car(self):
        """
        Update masina
        :return:
        """
        try:
            id = input('Dati id-ul masinii: ')
            nume = input('Dati numele masinii: ')
            an_achizitie = int(input('Dati anul achizitiei masinii: '))
            nr_km = float(input('Dati numarul de kilometri masinii: '))
            garantie = input('Este in garantie masina?')

            self.carService.update(id,
                                   nume,
                                   an_achizitie,
                                   nr_km,
                                   garantie)

        except ValueError as ve:
            print('Eroare', ve)

    def handle_update_card(self):
        """
        Update card
        :return:
        """
        try:
            id = input('Dati id-ul cardului: ')
            nume = input('Dati numele proprietarului cardului: ')
            prenume = input('Dati prenumele proprietarului cardului: ')
            CNP = int(input('Dati CNP-ul proprietarului cardului: '))
            data_nasterii = input('Data nasterii (dd.mm.yyyy): ')
            data_inregistrarii = input('Data inregistrarii (dd.mm.yyyy): ')

            self.cardService.update(id,
                                    nume,
                                    prenume,
                                    CNP,
                                    data_nasterii,
                                    data_inregistrarii)

        except ValueError as ve:
            print('Eroare', ve)

    def handle_update_tranzactii(self):
        """
        Update tranzactie
        :return:
        """
        try:
            id = input('Dati id-ul tranzactiei: ')
            id_masina = input('Dati id-ul masinii: ')
            id_card_client = input('Dati id-ul cardului: ')
            suma_piese = float(input('Suma piese: '))
            suma_manopera = float(input('Suma manopera: '))
            data = input('Data (dd.mm.yyyy): ')
            ora = input('Ora (hh:mm): ')
            discount = 0

            self.tranzactieService.update(id,
                                          id_masina,
                                          id_card_client,
                                          suma_piese,
                                          suma_manopera,
                                          data,
                                          ora,
                                          discount)

        except ValueError as ve:
            print('Eroare', ve)

    def handle_show_all_transactions_by_sum(self):
        """
        Afisare toate tranzactiile dintr-un interval dat
        :return:
        """
        try:
            val1 = float(input('Capul inferior al intervalului: '))
            val2 = float(input('Capul superior al intervalului: '))

            transactions = self.tranzactieService.get_transactions()

            transactions_list = self.tranzactieService. \
                all_transactions_from_an_interval(val1, val2, transactions, [],
                                                  0)

            print("")
            for transaction in transactions_list:
                print(transaction)

        except ValueError as ve:
            print('Eroare de validare: ', ve)
        except KeyError as ke:
            print('Eroare de cheie: ', ke)
        except Exception as ex:
            print('Eroare: ', ex)

    def search_full_text(self):
        """
        Cautare full text
        :return:
        """
        try:
            text = input("Introduceti textul ce vreti sa-l cautati:")
            searches = self.search.search_full_text(text)
            print(f'{searches}')
        except Exception as ex:
            print('Eroare: ', ex)

    def random_generator(self):
        """
        Random car generator
        :return:
        """

        try:
            n = int(input("Introduceti numarul de masini formate aleatoriu: "))
            for i in range(0, n):
                self.carService.add(self.generator.generate_id(),
                                    self.generator.generate_nume(),
                                    self.generator.generate_an(),
                                    self.generator.generate_km(),
                                    self.generator.generate_garantie())

        except ValueError as ve:
            print('Eroare', ve)

    def handle_descending_cars_by_handwork(self):
        """
        Functie afisare masini ordonate desc. dupa suma manopera
        :return:
        """
        print(self.cars_by_handwork.cars_desc_by_handwork())

    def handle_cards_by_discount(self):
        """
        Functie afisare carduri ordonate desc. dupa discount
        :return:
        """
        print(self.card_by_discount.cards_by_discount())

    def handle_delete_from_interval_of_time(self):

        """
        Sterge toate tranzactiile dintr-un interval de timp
        :return:
        """
        try:
            date_1 = input("Introduceti prima data(dd.mm.yyyy): ")
            datetime.strptime(date_1, '%d.%m.%Y')
            date_2 = input("Introduceti a doua data(dd.mm.yyyy) ")
            datetime.strptime(date_2, '%d.%m.%Y')

            self.tranzactieService.\
                delete_from_interval_of_time(date_1, date_2)

        except ValueError as ve:
            print("Data introdusa nu este valida(dd.mm.yyyy).", ve)
        except Exception as ex:
            print("Eroare", ex)

    def handle_update_garantie(self):
        """
        Functie update garantie
        :return:
        """
        self.carService.update_warranty()
        print()
        print('Garantia a fost modificata')

    def handle_delete_cascada(self):
        """
        Functie delete cascada
        :return:
        """
        id_de_sters = input('Dati id-ul ce doriti sa-l stergeti: ')
        print(self.delete_cascada.delete_cascada(id_de_sters))
