import os
from flask import Flask, request, Response, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/raw', methods=['GET'])
def raw():
    conn = sqlite3.connect('skyscrapers.db')

    cursor = conn.cursor()
    cursor.execute('''SELECT * from buildings''')
    data = []
    for url in cursor.fetchall():
      data.append(url[0])

    return Response(response=data,
    mimetype="application/json"), 200


@app.route('/', methods=['GET'])
def test():
    return Response('Wassup')


if __name__ == "__main__":
    app.run(debug=True)
