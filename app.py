import base64
import uuid
import os

import ahocorasick
from PIL import Image
from flask import Flask, request
from flask_cors import cross_origin
from flask_socketio import SocketIO, emit

from op import *


# 脏话屏蔽
def build_tree(wordlist):
    actree = ahocorasick.Automaton()
    for index, word in enumerate(wordlist):
        actree.add_word(word, (index, word))
    actree.make_automaton()
    return actree


def save_base64_image(base64_image, save_path):
    # 获取图片数据的头部和正文部分
    header, data = base64_image.split(",", 1)

    # 解码 Base64 数据
    image_data = base64.b64decode(data)

    # 创建新的图像，颜色模式为RGB，白色背景
    image = Image.new('RGB', (224, 224))

    # 保存图像到指定路径
    image.save(save_path, format="PNG")

    # 写入到本地文件
    with open(save_path, "wb") as image_file:
        image_file.write(image_data)


app = Flask(__name__)
socketio = SocketIO()
socketio.init_app(app, cors_allowed_origins='*')
name_space = '/'

# 脏话库读取
with open('./static/zh.json', 'r', encoding='utf-8') as f:
    zh_list = json.loads(f.read())


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/test')
def test():
    ip = request.remote_addr
    return ip


@app.route('/uploadImages', methods=['POST'])
def upload_images():
    pass


@app.route('/get_chatroom')
@cross_origin()
def get_chatroom():
    db = Mysql()
    res = db.get_chatroom()
    return res


@app.route('/insert_data', methods=['POST'])
def insert_data():
    db = Mysql()
    # 脏话屏蔽
    actree = build_tree(wordlist=zh_list)
    sender_cp = request.json.get('sender')
    content_cp = request.json.get('content')
    # 循环查询并替换
    for i in actree.iter(request.json.get('content')):
        content_cp = content_cp.replace(i[1][1], "**")
    for i in actree.iter(request.json.get('sender')):
        sender_cp = sender_cp.replace(i[1][1], "**")
    # 图片上传
    all_path = []
    save_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/ourforump/src/assets/upload/'
    for i in request.json.get('imgSrc'):
        # 生成唯一的文件名
        unique_filename = str(uuid.uuid4())[:8] + ".png"
        save_base64_image(i, save_path + unique_filename)
        # 保存文件名到列表
        all_path.append(unique_filename)
    # 图片路径字符串替换特殊字符
    path_str = ','.join(all_path).replace('\\', '\\\\')
    print(path_str)
    # 插入数据
    return db.insert_data(request.json.get('chatroom'), sender_cp, content_cp, path_str,
                          int(request.json.get('type')),
                          request.json.get('ip'),
                          request.json.get('address'))


@app.route('/get_all_data', methods=['POST'])
def getalldata():
    db = Mysql()
    print(request.json.get('get_count'))
    res = db.get_message(request.json.get('chatroom'), request.json.get('get_count'), int(request.json.get('type')))
    return res


@app.route('/get_pass', methods=['POST'])
def getpass():
    db = Mysql()
    res = db.get_pass(request.json.get('passtype'))
    return res


@app.route('/get_notice', methods=['POST'])
def getnotice():
    db = Mysql()
    res = db.get_notice(request.json.get('chatroom'))
    return res


@socketio.on('to_get_data', namespace=name_space)
def to_get_data_message(message):
    print(message)
    # 服务器广播给所有客户端
    emit('refresh', {'data': message['data'], 'order': 0})


@socketio.on('connect')
def test_connect():
    print('Client connected')


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
