import module_write_text as wr_module
import pandas as pd

def xlsx_to_csv(xlsx_file_path, output_path, ignore_rows=0, header_row_index=3):
    excel_file = pd.ExcelFile(xlsx_file_path)

    for sheet_name in excel_file.sheet_names:
        csv_content = xlsx_sheet_to_csv(excel_file, sheet_name, ignore_rows, output_path)

        csv_header = xlsx_row_to_csv_row(excel_file, sheet_name, header_row_index)

        content = f"{csv_header}\n{csv_content}"
        # content=f"{csv_content}"
        content = '\n'.join(line for line in content.splitlines() if line.strip())

        output_file_path = f"{output_path}\\{sheet_name}.csv"

        wr_module.str_to_file(output_file_path, content)
        # add_header(csv_file_path, csv_row)
        # print(f"Сохранен: {csv_file_name}")


def xlsx_sheet_to_csv(excel_file, sheet_name, ignore_rows, output_path):
    df = pd.read_excel(excel_file, sheet_name=sheet_name, skiprows=ignore_rows)

    csv_file_path = f"{output_path}\\{sheet_name}.csv"
    # df.to_csv( index=False, encoding='utf-8', sep=";")

    return df.to_csv(index=False, encoding='utf-8', sep=";")


def xlsx_row_to_csv_row(excel_file, sheet_name, row_index):
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    row = df.iloc[row_index]
    csv_row = ';'.join(map(str, row))

    return csv_row


def add_header(file_path, header):
    content = []
    with open(file_path, 'r') as file:
        content = file.readlines()
    # Добавляем новую строку в начало
    content.insert(0, header + '\n')

    # Записываем обратно в файл
    with open(file_path, 'w') as file:
        file.writelines(content)


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
