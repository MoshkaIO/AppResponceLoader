import os


def write_raw_txt(filepath, content):
    """
    Записывает нечто в виде строки в файл

        :param filepath (str):  Путь к файлу
        :param content (?): Строка для записи в файл
        :return: None
    """
    str_to_file(filepath, str(content))
    # with open(filepath, 'w', encoding='utf-8') as f:
    #     f.write(str(content))


def check_directory(path, service_name):
    """
    Проверяет, есть ли папка с именем сервиса в каталоге path

        :param path (str): Проверяемая папка
        :param service_name (str): Имя сервиса
        :return: None
    """
    service_dir_path = f"{path}\\{service_name}"
    if not os.path.isdir(service_dir_path):
        os.chdir(path)
        os.mkdir(service_name)


def write_host_pairs(filepath, content):
    """
    Записывает пары хостов и список их метрик в файл в форматированном виде

        :param filepath (str): Путь к файлу
        :param content (list(int,int,?): список кортежей пар хостов и их метрик
        :return:
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        for i in content: #перебираем все пары хостов
            # извлекаем 2 адреса и список метрик (на случай если их количество будет в будущем меняться)
            addr_1, addr_2, *metrics = i
            f.write(f"{addr_1}-{addr_2} {metrics}\n")


def check_write(path, service_name, host_group_name_1, host_group_name_2, inf):
    """
    Проверяет папку и записывает в неё данные в сыром и форматированном виде

        :param path (str): Путь к папке для записи
        :param service_name (str): имя сервиса
        :param host_group_name_1 (str): имя первой хост-группы
        :param host_group_name_2 (str): имя второй хост-группы
        :param inf (list(int,int,?): данные для записи
        :return: None
    """
    check_directory(path, service_name) # Проверяем наличие папки

    file_path = f"{path}\\{service_name}\\{host_group_name_1}-{host_group_name_2}.txt"
    write_raw_txt(file_path, inf)

    # то же имя, но с подчеркиванием в начале (для сортировки)
    file_path = f"{path}\\{service_name}\\_{host_group_name_1}-{host_group_name_2}.txt"
    write_host_pairs(file_path, inf)  # запись в форматированном виде


def str_to_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)


def add_header(file_path, header):
    """
    Вставляет строку в начало файла

        :param file_path (str): путь к файлу
        :param header (str): Строка для вставки
        :return: None
    """
    content = []
    with open(file_path, 'r') as file:
        content = file.readlines()
    # Добавляем новую строку в начало
    content.insert(0, header + '\n')

    # Записываем обратно в файл
    with open(file_path, 'w') as file:
        file.writelines(content)


def test_write_raw_txt():
    inf = [('10.19.77.18', '10.19.77.11', 2449), ('10.19.77.51', '10.19.77.11', 1988)]
    path = "C:\\Users\\mioffe\\Documents\\Проекты\\RSHBMON2\\выходные данные\\scriptHostPairs"
    host_group_name_1 = "IS_AS_EFR--AppServers"
    host_group_name_2 = "IS_AS_EFR--ActiveMQServers"
    service_name = "IS_AS_EFR"

    check_directory(path, service_name)

    file_path = f"{path}\\{service_name}\\{host_group_name_1}-{host_group_name_2}.txt"
    write_raw_txt(file_path, inf)

    print("test_write_raw_txt() finished")


def test_write_host_pairs():
    test_txt = [('10.19.77.18', '10.19.77.11', 2449), ('10.19.77.51', '10.19.77.11', 1988)]
    path = "C:\\Users\\mioffe\\Documents\\Проекты\\RSHBMON2\\выходные данные\\scriptHostPairs"
    host_group_name_1 = "IS_AS_EFR--AppServers"
    host_group_name_2 = "IS_AS_EFR--ActiveMQServers"
    service_name = "IS_AS_EFR"

    check_directory(path, service_name)

    file_path = f"{path}\\{service_name}\\_{host_group_name_1}-{host_group_name_2}.txt"

    write_host_pairs(file_path, test_txt)
    print("test_write_host_pairs() finished")


def test_write_all():
    test_txt = [('10.19.77.18', '10.19.77.11', 2449), ('10.19.77.51', '10.19.77.11', 1988)]
    path = "C:\\Users\\mioffe\\Documents\\Проекты\\RSHBMON2\\выходные данные\\scriptHostPairs"
    host_group_name_1 = "IS_AS_EFR--AppServers"
    host_group_name_2 = "IS_AS_EFR--ActiveMQServers"
    service_name = "IS_AS_EFR"

    check_write(path, service_name, host_group_name_1, host_group_name_2, test_txt)
    print("test_write_all() finished")


if __name__ == "__main__":
    # test_write_raw_txt()
    # test_write_host_pairs()
    test_write_all()
