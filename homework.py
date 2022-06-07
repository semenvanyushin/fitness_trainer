from dataclasses import dataclass
from typing import ClassVar, Dict, Sequence, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: ClassVar[Dict[str, str]] = {
        'Тип тренировки': '',
        'Длительность': '',
        'Дистанция': '',
        'Ср. скорость': '',
        'Потрачено ккал': '',
    }

    def get_message(self) -> str:
        """Возвращает сообщение со статистикой тренировки."""
        self.message['Тип тренировки'] = f'{self.training_type}'
        self.message['Длительность'] = f'{self.duration:0.3f} ч.'
        self.message['Дистанция'] = f'{self.distance:0.3f} км'
        self.message['Ср. скорость'] = f'{self.speed:0.3f} км/ч'
        self.message['Потрачено ккал'] = f'{self.calories:0.3f}.'
        return '; '.join("{}: {}".format(k, v)
                         for k, v in self.message.items())


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65  # Расстояние за 1 шаг
    M_IN_KM: float = 1000  # Константа для перевода метров в километры

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.LEN_STEP: float = 0.65  # Расстояние за 1 шаг
        self.M_IN_KM: float = 1000  # Константа для перевода метров в километры
        self.MINUTES_IN_HOUR: float = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_distance = self.get_distance()
        training_mean_speed = self.get_mean_speed()
        training_spent_calories = self.get_spent_calories()

        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           training_distance,
                           training_mean_speed,
                           training_spent_calories,
                           )


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.COEFF_CALORIE_1: float = 18
        self.COEFF_CALORIE_2: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # Длительность тренировки в минутах
        duration_in_min: float = self.duration * self.MINUTES_IN_HOUR
        mean_speed_run: float = self.get_mean_speed()
        spent_calorie: float = ((self.COEFF_CALORIE_1 * mean_speed_run
                                 - self.COEFF_CALORIE_2) * self.weight
                                / self.M_IN_KM * duration_in_min)
        return spent_calorie


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.COEFF_CALORIE_3: float = 0.035
        self.COEFF_CALORIE_4: float = 2
        self.COEFF_CALORIE_5: float = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # Длительность тренировки в минутах
        duration_in_min: float = self.duration * self.MINUTES_IN_HOUR
        mean_speed_sportswalking: float = self.get_mean_speed()
        spent_calories: float = ((self.COEFF_CALORIE_3 * self.weight
                                  + (mean_speed_sportswalking
                                     ** self.COEFF_CALORIE_4
                                     // self.height)
                                  * self.COEFF_CALORIE_5
                                  * self.weight) * duration_in_min)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38  # Расстояние за 1 гребок

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.LEN_STEP: float = 1.38  # Расстояние за 1 гребок
        self.COEFF_CALORIE_6: float = 1.1
        self.COEFF_CALORIE_7: float = 2

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = (self.length_pool * self.count_pool
                             / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_speed_swimming: float = self.get_mean_speed()
        calorie_consumption: float = ((mean_speed_swimming
                                       + self.COEFF_CALORIE_6)
                                      * self.COEFF_CALORIE_7 * self.weight)
        return calorie_consumption


def read_package(workout_type: str, data: Sequence[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    traning_version: dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    dict_keys: Sequence[str] = traning_version.keys()

    if workout_type in dict_keys:
        return traning_version[workout_type](*data)
    else:
        raise AttributeError


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
