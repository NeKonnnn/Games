import random
from words import words_by_category

class WordGame:
    def __init__(self):
        self.used_words = []
        self.last_letter = None
        
        # Выбираем случайную категорию при инициализации игры
        self.chosen_category = random.choice(list(words_by_category.keys()))
        self.words = words_by_category[self.chosen_category]

    def _get_last_letter(self, word):
        """Получает последнюю букву слова, учитывая правила игры."""
        if word[-1] in ["ь", "ы"]:
            return word[-2]
        return word[-1]

    def validate_input(self, word):
        """Проверяет, соответствует ли введенное слово правилам игры."""
        if not word:
            return "Вы не ввели слово!"
        
        if word in self.used_words:
            return f"Слово '{word}' уже было использовано!"
        
        if self.last_letter and word[0] != self.last_letter:
            return f"Это неправильное слово, вы должны назвать слово, начинающееся на букву '{self.last_letter}'."
        
        if word not in self.words:
            return f"Слово '{word}' не соответствует тематике '{self.chosen_category}'."
        
        return None

    def get_computer_word(self, player_word):
        """Возвращает слово, выбранное компьютером."""
        self.last_letter = self._get_last_letter(player_word)
        possible_words = [word for word in self.words if word[0] == self.last_letter and word not in self.used_words]
        
        if not possible_words:
            return None
        
        computer_word = random.choice(possible_words)
        self.used_words.append(computer_word)
        self.last_letter = self._get_last_letter(computer_word)
        return computer_word

    def play(self, player_word):
        validation_error = self.validate_input(player_word)
        if validation_error:
            return validation_error, None
        
        self.used_words.append(player_word)
        
        computer_word = self.get_computer_word(player_word)
        if not computer_word:
            return "Я не могу придумать слово. Вы выиграли!", None
        
        return None, computer_word
