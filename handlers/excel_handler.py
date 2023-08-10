import openpyxl


def get_task_4_words_from_excel(path=r'handlers\materials_for_studying\task_4\task_4.xlsx'):
    users_accents_word = []
    wb = openpyxl.load_workbook(path)
    ws = wb.active
    for row in ws.iter_rows(min_row=2, max_col=2, values_only=True):
        users_accents_word.append({'correct word': row[0], 'incorrect word': row[1]})
    return users_accents_word


def get_task_1_problem_from_excel(path=r'materials_for_studying\task_1\task_1.xlsx'):
    users_problems = []
    wb = openpyxl.load_workbook(path)
    ws = wb.active
    for row in ws.iter_rows(min_row=2, values_only=True):
        users_problems.append({'description': row[1], 'text_of_task': row[2],
                               'correct_answers': row[3]})
    return users_problems


print(get_task_1_problem_from_excel())
