import module_read_text as read_module
import module_logger_tech as tech


class LogModule:

    def __init__(self, config={}, log_path=None, checker=None, config_writer=None,
                 header_writer=None, writer=None, sep=None,  name_comment=None):
        # приоритет за параметрами, переданными напрямую
        # если параметр None, то проверяется config
        # если нет в конфиге, то вызывается default (кроме log_path)


        self.config = config

        self.checker=checker
        self.config_writer=config_writer
        self.header_writer=header_writer
        self.writer=writer
        self.sep=sep
        self.name_comment=name_comment

        self.log_name = "" #добавление log_name как отдельной кастомной сущности откладывается
        self.log_file_path = ""  # объявил заранее для удобства
        self.num_of_writes = 0  # количество использований функции self.write()

        self.define_params(log_path, checker, config_writer, header_writer, writer, sep, name_comment)
        self.check_params()
        # print("прошли через проверку")
        self.create_log()  # создаем лог

    def define_params(self, log_path, checker, config_writer, header_writer, writer, sep, name_comment):
        """ Определяет, какое значение присвоить каждому полю
            (Полученное напрямую в __init__ / полученное через config / по умолчанию)
        """
        tech.log_path_define(self, log_path)
        tech.checker_define(self, checker)
        tech.config_writer_define(self, config_writer)
        tech.header_writer_define(self, header_writer)
        tech.writer_define(self, writer)
        tech.sep_define(self, sep)
        tech.name_comment_define(self, name_comment)

    def check_params(self):
        """
        Проверяет типы данных в основных полях.
        В случае ошибки вызывается ValueError
        :return:
        """
        tech.check_log_path(self.log_path)
        tech.check_checker(self.checker)
        tech.check_header_writer(self.header_writer)
        tech.check_config_writer(self.config_writer)
        tech.check_writer(self.writer)
        tech.check_sep(self.sep)
        tech.check_name_comment(self.name_comment)


    def create_log(self):
        """
        Определяет имя нового лога, создает его, записывает в него заголовок и конфигурацию
        :return: (str) Путь к файлу созданного лога
        """
        last_report = self.find_last_log()
        print(f"предыдущий лог: {last_report}")
        if last_report is None:  # если предыдущий отчет не найден
            last_launch_num = 0
            last_launch_day = 1
            last_launch_date = tech.today_str()
        else:
            last_launch_day, last_launch_num, last_launch_date = last_report

        now_launch_num = last_launch_num + 1
        now_launch_day = last_launch_day
        now_launch_date = tech.today_str()
        now_launch_time = tech.time_str()

        if now_launch_date != last_launch_date:
            now_launch_day = last_launch_day + 1

        self.log_name = f"({now_launch_day}.{now_launch_num}) {now_launch_date} {now_launch_time} {self.name_comment}"
        self.log_file_path = f"{self.log_path}\\{self.log_name}.txt"
        with open(self.log_file_path, 'w', encoding='utf-8') as f:
            self.header_writer(sep=self.sep, log_file_path=self.log_file_path, content=self.log_name)
            self.config_writer(sep=self.sep, log_file_path=self.log_file_path, config=self.config)

        return self.log_file_path

    def find_last_log(self):
        """
        Находит последний отчет (лог)

        Аргументы:
            Нет

        Возвращаемое значение:
            (int,int,int): День последнего отчета, номер последнего отчета, дата последнего отчета

        Функция ищет последний лог в директории, чтобы правильно проименовать текущий
        При этом учитываются только логи, отобранные по формату функцией filter_format
        Если лог не будет найден, то нумерация начнется с дня 0, запуска 0.
        :return:
        """

        txt_files = read_module.filter_txt_files(self.log_path)
        formatted_files = self.filter_format(txt_files)

        if formatted_files == []:
            print("Внимание! Предыдущий лог не найден!")
            return None

        last_launch_num = 0
        last_launch_day = 0
        last_launch_date = ""

        for file in formatted_files:
            launch_num = tech.find_launch_num(file)
            launch_day = tech.find_launch_day(file)
            if launch_day > last_launch_day:
                last_launch_day = launch_day
                last_launch_num = launch_num
                last_launch_date = tech.find_launch_date(file)
            elif launch_day == last_launch_day and launch_num > last_launch_num:
                last_launch_num = launch_num
                last_launch_date = tech.find_launch_date(file)

        return last_launch_day, last_launch_num, last_launch_date

    def filter_format(self, contents):
        """
        Находит строки, которые проходят через self.checker

        :param
            contents (list(str)): список строк для проверки
        :return:
            list(str): список подходящих строк
        """
        result = []
        for content in contents:
            if self.checker(content):
                result.append(content)

        return result

    def write(self, content):
        """
        Записывает строку в лог и увеличивает счетчик

        :param content (str): Строка для записи в лог
        :return:
        """
        self.num_of_writes += 1
        self.writer(content)
        return

    def default_header_writer(self=None, sep=None, log_file_path=None, content=None):
        """
        Записывает заголовок лога

        Аргументы:
            :param sep (calleble): Разделитель, отделяющий заголовок от остального лога
            :param log_file_path (str): Путь к файлу лога
            :param content (str): Строка, которую записывают в качестве заголовка

        Возвращаемое значение:
            :return: Результат (boolean)
        """
        # заголовок для краткого описания. По умолчанию просто дублирует имя
        if log_file_path is None:
            log_file_path = self.log_file_path
        if content is None:
            content = self.log_name
        if sep is None:
            sep = self.sep

        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(f"log started:\"{content}\"{sep()}{sep()}")
        return True

    def default_config_writer(self=None, sep=None, log_file_path=None, config=None):
        """
        Записывает конфигурацию в лог

        Аргументы:
            :param sep (calleble):
            :param log_file_path (str):
            :param config (dict(str:str):
        :return:
        """
        if log_file_path is None:
            log_file_path = self.log_file_path
        if config is None:
            config = self.config
        if sep is None:
            sep = self.sep

        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(f"config: \n\n")
            for item in config.keys():
                f.write(f"\"{item}\"=\"{config[item]}\"\n")
            f.write(sep())

    def default_writer(self=None, content=""):
        with open(self.log_file_path, 'a', encoding='utf-8') as f:
            f.write(f"{tech.today_str()} {tech.time_str()}|| {str(content)}")
            f.write(self.sep())

    def default_sep(self=None):
        return "\n\n======\n\n"

    def default_name_comment(self=None):
        return ""

    def __str__(self):
        return f"log_file_path: {self.log_file_path}"

    def __repr__(self):
        return (f"log_file_path: {self.log_file_path} \n"
                f"num_of_writes: {self.num_of_writes}\n"
                f"{self.config}")

    def __len__(self):
        return self.num_of_writes

    def __eq__(self, other):
        return (self.log_file_path == other.self.log_file_path)


def test_LogModule_default():
    config = dict(
        log_path="C:\\Users\\mioffe\\Documents\\Проекты\\RSHBMON2\\выходные данные\\scriptHostPairs\\_LOG")
    logger = LogModule(config)
    logger.write("Это проверка test_LogModule_default()\n предполагается, что ничего не сломалось")
    print("test_LogModule_default() finished ")

def test_LogModule_custom():
    config = dict(
        log_path="C:\\Users\\mioffe\\Documents\\Проекты\\RSHBMON2\\выходные данные\\scriptHostPairs\\_LOG",
        sep=tech.custom_sep_1,
        checker=tech.check_format_2,
        config_writer=tech.custom_config_writer,
        header_writer=tech.custom_header_writer)
    logger = LogModule(config)
    logger.write("Это проверка test_LogModule_custom()\n предполагается, что ничего не сломалось")
    #print("test_LogModule_custom() finished ")

def test_LogModule_documentation():
    config = dict(
        log_path="C:\\Users\\mioffe\\Documents\\Проекты\\RSHBMON2\\выходные данные\\scriptHostPairs\\_LOG")

    logger = LogModule(config)
    logger.write("Это проверка test_LogModule_default()\n предполагается, что ничего не сломалось")
    print(logger.find_last_log.__doc__)
    print("test_LogModule_documentation() finished ")


if __name__ == "__main__":
    test_LogModule_default()
    # test_LogModule_custom()


# git change
#change 2
#change 3 for commit 2

