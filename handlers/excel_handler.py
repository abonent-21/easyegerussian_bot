import openpyxl



def get_task_4_words_from_excel(name_file='task_4.xlsx'):
    users_accents_word = []
    wb = openpyxl.load_workbook(rf'handlers\materials_for_studying\task_4\{name_file}')
    ws = wb.active
    for row in ws.iter_rows(min_row=2, max_col=2, values_only=True):
        users_accents_word.append({'correct word': row[0], 'incorrect word': row[1]})
    return users_accents_word
