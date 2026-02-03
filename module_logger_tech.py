from datetime import datetime
import re


# технические функции логгера
def today_str():
    """
    Возвращает текущую дату
    :return (str): Текущая дата в формате "%d.%m.%Y"
    """
    now = datetime.now()
    return now.strftime("%d.%m.%Y")
    # return f"{now.day}.{now.month}.{now.year}"


def time_str():
    """
        Возвращает текущее время
        :return (str): Текущее время в формате "%H-%M"
    """
    now = datetime.now()
    return f"{now.hour}-{now.minute}"


# def time_hh_mm_ss_str():
#
#     now = datetime.now()
#     return f"{now.hour}-{now.minute}-{now.second}"


def check_format_1(content):
    """
    Проверяет соответствие строки регулярному выражению r'\(\d+\.\d+\) \d\d\.\d\d\.\d{4} \d\d-\d\d.*'

    :param content: Строка для проверки
    :return (bool): Результат проверки
    """
    return re.search(r'\(\d+\.\d+\) \d\d\.\d\d\.\d{4} \d\d-\d\d.*', content)


def check_format_2(content):
    """
    Проверяет соответствие строки регулярному выражению r'\(\d+\.\d+\).*'

    :param content: Строка для проверки
    :return (bool): Результат проверки
    """
    return re.search(r'\(\d+\.\d+\).*', content)


def find_launch_num(filename):
    """
    Находит номер запуска по имени файла
    :param filename (str): имя файла
    :return (int): номер запуска
    """
    return int(re.findall(r'\d+', filename)[1])

def find_launch_day(filename):
    """
    Находит день запуска по имени файла
    :param filename (str): имя файла
    :return (int): день запуска
    """
    return int(re.findall(r'\d+', filename)[0])

def find_launch_date(filename):
    """
    Находит дату запуска по имени файла
    :param filename (str): имя файла
    :return (str): дату запуска
    """
    return re.search(r'\d\d\.\d\d\.\d{4}', filename)[0]


def checkType(object, need_type, object_name="Объект"):
    """
    Проверяет, принадлежит ли объект к нужному типу.

    Аргументы:
        :param object (__obj): Проверяемый объект
        :param need_type: Нужный тип/свойство
        :param object_name: Имя объекта, которое отобразится в исключении
    Возвращаемое значение:
        :return (__obj): Если объект принадлежит к нужному типу

    Если объект не принадлежит к нужному типу, то будет вызвано исключение
    """
    if need_type == callable:
        if not callable(object):
            raise TypeError(f"{object_name} ({object}) является {type(object)}, а должен быть {need_type}")
    elif not isinstance(object, need_type):
        raise TypeError(f"{object_name} ({object}) имеет тип {type(object)}, а должен быть {need_type}")
    return object


def custom_sep_1():
    """
    Возвращает строку-разделитель
    :return (str): строка-разделитель
    """
    return "\n\n//////////////////////////////\n\n"


def custom_config_writer(self=None, sep=None, log_file_path=None, config=None):
    """
    Пример пользовательской функции записи конфигурации в лог

        :param self (class LogModule): объект логгера
        :param sep (calleble): Функцию, возвращающая разделитель
        :param log_file_path (str): Путь к файлу лога
        :param config (dict): Конфиг
        :return: None
    """
    if log_file_path is None:
        log_file_path = self.log_file_path
    if config is None:
        config = self.config
    if sep is None:
        sep = self.sep

    with open(log_file_path, 'a', encoding='utf-8') as f:
        for item in config.keys():
            f.write(f"\"{item}\"=\"{config[item]}\"\n")
        f.write(sep())


def custom_header_writer(self=None, sep=None, log_file_path=None, content=None):
    """
    Пример пользовательской функции записи заголовка в лог

        :param self (class LogModule): объект логгера
        :param sep (calleble): Функцию, возвращающая разделитель
        :param log_file_path (str): Путь к файлу лога
        :param content(str): Строка для записи в заголовок
        :return: None
    """
    if log_file_path is None:
        log_file_path = self.log_file_path
    if content is None:
        content = self.log_name
    if sep is None:
        sep = self.sep

    with open(log_file_path, 'a', encoding='utf-8') as f:
        f.write(f"{content}{sep()}")
    return


def find_checker(checker_name):
    """
    Ищет checker по имени

        :param checker_name (str): Название checker-
        :return (calleble): Найденный checker
    """
    #ищет нужный checker из нескольких возможных (мне стоит заготовить несколько)
    match checker_name:
        case "checker1":
            return check_format_1
        case _:  # default
            return check_format_1


def log_path_define(self, log_path):
    """
    Устанавливает значение полю log_path

        :param self (class LogModule): объект логгера
        :param log_path: путь к файлу лога
        :return: None
    """
    if log_path is None:
        if isinstance(self.config, dict):
            if "log_path" in self.config:
                self.log_path = self.config["log_path"]
            else:
                raise ValueError("Ошибка: log_path должен быть задан (через конфиг либо парамтером)")
        elif isinstance(self.config, str):  # дополнительная опция
            self.log_path = self.config
            # raise ValueError("Ошибка: log_path должен быть задан (через конфиг либо парамтером)")


def checker_define(self, checker):
    """
    Устанавливает значение полю checker

        :param self (class LogModule): объект логгера
        :param checker (calleble): Приоритетное значение checker
        :return: None
    """
    if checker is None:
        if isinstance(self.config, dict):  # следующая проверка требует это условие
            if "checker" in self.config:  # проверяем, есть ли checker в конфигурации
                self.checker = self.config["checker"]
            else:
                self.checker = find_checker("default")  # присваиваем значение по умолчанию
        else:
            self.checker = find_checker("default")  # присваиваем значение по умолчанию


def config_writer_define(self, config_writer):
    """
    Устанавливает значению полю config_writer

        :param self (class LogModule): объект логгера
        :param config_writer (calleble): Приоритетное значение config_writer
        :return: None
    """
    if config_writer is None:
        if isinstance(self.config, dict):
            if "config_writter" in self.config:
                self.config_writer = self.config["config_writer"]
            else:
                self.config_writer = self.default_config_writer
        else:
            self.config_writer = self.default_config_writer


def header_writer_define(self, header_writer):
    """
    Устанавливает значению полю header_writer

        :param self (class LogModule): Объект логгера
        :param header_writer (calleble): Приоритетное значение header_writer
        :return: None
    """
    if header_writer is None:
        if isinstance(self.config, dict):
            if "header_writer" in self.config:
                self.header_writer = self.config["header_writer"]
            else:
                self.header_writer = self.default_header_writer
        else:
            self.header_writer = self.default_header_writer


def writer_define(self, writer):
    """
    Устанавливает значению полю writer

        :param self (class LogModule): Объект логгера
        :param writer (calleble): Приоритетное значение writer
        :return: None
    """
    if writer is None:
        if isinstance(self.config, dict):
            if "writer" in self.config:
                self.writer = self.config["writer"]
            else:
                self.writer = self.default_writer
        else:
            self.writer = self.default_writer


def sep_define(self, sep):
    """
    Устанавливает значению полю sep

        :param self (class LogModule): Объект логгера
        :param sep (calleble): Приоритетное значение sep
        :return: None
    """
    if sep is None:
        if isinstance(self.config, dict):
            if "sep" in self.config:
                self.sep = self.config["sep"]
            else:
                self.sep = self.default_sep
        else:
            self.sep = self.default_sep


def name_comment_define(self, name_comment):
    """
    Устанавливает значению полю name_comment

        :param self (class LogModule): Объект логгера
        :param name_comment (calleble): Приоритетное значение name_comment
        :return: None
    """
    if name_comment is None:
        if isinstance(self.config, dict):
            if "name_comment" in self.config:
                self.name_comment = self.config["name_comment"]
            else:
                self.name_comment = self.default_name_comment()  # ладно всё это строка, пусть будет так
        else:
            self.name_comment = self.default_name_comment()


def check_log_path(log_path):
    """
    Проверяет, соответствует ли log_path требованиям
    (имеет тип str)

        :return (str):  Присвоенное значение
    """
    return checkType(log_path, str, "log_path")  # может быть надо сразу self.log_path


# log_path, checker, config_writer, header_writer, writer, sep, name_comment

def check_checker(checker):
    """
    Проверяет, соответствует ли checker требованиям
    (имеет тип callable)

        :return (callable):  Присвоенное значение
    """
    return checkType(checker, callable, "checker")


def check_config_writer(config_writer):
    """
    Проверяет, соответствует ли config_writer требованиям
    (имеет тип callable)

        :return (callable):  Присвоенное значение
    """
    return checkType(config_writer, callable, "config_writer")


def check_header_writer(header_writer):
    """
    Проверяет, соответствует ли header_writer требованиям
    (имеет тип callable)

        :return (callable):  Присвоенное значение
    """
    return checkType(header_writer, callable, "header_writer")


def check_writer(writer):
    """
    Проверяет, соответствует ли writer требованиям
    (имеет тип callable)

        :return (callable):  Присвоенное значение
    """
    return checkType(writer, callable, "writer")


def check_sep(sep):
    """
    Проверяет, соответствует ли sep требованиям
    (имеет тип callable)

        :return (callable):  Присвоенное значение
    """
    return checkType(sep, callable, "sep")


def check_name_comment(name_comment):
    """
    Проверяет, соответствует ли name_comment требованиям
    (имеет тип callable)

        :return (callable):  Присвоенное значение
    """
    return checkType(name_comment, callable, "name_comment")
