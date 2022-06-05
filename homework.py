from typing import Type


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Выводит сообщение со статистикой тренировки."""
        message: str = (f'Тип тренировки: {self.training_type}; '
                        f'Длительность: {self.duration:0.3f} ч.; '
                        f'Дистанция: {self.distance:0.3f} км; '
                        f'Ср. скорость: {self.speed:0.3f} км/ч; '
                        f'Потрачено ккал: {self.calories:0.3f}.')
        return message


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65  # Расстояние за 1 шаг
    M_IN_KM: int = 1000  # Константа для перевода метров в километры

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 LEN_STEP: float = 0.65,
                 ) -> None:
        self.action = action  # Количество шагов/гребков
        self.duration = duration  # Длительность тренировки
        self.weight = weight  # Вес спортсмена

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        LEN_STEP: float = 0.65  # Расстояние за 1 шаг
        M_IN_KM: int = 1000  # Константа для перевода метров в километры
        distance: float = self.action * LEN_STEP / M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        minutes_in_hour: int = 60
        M_IN_KM: int = 1000  # Константа для перевода метров в километры
        # Длительность тренировки в минутах
        duration_in_min: float = self.duration * minutes_in_hour
        calorie_consumption: float = (coeff_calorie_1 * self.get_mean_speed()
                                      - coeff_calorie_2) * self.weight / M_IN_KM * duration_in_min
        return calorie_consumption


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height  # Рост спортсмена

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_3: float = 0.035
        coeff_calorie_4: int = 2
        coeff_calorie_5: float = 0.029
        minutes_in_hour: int = 60  # Количество минут в 1 часе
        # Длительность тренировки в минутах
        duration_in_min: float = self.duration * minutes_in_hour
        calorie_consumption: float = (coeff_calorie_3 * self.weight + (self.get_mean_speed()
                                                                       ** coeff_calorie_4 // self.height) * coeff_calorie_5 * self.weight) * duration_in_min
        return calorie_consumption


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
        self.length_pool = length_pool  # Длина бассейна в метрах
        self.count_pool = count_pool  # Сколько раз спортсмен переплыл бассейн

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        LEN_STEP: float = 1.38  # Расстояние за 1 гребок
        M_IN_KM: int = 1000  # Константа для перевода метров в километры
        distance: float = self.action * LEN_STEP / M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        M_IN_KM: int = 1000  # Константа для перевода метров в километры
        mean_speed: float = self.length_pool * self.count_pool / M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_6: float = 1.1
        coeff_calorie_7: int = 2
        calorie_consumption: float = (self.get_mean_speed()
                                      + coeff_calorie_6) * coeff_calorie_7 * self.weight
        return calorie_consumption


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    traning_version: dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    return traning_version[workout_type](*data)


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
