from Domain.Car import Car


class CarValidatorError(Exception):
    pass


class CarValidator:
    def validate(self, car: Car):
        garantieValues = ["da", "nu"]
        if car.an_achizitie < 0:
            raise CarValidatorError(f'{car.an_achizitie} is not '
                                    f'an allowed value.')
        if car.nr_km < 0:
            raise CarValidatorError(f'{car.nr_km} is not an allowed value.')
        if car.garantie not in garantieValues:
            raise CarValidatorError(f'{car.garantie} is not an allowed value.')
