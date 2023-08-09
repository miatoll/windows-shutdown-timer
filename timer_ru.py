import tkinter as tk
from tkinter import messagebox
import threading
import time
import os

class ShutdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Таймер Выключения Компьютера")

        self.label = tk.Label(root, text="Привет! \\(＾▽＾)/\nДавай поиграем в 'Таймер Выключения Компьютера'! :3")
        self.label.pack()

        self.minutes_entry = tk.Entry(root)
        self.minutes_entry.pack()

        self.shutdown_button = tk.Button(root, text="Выключить OwO", command=self.start_shutdown)
        self.shutdown_button.pack()

        self.cancel_button = tk.Button(root, text="Отмена", command=self.cancel_shutdown, state=tk.DISABLED)
        self.cancel_button.pack()

        self.status_label = tk.Label(root, text="")
        self.status_label.pack()

        self.shutdown_thread = None
        self.running = False  # Добавляем атрибут для отслеживания состояния отсчета

    def update_status_label(self, minutes, seconds):
        self.status_label.config(text=f"Инициируется отсчет... {minutes:02d}:{seconds:02d}")
        self.root.update()

    def start_shutdown(self):
        minutes = self.minutes_entry.get()
        try:
            minutes = int(minutes)
            if minutes <= 0:
                messagebox.showerror("Ошибка", "Пожалуйста, введите корректное количество минут.")
                return

            confirmation_message = f"Вы уверены, что хотите выключить компьютер через {minutes} минут?"
            result = messagebox.askyesno("Подтверждение", confirmation_message)

            if result:
                self.running = True
                self.shutdown_thread = threading.Thread(target=self.shutdown, args=(minutes,))
                self.shutdown_thread.start()
                self.shutdown_button.config(state=tk.DISABLED)
                self.cancel_button.config(state=tk.NORMAL)
            else:
                self.status_label.config(text="Отмена операции :3")

        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректное количество минут.")

    def shutdown(self, minutes):
        total_seconds = minutes * 60
        for remaining_seconds in range(total_seconds, 0, -1):
            if not self.running:
                break
            self.update_status_label(remaining_seconds // 60, remaining_seconds % 60)
            time.sleep(1)

        if self.running:
            os.system("shutdown /s /f /t 0")
            self.status_label.config(text="Компьютер выключен :3")
        else:
            self.status_label.config(text="Операция отменена :3")
        self.cancel_button.config(state=tk.DISABLED)
        self.shutdown_button.config(state=tk.NORMAL)
        self.running = False

    def cancel_shutdown(self):
        if self.shutdown_thread and self.running:
            self.running = False

if __name__ == "__main__":
    root = tk.Tk()
    app = ShutdownApp(root)
    root.mainloop()
