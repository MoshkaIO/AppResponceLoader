import module_write_text as wr_module
import pandas as pd

def xlsx_to_csv(xlsx_file_path, output_path, ignore_rows=0, header_row_index=3):
    """
    Конвертирует все листы таблицы xlsx в csv формат и записывает в одноименные файлы

    :param xlsx_file_path (str): путь к xlsx файлу
    :param output_path (str): путь к папке для записи результа
    :param ignore_rows (int): количество строк, которые надо проигнорировать
    :param header_row_index (int): номер строки, которую нужно использовать как заголовок csv-файла
    :return: None
    """
    excel_file = pd.ExcelFile(xlsx_file_path)

    for sheet_name in excel_file.sheet_names:
        csv_content = xlsx_sheet_to_csv(excel_file, sheet_name, ignore_rows)

        csv_header = xlsx_row_to_csv_row(excel_file, sheet_name, header_row_index)

        content = f"{csv_header}\n{csv_content}"
        content = '\n'.join(line for line in content.splitlines() if line.strip())

        output_file_path = f"{output_path}\\{sheet_name}.csv" # составляем путь к файлу по имени листа

        wr_module.str_to_file(output_file_path, content)  # используем простую запись текста в файл


def xlsx_sheet_to_csv(excel_file, sheet_name, ignore_rows):
    """
    Преобразует содержимое листа xlsx таблицы в csv формат

        :param excel_file (class ExcelFile): объект таблицы
        :param sheet_name (str): Название листа
        :param ignore_rows (int): Сколько строк таблиц проигнорировать
        :return (str): Содержимое листа в формате csv
    """
    df = pd.read_excel(excel_file, sheet_name=sheet_name, skiprows=ignore_rows)

    return df.to_csv(index=False, encoding='utf-8', sep=";")


def xlsx_row_to_csv_row(excel_file, sheet_name, row_index):
    """
    Преобразует строку с листа xlsx таблицы в csv формат

        :param excel_file (class ExcelFile): объект таблицы
        :param sheet_name (str): Название листа
        :param row_index (int): Номер строки, которую нужно преобразовать
        :return (str): Содержимое строки листа в формате csv
    """
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    row = df.iloc[row_index]
    csv_row = ';'.join(map(str, row))

    return csv_row





def test_xlsx_to_csv():
    xlsx_file_path = "C:\\Users\\mioffe\\Documents\\Проекты\\RSHBMON2\\входные данные\\scriptHostPairs\\CHECKSERVICES v2.xlsx"
    output_path = "C:\\Users\\mioffe\\Documents\\Проекты\\RSHBMON2\\входные данные\\scriptHostPairs"
    ignore_rows_count = 5
    xlsx_to_csv(xlsx_file_path, output_path, ignore_rows=ignore_rows_count)


def test_xlsx_to_csv2():
    xlsx_file_path = "C:\\Users\\mioffe\\Documents\\Проекты\\RSHBMON2\\входные данные\\scriptHostPairs\\CHECKSERVICES v2.xlsx"
    output_path = "C:\\Users\\mioffe\\Documents\\Проекты\\RSHBMON2\\входные данные\\scriptHostPairs\\ServicesHostGroupPairs"
    ignore_rows_count = 5
    header_row_index = 3
    xlsx_to_csv(xlsx_file_path, output_path, ignore_rows=ignore_rows_count, header_row_index=2)


if __name__ == "__main__":
    test_xlsx_to_csv2()
