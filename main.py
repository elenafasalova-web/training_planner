import tkinter as tk
from tkinter import ttk, messagebox
import json
import datetime
import os

class TrainingPlanner:
    def __init__(self, master):
        self.master = master
        master.title("Training Planner")

        self.data = []  # список для хранения тренировок

        # Создаем интерфейс
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Поля для ввода данных
        ttk.Label(self.master, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.date_entry = ttk.Entry(self.master)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.master, text="Тип тренировки:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.type_entry = ttk.Entry(self.master)
        self.type_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.master, text="Длительность (мин):").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.duration_entry = ttk.Entry(self.master)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка добавить
        self.add_button = ttk.Button(self.master, text="Добавить тренировку", command=self.add_training)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Фильтр по типу
        ttk.Label(self.master, text="Фильтр по типу:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.filter_type_entry = ttk.Entry(self.master)
        self.filter_type_entry.grid(row=4, column=1, padx=5, pady=5)

        # Фильтр по дате
        ttk.Label(self.master, text="Фильтр по дате:").grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.filter_date_entry = ttk.Entry(self.master)
        self.filter_date_entry.grid(row=5, column=1, padx=5, pady=5)

        # Buttons фильтров
        self.filter_type_button = ttk.Button(self.master, text="Фильтр по типу", command=self.filter_type)
        self.filter_type_button.grid(row=4, column=2, padx=5, pady=5)

        self.filter_date_button = ttk.Button(self.master, text="Фильтр по дате", command=self.filter_date)
        self.filter_date_button.grid(row=5, column=2, padx=5, pady=5)

        # Таблица для отображения данных
        self.tree = ttk.Treeview(self.master, columns=('Дата', 'Тип', 'Длительность'), show='headings')
        self.tree.heading('Дата', text='Дата')
        self.tree.heading('Тип', text='Тип тренировки')
        self.tree.heading('Длительность', text='Длительность')
        self.tree.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

        # Кнопка сброса фильтра
        self.reset_button = ttk.Button(self.master, text="Показать все", command=self.load_data)
        self.reset_button.grid(row=7, column=0, columnspan=3, pady=10)

    def add_training(self):
        date_str = self.date_entry.get()
        type_str = self.type_entry.get()
        duration_str = self.duration_entry.get()

        # Проверка корректности
        if not self.validate_date(date_str):
            messagebox.showerror("Ошибка", "Некорректный формат даты! Используйте ГГГГ-ММ-ДД.")
            return
        if not self.validate_positive_number(duration_str):
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом.")
            return

        # Добавление данных
        entry = {
            "date": date_str,
            "type": type_str,
            "duration": int(duration_str)
        }
        self.data.append(entry)
        self.save_data()
        self.load_data()

        # Очистка полей
        self.date_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

    def validate_date(self, date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def validate_positive_number(self, number_text):
        return number_text.isdigit() and int(number_text) > 0

    def load_data(self):
        # Загрузка из JSON
        if os.path.exists('data.json'):
            with open('data.json', 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = []

        self.refresh_table(self.data)

    def save_data(self):
        # Сохранение в JSON
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def refresh_table(self, data):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Заполнение таблицы
        for entry in data:
            self.tree.insert('', 'end', values=(entry['date'], entry['type'], entry['duration']))

    def filter_type(self):
        filter_value = self.filter_type_entry.get()
        filtered = [d for d in self.data if d['type'] == filter_value]
        self.refresh_table(filtered)

    def filter_date(self):
        filter_value = self.filter_date_entry.get()
        # Проверка формата даты
        if not self.validate_date(filter_value):
            messagebox.showerror("Ошибка", "Некорректный формат даты! Используйте ГГГГ-ММ-ДД.")
            return
        filtered = [d for d in self.data if d['date'] == filter_value]
        self.refresh_table(filtered)

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
