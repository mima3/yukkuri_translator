# coding=utf-8
from bottle import get, post, template, request, Bottle, response, redirect
import os
from json import dumps
from collections import defaultdict
from yukkuri_translator import MarisaTranslator


app = Bottle()
user_dict = None


def setup(conf):
    global app
    global user_dict
    user_dict = conf.get('MeCab', 'user_dict')


@app.get('/')
def homePage():
    return template('home').replace('\n', '');

@app.get('/json/translate')
def translate():
    """
    翻訳する
    """
    src = request.query.src
    t = MarisaTranslator(user_dict)
    response.content_type = 'application/json;charset=utf-8'
    return dumps(t.translate(src.encode('utf-8')))
