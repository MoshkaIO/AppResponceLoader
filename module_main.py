import module_write_text as wr_module
import module_find_pair as find_module
import module_read_text as read_module
import module_logger as log_module
from datetime import datetime

class MainModule:

    def __init__(self, config):

        self.config = self.check_config(config)

        self.hostgroup_id_path = self.config["hostgroup_id_path"]
        self.hostgroup_pair_path = self.config["hostgroup_pair_path"]
        self.host_pair_path = self.config["host_pair_path"]
        self.log_path = self.config["log_path"]
        self.addr = self.config["addr"]
        self.login = self.config["login"]
        self.password = self.config["password"]

        self.hostgroup_ids = {}  # ключ: имя   значение: id
        self.services = {}
        self.ar = None
        self.log = None
        self.start = None
        self.end = None

        self.run()

    def check_config(self, config):
        if isinstance(config, str):  # предполагается, что это путь к файлу конфигурации
            return read_module.read_config(config)
        if isinstance(config, dict):
            return config

    def run(self):

        self.create_log()
        self.start = 1769418900
        self.end = 1769422500

        self.report_time()
        self.hostgroup_ids = read_module.read_hostgroup_ids(self.hostgroup_id_path)
        self.services = read_module.read_services(self.hostgroup_pair_path)

        self.ar = find_module.create_ar_entity(self.addr, self.login, self.password)

        self.cycle()

    def create_log(self):
        self.log = log_module.LogModule(self.config)

    def cycle(self):
        for service in self.services.keys():
            hostgroup_pairs = self.services[service]
            for hostgroup_pair in hostgroup_pairs:
                items = hostgroup_pair.split("-")
                host_group_name_1 = f"{service}--{items[0]}"
                host_group_name_2 = f"{service}--{items[1]}"

                try:
                    result = self.iteration(host_group_name_1, host_group_name_2)
                    self.log.write(result)
                    self.write(service, host_group_name_1, host_group_name_2, result)

                except KeyError as err:
                    self.message(f"Not found {err}")
                    continue

                except Exception as err:
                    self.message(f"Unexpected {err=}, {type(err)=}")
                    continue

    def iteration(self, host_group_name_1, host_group_name_2):
        host_group_id_1 = self.hostgroup_ids[host_group_name_1]
        host_group_id_2 = self.hostgroup_ids[host_group_name_2]
        self.message(f"iteration {host_group_name_1} <---> {host_group_name_2}")
        result = find_module.find_host_pairs_between_hostgroups(self.ar, host_group_id_1, host_group_id_2, self.start,
                                                                self.end)
        return result

    def message(self, content):  # и в лог и в консоль
        self.log.write(content)
        print(content)

    def write(self, service_name, host_group_name_1, host_group_name_2, result):
        wr_module.check_write(self.host_pair_path, service_name, host_group_name_1, host_group_name_2, result)

    def report_time(self):  #эту функцию лучше вынести в отдельный технический файл
        start_time=self.config["start_time"]
        end_time=self.config["end_time"]
        #парсим дату и время из строки и переводим в unix timestamp
        self.start=datetime.strptime(start_time,"%d.%m.%Y %H:%M").timestamp()
        self.end = datetime.strptime(end_time, "%d.%m.%Y %H:%M").timestamp()


def test1():
    find_module.test_find_host_pairs_between_hostgroups()
    wr_module.test_write_raw_txt()
    print("test1 finished")


def test2():
    # IS_AS_EFR--AppServers   >   IS_AS_EFR--ActiveMQServers  220 > 219
    start = 1769418900
    end = 1769422500
    ar = find_module.create_ar_entity("127.0.1.1", "admin", "admin")
    result = find_module.find_host_pairs_between_hostgroups(ar, 220, 219, start, end)
    path = "C:\\Users\\mioffe\\Documents\\Проекты\\RSHBMON2\\выходные данные\\scriptHostPairs"
    host_group_name_1 = "IS_AS_EFR--AppServers"
    host_group_name_2 = "IS_AS_EFR--ActiveMQServers"
    service_name = "IS_AS_EFR"
    wr_module.check_write(path, service_name, host_group_name_1, host_group_name_2, result)


def default_config():
    config = {
        "hostgroup_id_path": "C:\\Users\\mioffe\\Documents\\Проекты\\RSHBMON2\\входные данные\\scriptHostPairs\\host_group_ids.csv",
        "hostgroup_pair_path": "C:\\Users\\mioffe\\Documents\\Проекты\\RSHBMON2\\входные данные\\scriptHostPairs\\testPairs",
        "log_path": "C:\\Users\\mioffe\\Documents\\Проекты\\RSHBMON2\\выходные данные\\scriptHostPairs\\_LOG",
        "host_pair_path": "C:\\Users\\mioffe\\Documents\\Проекты\\RSHBMON2\\выходные данные\\scriptHostPairs",
        "addr": "127.0.1.1",
        "login": "admin",
        "password": "admin"}
    return config


def launch_with_config(config_file):
    config = read_module.read_config(config_file)
    process = MainModule(config)


def test4():
    config = default_config()
    process = MainModule(config)


def test5():
    config_file = "C:\\Users\\mioffe\\Documents\\Проекты\\RSHBMON2\\входные данные\\scriptHostPairs\\config\\test_config.txt"
    launch_with_config(config_file)


def test6():
    croc_config_file = ("C:\\Users\\mioffe\\Documents\\Проекты\\RSHBMON2\\входные данные"
                        "\\scriptHostPairs\\config\\CROC_default_config.txt")
    dl_config_file = ("C:\\Users\\mioffe\\Documents\\Проекты\\RSHBMON2\\входные данные"
                      "\\scriptHostPairs\\config\\DL_default_config.txt")

    launch_with_config(croc_config_file)
    launch_with_config(dl_config_file)


if __name__ == "__main__":
    test6()
