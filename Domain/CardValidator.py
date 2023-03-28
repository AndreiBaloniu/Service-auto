from Domain.Card_client import Card_client


class CardValidatorError(Exception):
    pass


class CardValidator:
    def validate(self, card: Card_client):
        if len(str(card.CNP)) != 13:
            raise CardValidatorError(f'{card.CNP} is not an allowed value')
        if len(card.data_nasterii) != 10:
            raise CardValidatorError('Data nasterii trebuie sa fie de '
                                     'formatul '
                                     'dd.mm.yyyy')
        if len(card.data_inregistrarii) != 10:
            raise CardValidatorError('Inregistration date '
                                     'needs to be a dd.mm.yyyy '
                                     'format!')
        if card.data_nasterii[2] != '.':
            raise CardValidatorError('Data nasterii trebuie sa fie de '
                                     'formatul '
                                     'dd.mm.yyyy')
        if card.data_nasterii[5] != '.':
            raise CardValidatorError('Data nasterii trebuie sa fie de '
                                     'formatul '
                                     'dd.mm.yyyy')
        if card.data_inregistrarii[2] != '.':
            raise CardValidatorError('Data inregistrarii trebuie sa fie '
                                     'de formatul dd.mm.yyyy')
        if card.data_inregistrarii[5] != '.':
            raise CardValidatorError('Data inregistrarii trebuie sa fie '
                                     'de formatul dd.mm.yyyy')
