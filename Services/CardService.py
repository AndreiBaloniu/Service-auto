from Domain.AddOperation import AddOperation
from Domain.Card_client import Card_client
from Domain.CardValidator import CardValidator
from Domain.DeleteOperation import DeleteOperation
from Domain.UpdateOperation import UpdateOperation
from Repositories.Repository import Repository
from Services.UndoRedoService import UndoRedoService


class CardService:

    def __init__(self, cardRepository: Repository,
                 cardValidator: CardValidator,
                 undo_redo_service: UndoRedoService):
        self.cardValidator = cardValidator
        self.cardRepository = cardRepository
        self.undo_redo_service = undo_redo_service

    def add(self, cardId: str,
            nume: str,
            prenume: str,
            CNP: int,
            data_nasterii: str,
            data_inregistrarii: str):
        """
        Functia de adaugare card
        :param cardId: id-ul clientului
        :param nume: numele clientului
        :param prenume: prenumele clientului
        :param CNP: CNP-ul clientului
        :param data_nasterii: data nasterii clientului
        :param data_inregistrarii: data inregistrarii clientului
        :return:
        """
        if self.cnp_unique(CNP) is False:
            raise ValueError("Exista deja un utilizator cu acest CNP")
        card = Card_client(cardId, nume,
                           prenume, CNP,
                           data_nasterii, data_inregistrarii)
        self.cardValidator.validate(card)
        self.cardRepository.create(card)

        self.undo_redo_service.clear_redo_list()
        card_add_op = AddOperation(self.cardRepository, card)
        self.undo_redo_service.add_operation(card_add_op)

    def update(self, cardId: str,
               nume: str,
               prenume: str,
               CNP: int,
               data_nasterii: str,
               data_inregistrarii: str):
        """
        Functia de update card
        :param cardId: id-ul clientului
        :param nume: numele clientului
        :param prenume: prenumele clientului
        :param CNP: CNP-ul clientului
        :param data_nasterii: data nasterii clientului
        :param data_inregistrarii: data inregistrarii clientului
        :return:
        """
        if not self.cnp_unique(CNP):
            raise ValueError("Exista deja un card cu acest CNP.")

        card_before_update = self.get_card(cardId)
        card = Card_client(cardId, nume,
                           prenume, CNP,
                           data_nasterii, data_inregistrarii)
        self.cardValidator.validate(card)
        self.cardRepository.create(card)

        card_update_op = UpdateOperation(self.cardRepository,
                                         card_before_update,
                                         card)

        self.undo_redo_service.clear_redo_list()
        self.undo_redo_service.update_operation(card_update_op)

    def delete(self, cardId: str):
        """
        Functia de stergere card
        :param cardId: id-ul clientului
        :return:
        """
        card = self.cardRepository.read(cardId)
        self.cardRepository.delete(cardId)

        card_del_op = DeleteOperation(self.cardRepository, card)

        self.undo_redo_service.clear_redo_list()
        self.undo_redo_service.delete_operation(card_del_op)

    def get_cards(self):
        """
        Functia de afisare a tuturor cardurilor
        """
        return self.cardRepository.read()

    def get_card(self, cardId):
        """
        Functia de afisare a unui card
        """
        return self.cardRepository.read(cardId)

    def cnp_unique(self, cnp=None):
        """
        Functie pentru unicitatea CNP-ului
        :param cnp:
        :return:
        """
        cards = self.cardRepository.read()

        for elem in cards:
            if elem.CNP == cnp:
                return False
        return True
