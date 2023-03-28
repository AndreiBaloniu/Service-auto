from Domain.Entity import Entity
from Domain.UndoRedoOperations import UndoRedoOperation
from Repositories.Repository import Repository


class DeleteCascada(UndoRedoOperation):

    def __init__(self,
                 repository_1: Repository,
                 repository_2: Repository,
                 entity_1: Entity,
                 entity_2: Entity):

        self.repository_1 = repository_1
        self.repository_2 = repository_2
        self.entity_1 = entity_1
        self.entity_2 = entity_2

    def do_undo(self):

        self.repository_1.create(self.entity_1)
        self.repository_2.create(self.entity_2)

    def do_redo(self):

        self.repository_1.delete(self.entity_1.id_entity)
        self.repository_2.delete(self.entity_2.id_entity)
