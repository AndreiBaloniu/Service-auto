from Domain.AddOperation import AddOperation
from Domain.Car import Car
from Domain.CarValidator import CarValidator
from Domain.DeleteOperation import DeleteOperation
from Domain.UpdateOperation import UpdateOperation
from Repositories.Repository import Repository
from Services.UndoRedoService import UndoRedoService


class CarService:

    def __init__(self, carRepository: Repository,
                 carValidator: CarValidator,
                 undo_redo_service: UndoRedoService):
        self.carValidator = carValidator
        self.carRepository = carRepository
        self.undo_redo_service = undo_redo_service

    def add(self, carId: str,
            nume: str,
            an_achizitie: int,
            nr_km: float,
            garantie: str):
        """
        Functie adaugare masina
        :param carId:
        :param nume:
        :param an_achizitie:
        :param nr_km:
        :param garantie:
        :return:
        """
        car = Car(carId, nume, an_achizitie, nr_km, garantie)
        self.carValidator.validate(car)
        self.carRepository.create(car)

        self.undo_redo_service.clear_redo_list()
        car_add_op = AddOperation(self.carRepository, car)
        self.undo_redo_service.add_operation(car_add_op)

    def update(self, carId: str,
               nume: str,
               an_achizitie: int,
               nr_km: float,
               garantie: str):
        """
        Functie update masina
        :param carId:
        :param nume:
        :param an_achizitie:
        :param nr_km:
        :param garantie:
        :return:
        """
        car_before_update = self.get_car(carId)
        car = Car(carId, nume, an_achizitie, nr_km, garantie)
        self.carValidator.validate(car)
        self.carRepository.update(car)

        car_update_op = UpdateOperation(self.carRepository, car_before_update,
                                        car)

        self.undo_redo_service.clear_redo_list()
        self.undo_redo_service.update_operation(car_update_op)

    def delete(self, carId: str):
        """
        Functie sterge masina
        :param carId:
        :return:
        """
        car = self.carRepository.read(carId)
        self.carRepository.delete(carId)

        car_del_op = DeleteOperation(self.carRepository, car)

        self.undo_redo_service.clear_redo_list()
        self.undo_redo_service.delete_operation(car_del_op)

    def get_cars(self):
        """
        Returneaza o lista care contine toate obiectele de tip car din
        repository
        :return:
        """
        return self.carRepository.read()

    def get_car(self, carId):
        """
        Returneaza obiectul de tip car cu id-ul transmis ca parametru
        :param carId:
        :return:
        """
        return self.carRepository.read(carId)

    def update_warranty(self):
        """
        Actualizeaza garantia pentru fiecare masina
        :return:
        """

        cars = self.carRepository.read(None)
        operations = []

        cars_under_warranty = [car for car in cars
                               if 2021 - car.an_achizitie <= 3 and
                               car.nr_km <= 60000]

        cars_not_under_warranty = [car for car in cars
                                   if 2021 - car.an_achizitie > 3 or
                                   car.nr_km > 60000]

        for car in cars_under_warranty:
            car_before_update = self.get_car(car.id_entity)

            car.garantie = "da"
            self.carRepository.update(car)

            car_after_update = self.get_car(car.id_entity)

            car_update_op = UpdateOperation(self.carRepository,
                                            car_before_update,
                                            car_after_update)

            operations.append(car_update_op)

        for car in cars_not_under_warranty:
            car_before_update = self.get_car(car.id_entity)

            car.garantie = "nu"
            self.carRepository.update(car)

            car_after_update = self.get_car(car.id_entity)

            car_update_op = UpdateOperation(self.carRepository,
                                            car_before_update,
                                            car_after_update)

            operations.append(car_update_op)

        self.undo_redo_service.update_warranty(operations)
