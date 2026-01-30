import os


def write_raw_txt(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(content))


def check_directory(path, service_name):
    service_dir_path = f"{path}\\{service_name}"
    if not os.path.isdir(service_dir_path):
        os.chdir(path)
        os.mkdir(service_name)


def write_host_pairs(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        for i in content:
            # извлекаем 2 адреса и список метрик (на случай если их количество будет в будущем меняться)
            addr_1, addr_2, *metrics = i
            f.write(f"{addr_1}-{addr_2} {metrics}\n")


def check_write(path, service_name, host_group_name_1, host_group_name_2, inf):
    check_directory(path, service_name)

    file_path = f"{path}\\{service_name}\\{host_group_name_1}-{host_group_name_2}.txt"
    write_raw_txt(file_path, inf)

    # то же имя, но с подчеркиванием в начале (для сортировки)
    file_path = f"{path}\\{service_name}\\_{host_group_name_1}-{host_group_name_2}.txt"
    write_host_pairs(file_path, inf)


def str_to_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)


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
