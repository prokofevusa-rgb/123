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
        password=os.environ.get('PASS_POSGRE_TIMEWEB'),
        sslmode='disable'
    )

@app.route('/')
def home():
    return """
    <h1>🏢 МойСклад</h1>
    <ul>
        <li><a href="/regions">📍 Склады</a></li>
        <li><a href="/moves">📦 Перемещения</a></li>
        <li><a href="/stats">📊 Статистика</a></li>
        <li><a href="/test">🔍 Проверка БД</a></li>
    </ul>
    """

@app.route('/regions')
def regions():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM regions_moysklad')
    regions = cur.fetchall()
    cur.close()
    conn.close()
    
    html = "<h1>📍 Склады</h1><ul>"
    for r in regions:
        html += f"<li>{r[1]}</li>"
    html += "</ul><a href='/'>← Назад</a>"
    return html

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
