from flask import Flask
import psycopg2
import os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host='62.113.41.125',
        port='5432',
        database='default_db',
        user='gen_user',
        password='PASS_POSGRE_TIMEWEB',
        sslmode='disable'
    )

@app.route('/')
def home():
    return "<h1>🎉 Flask работает!</h1><p><a href='/test'>Проверить БД</a></p>"

@app.route('/test')
def test():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT version()')
        version = cur.fetchone()[0]
        cur.close()
        conn.close()
        return f"✅ База подключена!<br><br>{version}"
    except Exception as e:
        return f"❌ Ошибка: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
