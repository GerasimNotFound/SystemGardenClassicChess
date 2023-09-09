from flask import Flask, request


app = Flask(__name__)
@app.route('/alice', methods=['POST'])
def resp():
    agree_words = ['Да', 'Конечно', 'Давай']
    disagree_words = ['Нет','Не надо','Хватит']
    user = request.json.get('request', {}).get('command')
    dialogId = 0
    response_user = ('Добро пожаловать в навык "Шахматы". Вы можете ознакомиться с правилами игры сказав ' \
                    '"Правила" или же начать игру сказав "Поехали". Кроме того вы можете прослушать занимательную ' \
                    'теорию шахмат сказав "Теория". (Слова соглашения: Да Конечно Давай) (Слова несогласия: Нет Не надо Хватит)')
    if user == 'Теория':
        dialogId = 1
        response_user = ('*Заглушка* (будет выводить текст и спрашивать о продолжении) можно ответить Да (Конечно, Давай) или Нет (Не надо, Хватит)')
        while dialogId == 1:
            if user == agree_words[0][1][2]:
                response_user = ('*Заглушка* (будет выводить текст и спрашивать о продолжении) можно ответить Да или Нет')
            elif user == disagree_words[0][1][2]:
                dialogId = 2
            else:
                response_user = ('Не поняла вас. Скажите "Да" для продолжения или "Нет", если хотите остановиться.')
        response_user = 'Будем играть?'
        if user == agree_words[0][1][2]:
            pass


    response = {
        'response':{
            'user': response_user,
            'end_session': False
        },
        'version':'1.0'
    }
    return response

app.run('0.0.0.0', port=5000, debug=True)
