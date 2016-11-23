import os
from flask import Flask, request, Response, jsonify, render_template
import sqlite3

app = Flask(__name__)

@app.route('/raw', methods=['GET'])
def raw():
    conn = sqlite3.connect('skyscrapers.db')

    cursor = conn.cursor()
    cursor.execute('''SELECT * from buildings ORDER BY height DESC LIMIT 10''')
    data = []
    for url in cursor.fetchall():
      data.append({'city': url[0], 'name': url[1], 'height':url[2]})

    return render_template('raw.html', buildings=data)


@app.route('/', methods=['GET'])
def test():
    return Response('Wassup')


if __name__ == "__main__":
    app.run(debug=True)
