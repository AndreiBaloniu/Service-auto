from Domain.Car import Car
from Repositories.RepositoryJson import RepositoryJson
from utils import clear_file


def test_car_repository():
    """
    Functie test car repository
    :return:
    """
    filename = 'test_cars.json'
    clear_file(filename)
    car_repository = RepositoryJson(filename)
    added = Car('1', 'Dacia Logan', 2019, 72000, 'Da')
    car_repository.create(added)
    assert car_repository.read(added.id_entity) == added
