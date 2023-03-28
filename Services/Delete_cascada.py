from Domain.Delete_cascada import DeleteCascada
from Repositories.Repository import Repository
from Services.TranzactieService import TranzactieService
from Services.CarService import CarService
from Services.UndoRedoService import UndoRedoService


class Delete_Cascada:
    def __init__(self,
                 car_repository: Repository,
                 car_service: CarService,
                 tranzactie_repository: Repository,
                 tranzactie_service: TranzactieService,
                 undo_redo_service: UndoRedoService):
        self.car_repository = car_repository
        self.car_service = car_service
        self.tranzactie_repository = tranzactie_repository
        self.tranzactie_service = tranzactie_service
        self.undo_redo_service = undo_redo_service

    def delete_cascada(self, id_entity: str):
        try:
            if self.tranzactie_repository.read(id_entity) is None:
                raise ValueError("ID-ul introdus nu exista.")

            tranzactie = self.tranzactie_service.get_transaction(id_entity)
            car = self.car_service.get_car(tranzactie.id_masina)

            self.car_service.delete(tranzactie.id_masina)
            self.tranzactie_service.delete(id_entity)

            del_waterfall_op = DeleteCascada(self.tranzactie_repository,
                                             self.car_repository, tranzactie,
                                             car)

            self.undo_redo_service.clear_redo_list()

            self.undo_redo_service.delete_cascada(del_waterfall_op)

        except Exception as ex:
            print(ex)
        except KeyError as ke:
            print(ke)
