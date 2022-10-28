import hmac
from hashlib import sha256
from urllib.parse import unquote

# from local dir
from ownsecrets import BOT_TOKEN

secret_key = hmac.new(b'WebAppData', bytes(BOT_TOKEN, encoding='utf-8'), sha256).digest()


def is_valid_data(init_data_hash: str, data_check_string: str) -> bool:

    data_check_string_unquote = unquote(data_check_string)

    hash = hmac.new(secret_key, bytes(data_check_string_unquote, encoding='utf-8'), sha256).hexdigest()

    if hash == init_data_hash:
        return True
    else:
        return False