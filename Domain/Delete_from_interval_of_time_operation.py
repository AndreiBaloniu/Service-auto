from Domain.Entity import Entity
from Domain.UndoRedoOperations import UndoRedoOperation
from Repositories.Repository import Repository


class DeleteFromIntervalOperation(UndoRedoOperation):

    def __init__(self,
                 repository: Repository,
                 entity: Entity,
                 entity_after_update: Entity):

        self.repository = repository
        self.entity = entity
        self.entity_after_update = entity_after_update

    def do_undo(self):

        self.repository.update(self.entity)

    def do_redo(self):

        self.repository.update(self.entity_after_update)
