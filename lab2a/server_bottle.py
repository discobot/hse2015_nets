from bottle import route, run, request
from datetime import datetime
from collections import OrderedDict

msgs = OrderedDict({
    0: (datetime.now(), 'God', 'Initial message'),
})

msg_template = '<tr><td>{time}</td><td>\t<b>{user}: </b></td><td>{msg}</td></tr>'

@route('/')
def get_messages():
    result = '<h3>MegaChat</h3><table>'
    for ID, (time, user, msg) in msgs.items():
        result += msg_template.format(time=time, user=user, msg=msg)
    return result

@route('/', method='POST')
def post_message():
    ID =  request.forms.get('id')
    user = request.forms.get('user')
    msg = request.forms.get('msg')
    msgs[ID] = (datetime.now(), user, msg)

run(host='localhost', port=8080)
