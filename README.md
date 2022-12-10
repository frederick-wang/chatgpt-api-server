# chatgpt-api-server

![](https://img.shields.io/github/license/frederick-wang/chatgpt-api-server)

## 简介

这是一个兴趣使然的项目，今天为了给我的 QQ 群机器人调用 `ChatGPT` 服务写的，所以只能满足最基本的需求，一问一答。

如果你需要更多的功能，可以在此基础上自行改进。

原理是使用无头浏览器（选用了 `playwright`）模拟用户操作，在 `ChatGPT` 网页上输入问题，获取回答。

**注意：需要全局代理，否则无法访问 `ChatGPT` 网页。**

## 运行环境

我的运行环境是 `Python 3.9.12`，其他版本未测试。

## 安装依赖

```bash
python -m pip install -r requirements.txt
```

安装完成依赖后，需要再安装一下 `playwright` 需要用到的 `chromium`。

```bash
python -m playwright install chromium
```

## 配置文件

首先将 `config.example.yaml` 复制一份并重命名为 `config.yaml`，然后修改其中的配置。

```yaml
server:
  host: 0.0.0.0
  port: 23946
chat:
  timeout: 90
context:
  user_agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36
cookie:
  __Secure-next-auth.session-token: Input your cookie "__Secure-next-auth.session-token" here
```

将 `__Secure-next-auth.session-token` 的值改为你的 `ChatGPT` 的 `__Secure-next-auth.session-token` 的值，方法见下图。首先打开 `ChatGPT` 的网站，然后在 `Chrome` 中按 `F12` 打开开发者工具，然后点击 `Application`，再点击 `Cookies`，找到 `__Secure-next-auth.session-token`，复制其值。

![](https://res.zhaoji.ac.cn/images/20221210215535.png)

## 启动服务

在终端中执行：

```bash
python server.py
```

如果启动成功，你应该可以看到下图所示的输出。

![](https://res.zhaoji.ac.cn/images/20221210215923.png)

## 在线 Demo

在服务启动成功后，你可以访问 `http://127.0.0.1:23946/` 查看在线 Demo。

![](https://res.zhaoji.ac.cn/images/20221210221829.png)

在上方的输入框中输入问题，点击 `Send` 按钮，稍等几秒，即可获取回答。

## 接口调用

只要给 `/api/chat` 这个接口发 `POST` 请求就可以了。

在 `JavaScript` 中使用 `fetch` 调用接口的示例：

```js
fetch('http://127.0.0.1:23946/api/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        msg: 'Hello',
    }),
}).then(res => res.json()).then(console.log)
```

在终端中使用 `curl` 调用接口的示例：

```bash
curl -X POST -H "Content-Type: application/json" -d '{"msg": "Hello"}' http://127.0.0.1:23946/api/chat
```

在 `Python` 中使用 `requests` 调用接口的示例：

```python
import requests

requests.post('http://127.0.0.1:23946/api/chat', json={'msg': 'Hello'}).json()
```

接口的返回值是一个 `JSON` 对象，包含了 `error`、`message` 和 `data` 三个字段，其中 `data` 是一个 `object`，包含 `cost_time` 和 `response` 两个字段，分别表示请求耗时和 `ChatGPT` 的回复。

```json
{
  "data": {
    "cost_time": 6.0790696144104,
    "response": "Hello! I'm Assistant, a large language model trained by OpenAI. I'm here to help with any questions you may have. Is there anything in particular you would like to know?"
  },
  "error": 0,
  "message": "Success"
}
```
