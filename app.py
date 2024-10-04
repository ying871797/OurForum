import base64
import os
import uuid

import ahocorasick
import pandas as pd
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


# 获取聊天室列表
@app.route('/get_chatroom')
@cross_origin()
def get_chatroom():
    db = Mysql('data')
    res = db.get_chatroom()
    return res


# 获取访问量
@app.route('/get_aqr', methods=['GET'])
def get_aqr():
    db = Mysql('data')
    res = db.get_aqr()
    print(json.dumps(res))
    return json.dumps(res)


# 插入访问记录
@app.route('/record_aqr', methods=['POST'])
def insert_aqr():
    ip = request.json.get('ip')
    address = request.json.get('address')
    page_name = request.json.get('page_name')
    # 访问记录
    data = {
        'datetime': [str(time.strftime("%Y/%m/%d %H:%M:%S"))],
        'ip': [ip],
        'address': [address],
        'page_name': [page_name]
    }
    df = pd.DataFrame(data)
    df.to_csv(f'logs/{str(time.strftime("%Y%m%d"))}.csv', mode='a', index=False, header=False, encoding='utf-8')
    return 'ok'


@app.route('/insert_aqr', methods=['POST'])
def insert_aqc():
    db = Mysql('aqr')
    # 访问量
    res = db.insert_aqr()
    return res


# 插入消息
@app.route('/insert_data', methods=['POST'])
def insert_data():
    db = Mysql('data')
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


# 黑名单ip添加
@app.route('/add_black_ip', methods=['POST'])
def add_black_ip():
    db = Mysql('data')
    return db.insert_black_ip(request.json.get('ip'))


@app.route('/get_message', methods=['POST'])
def get_message():
    db = Mysql('data')
    # 根据type获取不同数量的数据
    res = db.get_message(request.json.get('chatroom'), request.json.get('get_count'), int(request.json.get('type')))
    # 添加评论数量
    return res


@app.route('/get_comments', methods=['POST'])
def get_comments():
    db = Mysql('comments')
    res = db.get_comment(request.json.get('msg_id'), request.json.get('chatroom'), request.json.get('get_count'),
                         request.json.get('type'))
    return res


@app.route('/insert_comment', methods=['POST'])
def insert_comment():
    db = Mysql('comments')
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
    return db.insert_comment(request.json.get('msg_id'), request.json.get('chatroom'), sender_cp, content_cp, path_str,
                             int(request.json.get('type')),
                             request.json.get('ip'),
                             request.json.get('address'))


# 修改消息
@app.route('/update_message', methods=['POST'])
def update_message():
    db = Mysql('data')
    return db.update_message(request.json.get('data'))


# 删除消息及图片
@app.route('/delete_message', methods=['POST'])
def delete_message():
    db = Mysql('data')
    # 图片删除
    data = request.json.get('data')
    imgSrc = data['imgSrc'].split(',')
    path = '../ourforump/src/assets/upload/'
    # 判断是否存在图片
    if imgSrc != ['']:
        for i in imgSrc:
            if os.path.exists(path + i):
                os.remove(path + i)
            else:
                print("删除文件失败")
    return db.delete_message(request.json.get('data'))


# 获取所有数据（指定表）
@app.route('/get_all', methods=['POST'])
def get_all():
    db = Mysql('data')
    res = db.get_all(str(request.json.get('table')))
    return res


# 获取指定密码
@app.route('/get_pass', methods=['POST'])
def getpass():
    db = Mysql('data')
    res = db.get_pass(request.json.get('passtype'))
    return res


# 获取公告
@app.route('/get_notice', methods=['POST'])
def get_notice():
    db = Mysql('data')
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
