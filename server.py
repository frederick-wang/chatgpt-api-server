import time
from typing import Any

from rich import print

from context import CONTEXT, START_URL
from config import config

from flask import Flask, jsonify, request

app = Flask(__name__)

HOST: str = config['server']['host']
PORT: int = int(config['server']['port'])
REPLY_TIMEOUT: float = float(config['chat']['timeout'])


def reply(msg: str) -> 'tuple[str, float]':
    page = CONTEXT.new_page()
    try:
        page.goto(START_URL)
        textarea = page.query_selector('textarea')
        btn = page.query_selector('textarea+button')
        if not textarea or not btn:
            raise ValueError('Could not find textarea or button')
        msg = msg.strip()
        print(f'[bold blue]Send message[/bold blue]: {msg}')
        for line in msg.splitlines():
            textarea.type(line)
            textarea.press('Shift+Enter')
        btn.click()
        start_time = time.time()
        while True:
            if time.time() - start_time > REPLY_TIMEOUT:
                raise RuntimeError('Reply timeout')
            reponse_text_list = page.query_selector_all(
                'div[class*="request-:"]')
            if btn.is_enabled() and reponse_text_list:
                cost_time = time.time() - start_time
                return reponse_text_list[-1].inner_text(), cost_time
            time.sleep(1)
    finally:
        page.close()


@app.route('/api/chat', methods=['POST'])
def chat():
    if request.method != 'POST':
        return jsonify({
            'error': 1,
            'message': 'Invalid request method',
            'data': None,
        }), 400
    # request data format: {"msg": "Hello"}
    if not request.is_json:
        return jsonify({
            'error': 1,
            'message': 'Invalid request data format, not json',
            'data': None,
        }), 400
    data: Any = request.get_json()
    if 'msg' not in data:
        return jsonify({
            'error': 1,
            'message': 'Invalid request data format, no msg field',
            'data': None,
        }), 400
    msg = data['msg']
    try:
        response, cost_time = reply(msg)
        return jsonify({
            'error': 0,
            'message': 'Success',
            'data': {
                'response': response,
                'cost_time': cost_time,
            }
        }), 200
    except Exception as e:
        return jsonify({
            'error': 1,
            'message': repr(e),
            'data': None,
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'error': 0,
        'message': 'Success',
        'data': {
            'status': 'ok',
        },
    }), 200


@app.route('/', methods=['GET'])
def index():
    return '''
    <html>
    <head>
        <title>ChatGPT API Server</title>
    </head>
    <body>
        <h1>ChatGPT API Server</h1>
        <p>ChatGPT Server is running.</p>
        <div>
            <!-- Invoke API Demo (using ajax) -->
            <h2>Invoke API Demo</h2>
            <p>Input message:</p>
            <textarea id="msg" style="width: 100%; height: 100px;"></textarea>
            <p>Response:</p>
            <textarea id="response" style="width: 100%; height: 100px;"></textarea>
            <p>
                <button id="btn">Send</button>
            </p>
            <script>
                document.getElementById('btn').onclick = function () {
                    var msg = document.getElementById('msg').value;
                    var xhr = new XMLHttpRequest();
                    xhr.open('POST', '/api/chat');
                    xhr.setRequestHeader('Content-Type', 'application/json');
                    xhr.onreadystatechange = function () {
                        if (xhr.readyState === 4) {
                            if (xhr.status === 200) {
                                var data = JSON.parse(xhr.responseText);
                                document.getElementById('response').value = data.data.response;
                            } else {
                                alert('Error: ' + xhr.status);
                            }
                        }
                    };
                    xhr.send(JSON.stringify({msg: msg}));
                };
            </script>
        </div>
    </body>
    </html>
    '''


if __name__ == '__main__':
    try:
        print('[green]Starting chatgpt api server ...[/green]')
        # Run flask server
        app.run(host=HOST, port=PORT, debug=False, threaded=False)
    finally:
        print('\n[green]Exiting ...[/green]')
