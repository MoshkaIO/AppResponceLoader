from steelscript.appresponse.core.appresponse import AppResponse
from steelscript.common import UserAuth
from steelscript.appresponse.core.reports import DataDef, Report
from steelscript.appresponse.core.types import Key, Value, TrafficFilter
from steelscript.appresponse.core.reports import SourceProxy


def find_host_pairs_between_hostgroups(ar, host_group_id_1, host_group_id_2, start, end):
    """
    Делает запрос всех пар хостов между двумя хост-группами в указанный промежуток

    :param ar (class AppResponce): специальный объект для взаимодействия с сервисом AppResponce
    :param host_group_id_1 (int): id первой хост-группы
    :param host_group_id_2 (int): id второй хост-группы
    :param start (int): начало временного интервала (unix timestamp)
    :param end (int): конец временного интервала (unix timestamp)
    :return: список кортежей, состоящих из пар хостов и числа активных соединений между ними
    """
    report = Report(ar)

    columns = [
        Key('tcp.ip'),
        Key('conn_tcp.ip'),
        Value('sum_tcp.active_connections')
    ]

    data_def = DataDef(source=SourceProxy(name='aggregates'),
                       columns=columns, start=start, end=end,
                       topbycolumns=[Value('sum_tcp.active_connections')],
                       granularity=0,
                       limit=25,
                       )
    data_def.add_filter(
        TrafficFilter(f"host_group.id=='{host_group_id_1}' and conn_host_group.id=='{host_group_id_2}'"))
    report.add(data_def)

    report.run()
    data = report.get_data()
    return data


def create_ar_entity(addr, login, password):
    """
    Создание объекта для взаимодействия с сервисом AppResponce

    :param addr (str): Адрес сервиса
    :param login (str): Логин для авторизации
    :param password (str): Пароль для авторизации
    :return (class AppResponce): Объекта для взаимодействия с сервисом AppResponce
    """
    return AppResponse(addr,
                       auth=UserAuth(login, password))


def test_find_host_pairs_between_hostgroups():
    ar = AppResponse('127.0.1.1',
                     auth=UserAuth('admin', 'admin'))
    # IS_AS_EFR--AppServers   >   IS_AS_EFR--ActiveMQServers  220 > 219
    start = 1769418900
    end = 1769422500
    result=find_host_pairs_between_hostgroups(ar, 220, 219, start, end)
    print(result)
    return result


if __name__ == "__main__":
    test_find_host_pairs_between_hostgroups()
