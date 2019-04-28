# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами
import grabnails
import json
import logging
import random
# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])

def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)
    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.
        global ggl
        ggl = ['pinterest дизайн маникюр']
        sessionStorage[user_id] = {
            'suggests': [
                "нюд",
                "блёстки",
                "геометрия",
                "острые",
                "матовые",
                "овал",
                "длинные",
                "розовый",
                "стразы",
                "весна",
                "жёлтый",
                "буквы",
                "короткие",
                "на работу",
                "на свидание"
            ]
        }

        res['response']['text'] = 'Привет!'  + '\n' + 'Введи несколько параметров, которые помогут мне подобрать лучший маникюр для тебя. Например:'\
         + '\n' + '- цвет' + '\n' + '- длина' + '\n' + '- форма' + '\n' + 'Напиши «стоп» чтобы выйти из навыка.'
        res['response']['buttons'] = get_suggests(user_id)
        return

    # Обрабатываем ответ пользователя.
    if req['request']['original_utterance'].lower() == 'стоп':
        res['response']['text'] = 'Пока!'
        return
    if req['request']['original_utterance'].lower() == 'хочу маникюр!':
        global img
        img = grabnails.im_id(0, ' '.join(ggl))
        res['response']['card'] = {}
        res['response']['card']['type'] = 'BigImage'
        res['response']['card']['title'] = 'Этот город я знаю.'
        res['response']['card']['image_id'] = img
        return
    res['response']['buttons'] = get_suggests(user_id)
    ggl.append(req['request']['original_utterance'].lower())
    # Если нет, то убеждаем его купить слона!
    res['response']['text'] = '«' + ' '.join(ggl) + '» ' + 'уже в списке параметров.' + '\n' + 'Если это всё, то напиши «хочу маникюр!»'

# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    random.shuffle(session['suggests'])
    arr = ['хочу маникюр!', 'стоп', 'случайный маникюр дня'] + session['suggests']
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in arr[:6]
    ]


    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests
