import json
import handlers.excel_handler

with open("handlers/users_data/current_user_accents.json", encoding='UTF-8') as f:
    users_current_accent_words = json.load(f)


def get_accents_from_excel():
    return handlers.excel_handler.get_accent_word_from_excel()


def check_id_in_list(user_id):
    return user_id in users_current_accent_words


def create_new_words_for_new_user(user_id):
    correct_word = get_accents_from_excel()[0]['correct word']
    incorrect_word = get_accents_from_excel()[0]['incorrect word']
    users_current_accent_words[user_id] = {'correct_word': correct_word, 'incorrect_word': incorrect_word,
                                           'current_num': 0}


def get_words_user(user_id):
    return [users_current_accent_words[user_id]['correct_word'], users_current_accent_words[user_id]['incorrect_word']]


def give_new_words_for_user(user_id, current_num):
    correct_word = get_accents_from_excel()[(current_num + 1) % len(get_accents_from_excel())]['correct word']
    incorrect_word = get_accents_from_excel()[(current_num + 1) % len(get_accents_from_excel())]['incorrect word']
    users_current_accent_words[user_id] = {'correct_word': correct_word, 'incorrect_word': incorrect_word,
                                           'current_num': (current_num + 1) % len(get_accents_from_excel()star)}


def check_correct_word(user_id, message):
    return message == users_current_accent_words[user_id]['correct_word']
