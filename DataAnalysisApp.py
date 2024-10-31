import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog


class DataAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Analysis Application")
        self.root.geometry("800x600")

        self.data = None
        self.original_data = None  # Переменная для хранения оригинальных данных

        # Создание элементов интерфейса
        self.create_widgets()

    def create_widgets(self):
        # Кнопка для загрузки файла
        self.load_button = tk.Button(self.root, text="Загрузить файл", command=self.load_file)
        self.load_button.pack(pady=10)

        # Рамка для таблицы и скроллбаров
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Горизонтальный скроллбар
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal")
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Таблица для отображения данных с горизонтальным скроллбаром
        self.tree = ttk.Treeview(table_frame, xscrollcommand=h_scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree.bind("<Button-1>", self.on_column_click)  # Добавляем обработчик для клика по заголовку
        h_scrollbar.config(command=self.tree.xview)

        # Панель с кнопками для анализа данных
        self.analysis_frame = tk.Frame(self.root)
        self.analysis_frame.pack(pady=10)

        tk.Button(self.analysis_frame, text="Среднее", command=self.calculate_mean).grid(row=0, column=0, padx=5)
        tk.Button(self.analysis_frame, text="Минимум", command=self.calculate_min).grid(row=0, column=1, padx=5)
        tk.Button(self.analysis_frame, text="Максимум", command=self.calculate_max).grid(row=0, column=2, padx=5)

        # Поле ввода для фильтрации и кнопка сброса фильтра
        self.filter_value = tk.StringVar()
        tk.Entry(self.analysis_frame, textvariable=self.filter_value, width=20).grid(row=1, column=0, padx=5)
        tk.Button(self.analysis_frame, text="Фильтровать", command=self.filter_data).grid(row=1, column=1, padx=5)
        tk.Button(self.analysis_frame, text="Сбросить фильтр", command=self.reset_filter).grid(row=1, column=2, padx=5)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                # Загрузка данных с указанием разделителя ";"
                self.data = pd.read_csv(file_path, sep=';')
                self.original_data = self.data.copy()  # Сохраняем оригинальные данные
                self.show_data()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

    def show_data(self):
        # Очистка таблицы перед отображением новых данных
        self.tree.delete(*self.tree.get_children())
        self.tree["column"] = list(self.data.columns)
        self.tree["show"] = "headings"

        # Задание заголовков
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        # Заполнение данными
        for _, row in self.data.iterrows():
            self.tree.insert("", "end", values=list(row))

    def on_column_click(self, event):
        """Определяем, по какому столбцу был произведен клик."""
        region = self.tree.identify("region", event.x, event.y)
        if region == "heading":
            col_id = self.tree.identify_column(event.x)
            col_idx = int(col_id.replace("#", "")) - 1
            self.selected_column = self.tree["columns"][col_idx]
            messagebox.showinfo("Выбранный столбец", f"Выбран столбец: {self.selected_column}")

    def calculate_mean(self):
        column = getattr(self, "selected_column", None)
        if column:
            # Преобразование значений в числовой формат, игнорируя ошибки
            numeric_column = pd.to_numeric(self.data[column], errors='coerce')
            if pd.api.types.is_numeric_dtype(numeric_column):
                mean_value = numeric_column.mean()
                messagebox.showinfo("Среднее значение", f"Среднее значение для столбца {column}: {mean_value}")
            else:
                messagebox.showerror("Ошибка", f"Столбец {column} не является числовым.")
        else:
            messagebox.showerror("Ошибка", "Выберите столбец для анализа.")

    def calculate_min(self):
        column = getattr(self, "selected_column", None)
        if column:
            numeric_column = pd.to_numeric(self.data[column], errors='coerce')
            if pd.api.types.is_numeric_dtype(numeric_column):
                min_value = numeric_column.min()
                messagebox.showinfo("Минимальное значение", f"Минимальное значение для столбца {column}: {min_value}")
            else:
                messagebox.showerror("Ошибка", f"Столбец {column} не является числовым.")
        else:
            messagebox.showerror("Ошибка", "Выберите столбец для анализа.")

    def calculate_max(self):
        column = getattr(self, "selected_column", None)
        if column:
            numeric_column = pd.to_numeric(self.data[column], errors='coerce')
            if pd.api.types.is_numeric_dtype(numeric_column):
                max_value = numeric_column.max()
                messagebox.showinfo("Максимальное значение", f"Максимальное значение для столбца {column}: {max_value}")
            else:
                messagebox.showerror("Ошибка", f"Столбец {column} не является числовым.")
        else:
            messagebox.showerror("Ошибка", "Выберите столбец для анализа.")

    def filter_data(self):
        if self.data is None:
            messagebox.showerror("Ошибка", "Сначала загрузите данные.")
            return

        filter_text = self.filter_value.get()
        if not filter_text:
            messagebox.showwarning("Предупреждение", "Введите значение для фильтрации.")
            return

        filtered_data = self.data[self.data.apply(lambda row: row.astype(str).str.contains(filter_text).any(), axis=1)]
        if not filtered_data.empty:
            self.data = filtered_data
            self.show_data()
        else:
            messagebox.showinfo("Результат фильтрации", "Нет строк, удовлетворяющих фильтру.")

    def reset_filter(self):
        """Сброс фильтрации и восстановление оригинальных данных."""
        if self.original_data is not None:
            self.data = self.original_data.copy()
            self.show_data()
            self.filter_value.set("")  # Очищаем поле фильтра

if __name__ == "__main__":
    root = tk.Tk()
    app = DataAnalysisApp(root)
    root.mainloop()
