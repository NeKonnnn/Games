import tkinter as tk
from tkinter import messagebox
from game import WordGame
from PIL import Image, ImageTk

class WordGameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Игра 'Слова'")
        
        # Загрузка и масштабирование изображения
        self.original_image = Image.open("words_game.png")
        self.bg_image = ImageTk.PhotoImage(self.original_image)

        # Фоновое изображение
        self.background_label = tk.Label(self.master, image=self.bg_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label.bind("<Configure>", self.resize_image)

        # Инициализация игры
        self.game = WordGame()
        
        # Создание виджетов начального меню
        self.start_button = tk.Button(self.master, text="Начать", command=self.start_game, bg="green")
        self.rules_button = tk.Button(self.master, text="Правила игры", command=self.show_rules, bg="yellow")
        self.info_button = tk.Button(self.master, text="Информация о разработчике", command=self.show_developer_info, bg="blue")
        self.place_buttons_center()
        
        # Виджеты для игры
        self.word_entry = tk.Entry(self.master, width=40, font=("Arial", 14))
        self.word_entry.bind("<Return>", self.submit_word_by_enter)
        self.enter_button = tk.Button(self.master, text="Ввод", command=self.submit_word, bg="green")
        self.give_up_button = tk.Button(self.master, text="Сдаться", command=self.give_up, bg="red")
        self.restart_button = tk.Button(self.master, text="Начать заново", command=self.restart_game, bg="blue")
        self.quit_button = tk.Button(self.master, text="Закончить", command=self.master.quit, bg="red")
        self.rules_button_game = tk.Button(self.master, text="Правила игры", command=self.show_rules_from_game, bg="yellow")

        # Виджеты для экрана информации о разработчике и правил
        self.developer_label = tk.Label(self.master, text="Разработал игру Иванов Иван Иванович 22.08.2023 года.", bg="lightblue", fg="black")
        self.rules_label = tk.Label(self.master, text="Правила игры 'Слова':\n\n"
                            "1. Цель игры: Игрок и компьютер поочередно называют слова. Каждое следующее слово должно начинаться с последней буквы предыдущего слова. Цель игрока – заставить компьютер ошибиться или не придумать слово на нужную букву.\n\n"
                            "2. Тематики: В игре существуют следующие тематики: животные, города, имена. Компьютер случайным образом выбирает одну из этих тематик перед началом игры.\n\n"
                            "3. Начало игры: Игрок начинает первым и вводит слово из выбранной тематики.\n\n"
                            "4. Ограничения по словам: Слова не должны повторяться. Слова должны соответствовать выбранной тематике. Слова должны быть существительными.\n\n"
                            "5. Буквы 'ь' и 'ы': Если слово заканчивается на 'ь' или 'ы', следующее слово должно начинаться с предпоследней буквы этого слова.\n\n"
                            "6. Регистр букв: Игрок может вводить слова как с заглавной, так и со строчной буквы. Однако регистр не влияет на правильность ответа. Например, слова 'Москва' и 'москва' считаются одинаковыми.\n\n"
                            "7. Завершение игры: Если игрок или компьютер не могут придумать слово на нужную букву, противник выигрывает. Игрок может сдаться в любой момент, нажав кнопку 'Сдаться'. Игра может быть перезапущена в любой момент, нажав кнопку 'Начать заново'.",
                            bg="lightblue", fg="black", justify=tk.LEFT)
        self.back_button = tk.Button(self.master, text="Назад", command=self.show_main_menu, bg="blue")
        self.back_to_game_button = tk.Button(self.master, text="Вернуться в игру", command=self.return_to_game, bg="blue")
    
    def place_buttons_center(self):
        self.start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, y=-60)
        self.rules_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, y=0)
        self.info_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, y=60)

    def resize_image(self, event):
        new_width = event.width
        new_height = event.height
        self.bg_image = ImageTk.PhotoImage(self.original_image.resize((new_width, new_height)))
        self.background_label.config(image=self.bg_image)

    def show_main_menu(self):
        self.developer_label.pack_forget()
        self.rules_label.pack_forget()
        self.back_button.pack_forget()
        self.place_buttons_center()

    def show_rules(self):
        self.start_button.place_forget()
        self.rules_button.place_forget()
        self.info_button.place_forget()
        self.rules_label.pack(pady=40)
        self.back_button.pack(pady=20)

    def show_developer_info(self):
        self.start_button.place_forget()
        self.rules_button.place_forget()
        self.info_button.place_forget()
        self.developer_label.pack(pady=40)
        self.back_button.pack(pady=20)

    def start_game(self):
        self.start_button.place_forget()
        self.rules_button.place_forget()
        self.info_button.place_forget()
        self.word_entry.place(relx=0.5, rely=0.5, anchor=tk.CENTER, y=-60)
        self.enter_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, y=0)
        self.give_up_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, y=60)
        self.restart_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, y=120)
        self.quit_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, y=180)
        self.rules_button_game.place(relx=0.5, rely=0.5, anchor=tk.CENTER, y=240)
        # Информируем игрока о выбранной тематике
        messagebox.showinfo("Тематика игры", f"Тематика этой игры: {self.game.chosen_category}.")

    def submit_word(self):
        player_word = self.word_entry.get().strip().lower()
        error, computer_word = self.game.play(player_word)
        if error:
            messagebox.showerror("Ошибка", error)
            return
        messagebox.showinfo("Ответ компьютера", f"Компьютер выбрал слово: {computer_word}")
        self.word_entry.delete(0, tk.END)

    def submit_word_by_enter(self, event=None):
        self.submit_word()

    def give_up(self):
        self.game.reset()
        messagebox.showinfo("Игра окончена", "Вы сдались!")
        self.word_entry.delete(0, tk.END)
        self.show_main_menu()

    def restart_game(self):
        self.game.reset()
        self.word_entry.delete(0, tk.END)
        messagebox.showinfo("Игра началась заново", "Выберите новую тематику и начните игру!")

    def show_rules_from_game(self):
        self.word_entry.place_forget()
        self.enter_button.place_forget()
        self.give_up_button.place_forget()
        self.restart_button.place_forget()
        self.quit_button.place_forget()
        self.rules_button_game.place_forget()
        self.rules_label.pack(pady=40)
        self.back_to_game_button.pack(pady=20)

    def return_to_game(self):
        self.rules_label.pack_forget()
        self.back_to_game_button.pack_forget()
        self.start_game()

# Запуск GUI
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = WordGameGUI(root)
    root.mainloop()