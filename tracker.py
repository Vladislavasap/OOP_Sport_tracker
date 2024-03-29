from dataclasses import asdict, dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MINUTES_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Cycling(Training):
    '''Тренировка: езда на велосипеде'''
    LEN_STEP = 1.40
    COEFF_FOR_TRAIL = 6
    COEFF_FOR_CLASSIC = 2.5

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 area_type: str
                 ) -> None:
        super().__init__(action, duration, weight)
        self.area_type = area_type

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        if self.area_type == 'trail':
            colories_per_minute = (self.COEFF_FOR_TRAIL * self.get_mean_speed()
                                   * self.weight)
        else:
            colories_per_minute = (self. COEFF_FOR_CLASSIC
                                   * self.get_mean_speed()
                                   * self.weight)
        training_mins = self.duration * self.MINUTES_IN_HOUR
        return (colories_per_minute / self.M_IN_KM) * training_mins


class Running(Training):
    """Тренировка: бег."""
    COEFF3: int = 18
    COEFF4: int = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        colories_per_minute = ((self.COEFF3 * self.get_mean_speed()
                               - self.COEFF4)
                               * self.weight)
        training_mins = self.duration * self.MINUTES_IN_HOUR
        return (colories_per_minute / self.M_IN_KM) * training_mins


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIES_1: float = 0.035
    COEFF_CALORIES_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALORIES_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.COEFF_CALORIES_2 * self.weight)
                * (self.duration * self.MINUTES_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""
    COEFF1: float = 1.1
    COEFF2: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км. в плавании"""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.lenght_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.COEFF1)
                * self.COEFF2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
        'CYC': Cycling
    }

    if workout_type not in training_type:
        raise ValueError(f'Некорректный тип тренировки {workout_type}')
    else:
        return training_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = Training.show_training_info(training)
    print(InfoMessage.get_message(info))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('CYC', [10000, 1, 75, 'trial'])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
