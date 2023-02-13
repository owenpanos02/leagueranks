from flask import Flask, render_template, request, redirect, url_for
from account import *
import requests




app = Flask(__name__)



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', val = account('HxHFAN99'), val2 = account('hibago'), val3 = account('RaggedyShoes'), val4 = account('luckbih3'),  val5 = account('KloudyMan'))


@app.route('/test')
def test():
    return render_template('test.html', test_val = account('HxHFAN99'), test_val2 = account('hibago'), test_val3 = account('RaggedyShoes'), test_val4 = account('luckbih3'),  test_val5 = account('KloudyMan'))


if __name__ == '__main__':
    app.run()

    


