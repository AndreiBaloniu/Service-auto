from Domain.Entity import Entity
from Domain.UndoRedoOperations import UndoRedoOperation
from Repositories.Repository import Repository


class AddOperation(UndoRedoOperation):

    def __init__(self, repository: Repository,
                 entity: Entity):

        self.repository = repository
        self.entity = entity

    def do_undo(self):
        self.repository.delete(self.entity.id_entity)

    def do_redo(self):
        self.repository.create(self.entity)
