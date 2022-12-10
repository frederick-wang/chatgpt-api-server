import yaml
from playwright._impl._api_structures import SetCookieParam

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    context: 'dict[str, str]' = config['context']
    cookie: 'dict[str, str]' = config['cookie']
    chat: 'dict[str, str]' = config['chat']
    # convert to cookie object
    cookie_vars = [
        SetCookieParam(
            name=k,
            value=v,
            domain='chat.openai.com',
            path='/',
            # expires=1673246855446,
            httpOnly=True,
            secure=True,
            sameSite='Lax',
        ) for k, v in cookie.items()
    ]
