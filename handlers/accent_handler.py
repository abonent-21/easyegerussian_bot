import json

users_accent_words = {1: {'correct_word': '', 'incorrect_word': '', 'current_num': 0}}
with open("users_data/current_user_accents.json", encoding='UTF-8') as f:
    users_accent_words = json.load(f)

with open("materials_for_studing/accents.json", encoding='UTF-8') as f:
    accents = json.load(f)


def check_id_in_list(user_id):
    return user_id in users_accent_words


def create_new_words_for_new_user(user_id):
    correct_word = accents[0]['correct word']
    incorrect_word = accents[0]['incorrect word']
    users_accent_words[user_id] = {'correct_word': correct_word, 'incorrect_word': incorrect_word, 'current_num': 0}


def get_words_user(user_id):
    return [users_accent_words[user_id]['correct_word'], users_accent_words[user_id]['incorrect_word']]


def give_new_words_for_user(user_id, current_num):
    correct_word = accents[(current_num + 1) % len(accents)]['correct word']
    incorrect_word = accents[(current_num + 1) % len(accents)]['incorrect word']
    users_accent_words[user_id] = {'correct_word': correct_word, 'incorrect_word': incorrect_word,
                                   'current_num': (current_num + 1) % len(accents)}


def check_correct_word(user_id, message):
    return message == users_accent_words[user_id]['correct_word']
