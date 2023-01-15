from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import os
import cipher

# Путь к файлу с интейрфейсом
UI_PATH = os.path.join(os.path.dirname(__file__), "main.ui")

# Алфавит для шифрования
ALPHABET = "abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыъэюя"


class MainForm(QMainWindow):
    def __init__(self):
        super().__init__()
        # Загружаем интерфейс из файла
        uic.loadUi(UI_PATH, self)

        # Объект для доступа к буферу обмена
        self._clipboard = QApplication.clipboard()
        # Объект шифровальщик
        self._cipher = cipher.AffineCaesar(ALPHABET)

        # Настройка интерфейса
        self._configure_ui()

    def _configure_ui(self):
        self.plainInsertBtn.clicked.connect(self._plain_insert)
        self.plainCopyBtn.clicked.connect(self._plain_copy)
        self.cipherInsertBtn.clicked.connect(self._cipher_insert)
        self.cipherCopyBtn.clicked.connect(self._cipher_copy)

        self.encryptBtn.clicked.connect(self._encrypt)
        self.decryptBtn.clicked.connect(self._decrypt)

    def _plain_insert(self):
        """Вставляет содержимое буфера обмена в поле открытого текста"""
        if (self._clipboard.mimeData().hasText()):
            self.plainText.setPlainText(self._clipboard.text())

    def _plain_copy(self):
        """Копирует поле открытого текста в буфер обмена"""
        self._clipboard.setText(self.plainText.toPlainText())

    def _cipher_insert(self):
        """Вставляет содержимое буфера обмена в поле шифротекста"""
        if (self._clipboard.mimeData().hasText()):
            self.cipherText.setPlainText(self._clipboard.text())

    def _cipher_copy(self):
        """Копирует поле шифротекста в буфер обмена"""
        self._clipboard.setText(self.cipherText.toPlainText())

    def _lower_plain(self):
        """Переводит открытый текст в нижний регистр"""
        self.plainText.setPlainText(self.plainText.toPlainText().lower())

    def _lower_cipher(self):
        """Переводит шифротекст в нижний регистр"""
        self.cipherText.setPlainText(self.cipherText.toPlainText().lower())

    def _encrypt(self):
        self._lower_plain()
        # Создаем ключ из введенных данных
        key = cipher.AffineCaesarKey(
            self.multiplier.value(), self.summand.value())
        try:
            # Пробуем шифровать
            encrypted = self._cipher.encrypt(self.plainText.toPlainText(), key)
            self.cipherText.setPlainText(encrypted)
        except cipher.BadKey as e:
            # Если ключ плохой, то выводим сообщение
            self._display_bad_key_message(e.get_key())

    def _decrypt(self):
        self._lower_cipher()
        # Создаем ключ из введенных данных
        key = cipher.AffineCaesarKey(
            self.multiplier.value(), self.summand.value())
        try:
            # Пробуем расшифровать
            decrypted = self._cipher.decrypt(
                self.cipherText.toPlainText(), key)
            self.plainText.setPlainText(decrypted)
        except cipher.BadKey as e:
            # Если ключ плохой, то выводим сообщение
            self._display_bad_key_message(e.get_key())

    def _display_bad_key_message(self, key: cipher.AffineCaesarKey):
        """Выдает сообщение о неверном ключе шифрования"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(
            f"Размер алфавита ({len(ALPHABET)}) и множитель ключа ({key.multiplier}) должны быть взаимно просты!")
        msg.setWindowTitle("Неверный ключ!")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
