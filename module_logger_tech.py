from datetime import datetime
import re


# технические функции логгера
def today_str():
    now = datetime.now()
    return now.strftime("%d.%m.%Y")
    # return f"{now.day}.{now.month}.{now.year}"


def time_str():
    now = datetime.now()
    return f"{now.hour}-{now.minute}"


def time_hh_mm_ss_str():
    now = datetime.now()
    return f"{now.hour}-{now.minute}-{now.second}"


def check_format_1(content):
    return re.search(r'\(\d+\.\d+\) \d\d\.\d\d\.\d{4} \d\d-\d\d.*', content)


def check_format_2(content):
    return re.search(r'\(\d+\.\d+\).*', content)


def find_launch_num(filename):
    return int(re.findall(r'\d+', filename)[1])


def find_launch_date(filename):
    return re.search(r'\d\d\.\d\d\.\d{4}', filename)[0]


def find_launch_day(filename):
    return int(re.findall(r'\d+', filename)[0])


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
    return "\n\n//////////////////////////////\n\n"


def custom_config_writer(self=None, sep=None, log_file_path=None, config=None):
    """
    Пример пользовательской функции записи конфигурации в лог
    :param self:
    :param sep:
    :param log_file_path:
    :param config:
    :return:
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

    :param self:
    :param sep:
    :param log_file_path:
    :param content:
    :return:
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
    #ищет нужный checker из нескольких возможных (мне стоит заготовить несколько)
    match checker_name:
        case "checker1":
            return check_format_1
        case _:  # default
            return check_format_1


def log_path_define(self, log_path):
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

    :param self: объкт, содержащий поле checker
    :param checker: Приоритетное значение checker
    :return:
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
    if config_writer is None:
        if isinstance(self.config, dict):
            if "config_writter" in self.config:
                self.config_writer = self.config["config_writer"]
            else:
                self.config_writer = self.default_config_writer
        else:
            self.config_writer = self.default_config_writer


def header_writer_define(self, header_writer):
    if header_writer is None:
        if isinstance(self.config, dict):
            if "header_writer" in self.config:
                self.header_writer = self.config["header_writer"]
            else:
                self.header_writer = self.default_header_writer
        else:
            self.header_writer = self.default_header_writer


def writer_define(self, writer):
    if writer is None:
        if isinstance(self.config, dict):
            if "writer" in self.config:
                self.writer = self.config["writer"]
            else:
                self.writer = self.default_writer
        else:
            self.writer = self.default_writer


def sep_define(self, sep):
    if sep is None:
        if isinstance(self.config, dict):
            if "sep" in self.config:
                self.sep = self.config["sep"]
            else:
                self.sep = self.default_sep
        else:
            self.sep = self.default_sep


def name_comment_define(self, name_comment):
    if name_comment is None:
        if isinstance(self.config, dict):
            if "name_comment" in self.config:
                self.name_comment = self.config["name_comment"]
            else:
                self.name_comment = self.default_name_comment()  # ладно всё это строка, пусть будет так
        else:
            self.name_comment = self.default_name_comment()


def check_log_path(log_path):
    return checkType(log_path, str, "log_path")  # может быть надо сразу self.log_path


# log_path, checker, config_writer, header_writer, writer, sep, name_comment

def check_checker(checker):
    """ Проверка, что checker является callable"""
    return checkType(checker, callable, "checker")


def check_config_writer(config_writer):
    return checkType(config_writer, callable, "config_writer")


def check_header_writer(header_writer):
    return checkType(header_writer, callable, "header_writer")


def check_writer(writer):
    return checkType(writer, callable, "writer")


def check_sep(sep):
    return checkType(sep, callable, "sep")


def check_name_comment(name_comment):
    return checkType(name_comment, callable, "name_comment")
