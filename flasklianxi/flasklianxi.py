from flask import Flask, render_template, request
import config
import random, string, json, redis
import eventlet
import eventlet.wsgi
import socketio

app = Flask(__name__)
app.config['SECRET_KEY'] = config.key
rds = redis.Redis(host='localhost', port=6379, db=0, password=None)
socket_app = socketio.Server()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['GET', 'POST'])
def download():
    url = request.form.get('url', '')
    print(url)
    key = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(16)])

    nums = rds.publish('download_job', json.dumps({'url': url, 'key': key}))

    return render_template('download.html')


@socket_app.on('my event')
def event(sid, environ):
    print('received sid:{} emviron:{} '.format(sid, environ))
    if 'key' not in environ:
        socket_app.emit(environ['key'], {'message': '错误'})
        return
    socket_app.emit(environ['key'], {'message': '等待'})


@app.route('/callback', methods=['GET', 'POST'])
def callback():
    data = request._get_body_string().decode()
    print(data)
    data = json.loads(data)
    key = data.get('key', '')
    file_name = data.get('filename', '')
    print(key, file_name)
    url = 'http://oi9gn1ckm.bkt.clouddn.com/{}'.format(file_name)
    print(url)
    socket_app.emit(key, {'url': url})


if __name__ == '__main__':
    # app.run(port=63730)

    new_app = socketio.Middleware(socket_app, app)
    eventlet.wsgi.server(eventlet.listen(('', 8000)), new_app)
