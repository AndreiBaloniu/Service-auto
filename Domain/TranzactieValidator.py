from Domain.Tranzactie import Tranzactie


class TranzactieValidatorError(Exception):
    pass


class TranzactieValidator:
    def validate(self, tranzactie: Tranzactie):
        if tranzactie.suma_manopera < 0:
            raise TranzactieValidatorError(f'{tranzactie.suma_manopera} '
                                           f'is not an allowed value.')
        if tranzactie.suma_piese < 0:
            raise TranzactieValidatorError(f'{tranzactie.suma_piese} '
                                           f'is not an allowed value.')
        if len(tranzactie.data) != 10:
            raise TranzactieValidatorError('Data trebuie sa fie de format '
                                           'dd.mm.yyyy')
        if tranzactie.data[2] != '.':
            raise TranzactieValidatorError('Data trebuie sa fie de format '
                                           'dd.mm.yyyy')
        if tranzactie.data[5] != '.':
            raise TranzactieValidatorError('Data trebuie sa fie de format '
                                           'dd.mm.yyyy')
        if len(tranzactie.ora) != 5:
            raise TranzactieValidatorError('Ora trebuie sa fie de format '
                                           'hh:mm.')
        if tranzactie.ora[2] != ':':
            raise TranzactieValidatorError('Ora trebuie sa fie de format '
                                           'hh:mm.')
