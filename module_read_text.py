import csv
import os
import json


# Считывание ID хостгрупп
def read_hostgroup_ids(path):
    hostgroups = {}
    with open(path, mode='r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        # Пропускаем заголовок
        next(csv_reader)
        for row in csv_reader:
            hostgroup_id = row[0]
            hostgroup_name = row[1]
            hostgroups[hostgroup_name] = int(hostgroup_id)

    return hostgroups


def read_id_hostgroups(path):
    hostgroups = {}
    with open(path, mode='r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        # Пропускаем заголовок
        next(csv_reader)
        for row in csv_reader:
            hostgroup_id = row[0]
            hostgroup_name = row[1]
            hostgroups[int(hostgroup_id)] = hostgroup_name

    return hostgroups


# Считывание пар хост-групп в пределах сервиса

def read_hostgroup_pairs(path, file_list):
    # складируем списки пар для каждого сервиса в словарь
    # название сервиса - ключ к списку пар
    services = {}
    for filename in file_list:
        name = filename.replace('.csv', '')
        pair_list = []
        with open(f"{path}\\{filename}", mode='r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            next(csv_reader)
            for row in csv_reader:
                hostgroup_pair = row[0]
                pair_list.append(hostgroup_pair)
        services[name] = pair_list

    return services


# проверяет директорию, возвращает список имен csv файлов
def filter_csv_files(path):
    return filter_files(path, "csv")


def filter_txt_files(path):
    return filter_files(path, "txt")


def filter_files(path, extension):
    files = os.listdir(path)
    filtered = []
    for i in files:
        if i.endswith(f".{extension}"):
            filtered.append(i)

    return filtered


def read_services(path):
    file_list = filter_csv_files(path)
    services = read_hostgroup_pairs(path, file_list)
    # print(services)
    return services


def read_config(file_path):
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