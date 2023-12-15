from itertools import combinations
from copy import deepcopy


class Profile:
    """
    Родительский класс для классов изделий и остатков
    """
    def __init__(self):
        """
        self.width - список ширин
        """
        self.width: list[float] = list()

    def add(self, new_width: list[float]):
        """
        Метод для добавления ширин новых профилей.
        :param new_width: список ширин добавляемых профилей.
        :return: Ничего
        """
        self.width.extend(new_width)
        self.width.sort()

    def remove(self, deleted_width: list[float], str_error: str):
        """
        Метод для удаления не нежных профилей. Возможно метод не понадобится.
        :param deleted_width: Список ширин удаляемых профилей.
        :param str_error: Строка для вывода ошибки.
        :return: Ничего
        """
        for profile_width in deleted_width:
            try:
                self.width.remove(profile_width)
            except ValueError:
                print(str_error + str(profile_width))

    def get_number(self) -> int:
        """
        Метод для получения длины списка профилей.
        :return: Длина списка профилей.
        """
        return len(self.width)


class Products(Profile):
    def __init__(self, delta: float):
        """
        :param delta: Длина разреза.
        """
        super().__init__()
        self.delta: float = delta

    def remove_products(self, deleted_width: list[float]):
        super().remove(deleted_width, str_error='Ошибка! В списке нет изделия шириной ')


class Remains(Profile):
    def __init__(self, length_whole_profile: float, number_whole_profile: int):
        """
        :param length_whole_profile: Длина целого профиля.
        :param number_whole_profile: Количество целых профилей.
        """
        super().__init__()
        self.length_whole_profile: float = length_whole_profile
        self.number_whole_profile: int = number_whole_profile

    def remove_remains(self, deleted_width: list[float]):
        super().remove(deleted_width, str_error='Ошибка! В списке нет остатка шириной ')

    def get_max_remain(self) -> float:
        """
        Возвращает максимальную длину остатков.
        :return: Длина остатка.
        """
        if self.number_whole_profile == 0:
            return self.length_whole_profile
        else:
            return max(self.width)


class Optimization:
    @staticmethod
    def get_all_collections(products: Products, max_length_remain: float) -> list[tuple[float]]:
        """
        Метод для получения всевозможных наборов ширин изделий, сумма которых не превышает максимальную длину остатка.
        :param products: Объект Products.
        :param max_length_remain: Максимальная длина остатков.
        :return: Список списков ширин изделий.
        """
        result_collections: list[tuple[float]] = list()

        for i in range(products.get_number()):
            collections: list[tuple[float]] = list(combinations(products.width, i))
            flag: bool = False
            for collection in collections:
                if sum(collection) + len(collection) * products.delta < max_length_remain:
                    result_collections.append(collection)
                    flag = True
            if not flag:
                break

        return result_collections

    @staticmethod
    def remove_collection_from_products(products: Products, collection: tuple[float]) -> list[float]:
        """
        Метод для удаления ширины изделий, входящих в коллекцию, из списка изделий.
        :param products:
        :param collection:
        :return:
        """
        # Скопируем список изделий
        result: list[float] = deepcopy(products.width)

        for product in collection:
            result.remove(product)

        return result
