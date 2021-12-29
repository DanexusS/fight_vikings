import csv
import string
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QWidget, QMessageBox
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QTableWidgetItem, QApplication


def check_title(title):
    for i in range(ord("a"), ord("z") + 1):
        if chr(i) in title.lower():
            return True
    for i in range(ord("а"), ord("я") + 1):
        if chr(i) in title.lower():
            return True
    return False


def check_file_name(file_name):
    restricted_symbols = string.punctuation
    numbers = string.digits

    for symbol in restricted_symbols:
        if symbol in file_name:
            return False
    for num in numbers:
        if num in file_name:
            return True
    return check_title(file_name)


"""
    -=-=-=-=-=-=-=-=-=-  РЕДАКТОР ПРЕДМЕТОВ  -=-=-=-=-=-=-=-=-=-
"""


class DatabaseEditor(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("items_edit_widget.ui", self)
        self.save = uic.loadUi("save_items_widget.ui")

        with open("items_database.csv", encoding="utf8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)

        self.item_headers = ["Название"]
        self.items_database = [{"Название": ""}]
        self.header_id = None
        self.header_type = ""

        self.table.setRowCount(1)
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(self.item_headers)
        self.table.setItem(0, 0, QTableWidgetItem(""))
        self.item_table_list = [[self.table.item(0, 0)]]

        """
            Настройка основного редактора предметов
        """
        self.add_line_btn.clicked.connect(self.add_row)
        self.save_btn.clicked.connect(lambda: self.save.show())
        self.delete_selected_btn.clicked.connect(self.delete_selected)

        self.table.itemChanged.connect(self.item_edited)
        self.table.horizontalHeader().sectionDoubleClicked.connect(self.change_horizontal_header)
        self.table.horizontalHeader().sectionClicked.connect(self.column_range_clicked)
        self.table.verticalHeader().sectionClicked.connect(self.row_range_clicked)
        self.table.itemClicked.connect(lambda: self.delete_selected_btn.setEnabled(True))
        self.table.clicked.connect(self.hide_btn)
        self.table.itemSelectionChanged.connect(self.hide_btn)

        self.delete_selected_btn.setEnabled(False)

        """
            Настройка дочерних элементов
        """
        self.save.browse_location_btn.clicked.connect(self.browse_save_item_location)
        self.save.save_csv_btn.clicked.connect(self.save_csv_items)

    def hide_btn(self):
        column_count = len(self.item_headers)
        row_count = len(self.item_table_list)
        visibility = not len(self.table.selectedItems()) == 0 \
                     and (column_count != 1 or row_count != 1)

        self.delete_selected_btn.setEnabled(visibility)

    def delete_selected(self):
        selected_items = self.table.selectedItems()

        if self.header_type == "row":
            self.table.removeRow(self.header_id)
            self.items_database.remove(self.items_database[self.header_id])
            self.item_table_list.remove(self.item_table_list[self.header_id])
        elif self.header_type == "column":
            header_to_delete = self.item_headers[self.header_id]
            row_count = len(self.item_table_list)

            self.table.removeColumn(self.header_id)
            for row in range(row_count):
                self.item_table_list[row].remove(self.item_table_list[row][self.header_id])
                self.items_database[row].pop(header_to_delete)
            self.item_headers.remove(header_to_delete)
        else:
            for ind in range(len(selected_items)):
                selected_item = selected_items[ind]
                row, column = selected_item.row(), selected_item.column()

                selected_item.setText("")
                self.item_table_list[row][column] = self.table.item(row, column)
                self.items_database[row][self.item_headers[column]] = ""

        self.header_id = None
        self.header_type = ""
        self.delete_selected_btn.setEnabled(False)

    def column_range_clicked(self, index):
        column_count = len(self.item_headers)
        if column_count != 1:
            self.header_id = index
            self.header_type = "column"
            self.delete_selected_btn.setEnabled(True)

    def row_range_clicked(self, index):
        row_count = len(self.item_table_list)
        if row_count != 1:
            self.header_id = index
            self.header_type = "row"
            self.delete_selected_btn.setEnabled(True)

    #   Логика сохранение
    def browse_save_item_location(self):
        location = QFileDialog.getOpenFileName(self, "Выбрать путь", "")[0]
        location_text = location[:location.rfind("/") + 1]

        self.save.location_edit.setText(location_text)

    #   csv
    def save_csv_items(self):
        location = self.save.location_edit.text()
        file_name = self.save.file_name_edit.text()

        if check_file_name(file_name):
            if "/" in location:
                with open(f"{location}{file_name}.csv", "w", newline="") as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=self.item_headers)

                    writer.writeheader()
                    for item in self.items_database:
                        writer.writerow(item)
            else:
                pass
        else:
            pass

    def csv_loader(self, full_file_location):
        file = open(full_file_location, "r").read()
        parsed_file = [line.split(",") for line in file.split("\n")][:-1]
        self.item_headers = parsed_file[0]
        self.items_database = []
        self.item_table_list = []

        self.table.setRowCount(len(parsed_file) - 1)
        self.table.setColumnCount(len(self.item_headers))

        row, column = 0, 0
        for line in parsed_file[1:]:
            if len(line) <= len(self.item_headers):
                self.items_database.append({})
                self.item_table_list.append([])
                for title in line:
                    self.items_database[row][self.item_headers[column]] = title

                    self.table.setItem(row, column, QTableWidgetItem(""))
                    self.table.item(row, column).setText(title)
                    self.item_table_list[row].append(self.table.item(row, column))

                    column += 1
                column = 0
                row += 1

        self.table.setHorizontalHeaderLabels(self.item_headers)

    #   Изменение клетки
    def item_edited(self):
        selected_items = self.table.selectedItems()

        if len(selected_items) != 0:
            selected_item = selected_items[0]
            row, column = selected_item.row(), selected_item.column()

            self.table.item(row, column).setText(selected_item.text())
            self.item_table_list[row][column] = self.table.item(row, column)

            header = self.item_headers[column]
            for key in self.items_database[row].keys():
                if key == header:
                    self.items_database[row][key] = self.item_table_list[row][column].text()

    #   Изменение названия заголовка
    def change_horizontal_header(self, index):
        old_header = self.item_headers[index]
        new_header, is_compilable = QInputDialog.getText(self, f"Заголовок {index}", "Новое название:",
                                                         QLineEdit.Normal, old_header)

        if is_compilable and check_title(new_header):
            row_count = len(self.item_table_list)
            for row in range(row_count):
                new_category = {}
                for header in self.item_headers:
                    info = self.items_database[row].get(header, "")
                    if header != old_header:
                        new_category[header] = info
                    else:
                        new_category[new_header] = info
                self.items_database[row] = new_category

            self.item_headers[index] = new_header
            self.table.setHorizontalHeaderLabels(self.item_headers)

    #   Добавление строки
    def add_row(self):
        column_count = len(self.item_headers)
        row_count = len(self.item_table_list)

        self.table.setRowCount(row_count + 1)

        temp = []
        for col in range(column_count):
            self.table.setItem(row_count, col, QTableWidgetItem(""))
            temp.append(self.table.item(row_count, col))
        self.item_table_list.append(temp)

        categories = {}
        for header in self.item_headers:
            categories[header] = ""
        self.items_database.append(categories)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = DatabaseEditor()
    ex.show()

    sys.exit(app.exec_())
