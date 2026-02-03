import csv
import os
import json


# Считывание ID хостгрупп
def read_hostgroup_ids(filepath):
    """
    Считывает id хост-групп из файла

        :param filepath (str): путь к файлу
        :return (dict): Словарь, ключ - имя хост группы, значение - id
    """
    hostgroups = {}
    with open(filepath, mode='r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        next(csv_reader)  # Пропускаем заголовок
        for row in csv_reader:
            hostgroup_id = row[0]
            hostgroup_name = row[1]
            hostgroups[hostgroup_name] = int(hostgroup_id)

    return hostgroups


# def read_id_hostgroups(path):
#
#     hostgroups = {}
#     with open(path, mode='r', newline='') as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=';')
#         # Пропускаем заголовок
#         next(csv_reader)
#         for row in csv_reader:
#             hostgroup_id = row[0]
#             hostgroup_name = row[1]
#             hostgroups[int(hostgroup_id)] = hostgroup_name
#
#     return hostgroups




def read_hostgroup_pairs(path, file_list): # Считывание пар хост-групп в пределах сервиса
    """
    Определяет список пар хост-групп для каждого сервиса

        :param path (str): Путь к папке с файлами, содержащими пары хостов для каждого сервиса
        :param file_list (list(str)): Список имен файлов
        :return (dict): Словарь, где ключ - имя сервиса (str), значение - список пар хост-групп [list(str)]
    """
    services = {}
    for filename in file_list:
        name = filename.replace('.csv', '')
        pair_list = []
        with open(f"{path}\\{filename}", mode='r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            next(csv_reader)
            for row in csv_reader:
                hostgroup_pair = row[0]
                pair_list.append(hostgroup_pair) # складируем списки пар для каждого сервиса в словарь
        services[name] = pair_list # название сервиса - ключ к списку пар

    return services



def filter_csv_files(path): # проверяет директорию, возвращает список имен csv файлов
    """
    Возвращает список имен csv-файлов в папке

        :param path (str): путь к папке
        :return (list(str)): Список имен csv-файлов
    """
    return filter_files(path, "csv")


def filter_txt_files(path):
    """
    Возвращает список имен txt-файлов в папке

        :param path (str): путь к папке
        :return (list(str)): Список имен txt-файлов
    """
    return filter_files(path, "txt")


def filter_files(path, extension):
    """
    Возвращает список имен файлов с расширением extension

        :param path (str): Путь к папке с файлами
        :param extension (str): Расширение файла
        :return (list(str)): Список имен extension-файлов
    """
    files = os.listdir(path)
    filtered = []
    for i in files:
        if i.endswith(f".{extension}"):
            filtered.append(i)

    return filtered


def read_services(path):
    """
    Определяет список пар хост-групп для каждого сервиса, описанного в .csv файлах в папке path

        :param path (str): Путь к папке
        :return (dict): Словарь, где ключ - имя сервиса (str), значение - список пар хост-групп [list(str)]
    """
    file_list = filter_csv_files(path)
    services = read_hostgroup_pairs(path, file_list)
    return services


def read_config(file_path):
    """
    Считывает конфигурацию из файла

        :param file_path (str): Файл конфигурации
        :return (dict): Конфигурация
    """
    f = open(file_path, 'r', encoding="utf-8")  # дополнительно обозначил кодировку, т.к. json выдает cp-1251
    config = json.load(f)
    return config


def test_read_hostgroup_pairs():
    path = "C:\\Users\\mioffe\\Documents\\Проекты\\RSHBMON2\\входные данные\\scriptHostPairs\\ServicesHostGroupPairs"
    file_list = filter_csv_files(path)
    services = read_hostgroup_pairs(path, file_list)
    print(services)
    return services


def test_read_hostgroup_ids():
    path = "C:\\Users\\mioffe\\Documents\\Проекты\\RSHBMON2\\входные данные\\scriptHostPairs\\host_group_ids.csv"
    result = read_hostgroup_ids(path)
    print(result["IS_ABS_CFT--AppServers"])
    print(result["IS_ABS_CFT--ActiveMQ"])
    return result


def test_read_config():
    config_file = "C:\\Users\\mioffe\\Documents\\Проекты\\RSHBMON2\\входные данные\\scriptHostPairs\\config\\test_config.txt"
    result = read_config(config_file)
    print(result)
    print(type(result))


if __name__ == "__main__":
    # test_read_hostgroup_ids()
    # test_read_hostgroup_pairs()
    test_read_config()


# new commit from main (no testing!!!1!) 3