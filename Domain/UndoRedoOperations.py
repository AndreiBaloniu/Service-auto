from abc import ABC, abstractmethod


class UndoRedoOperation(ABC):

    @abstractmethod
    def do_undo(self):
        ...

    @abstractmethod
    def do_redo(self):
        ...
