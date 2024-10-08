import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel, QListWidget, QMessageBox, QHBoxLayout
)
from matplotlib import pyplot as plt

class FinanceManagerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kişisel Finans Yönetimi Uygulaması")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Gelir ve gider girişi
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Tutarı girin...")
        self.layout.addWidget(self.amount_input)

        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Açıklama girin...")
        self.layout.addWidget(self.description_input)

        # Gelir ve gider seçim kutusu
        self.type_input = QListWidget()
        self.type_input.addItems(["Gelir", "Gider"])
        self.layout.addWidget(self.type_input)

        # Veri ekleme butonu
        self.add_button = QPushButton("Veri Ekle")
        self.add_button.clicked.connect(self.add_data)
        self.layout.addWidget(self.add_button)

        # Rapor gösterme butonu
        self.report_button = QPushButton("Rapor Göster")
        self.report_button.clicked.connect(self.show_report)
        self.layout.addWidget(self.report_button)

        # Verileri yükle
        self.load_data()

    def add_data(self):
        amount = self.amount_input.text()
        description = self.description_input.text()
        data_type = self.type_input.currentItem().text() if self.type_input.currentItem() else None

        if amount and description and data_type:
            try:
                amount = float(amount)
                data = self.load_existing_data()
                data.append({"amount": amount, "description": description, "type": data_type})
                with open("finance_data.json", "w") as file:
                    json.dump(data, file)
                self.amount_input.clear()
                self.description_input.clear()
                self.load_data()
            except ValueError:
                QMessageBox.warning(self, "Hata", "Lütfen geçerli bir tutar girin.")
        else:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun.")

    def load_data(self):
        self.data_list = QListWidget()
        self.layout.addWidget(self.data_list)
        self.data_list.clear()
        
        data = self.load_existing_data()
        for entry in data:
            self.data_list.addItem(f"{entry['type']}: {entry['description']} - {entry['amount']} TL")

    def load_existing_data(self):
        try:
            with open("finance_data.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def show_report(self):
        data = self.load_existing_data()
        income = sum(item['amount'] for item in data if item['type'] == "Gelir")
        expenses = sum(item['amount'] for item in data if item['type'] == "Gider")

        # Grafik gösterimi
        labels = 'Gelir', 'Gider'
        sizes = [income, expenses]
        explode = (0.1, 0)  # Geliri biraz patlat

        plt.figure(figsize=(7, 7))
        plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.axis('equal')  # Eşit oran
        plt.title("Finans Raporu")
        plt.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinanceManagerApp()
    window.show()
    sys.exit(app.exec_())

