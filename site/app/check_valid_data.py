import hashlib
import hmac


def verify_telegram_init_data(init_data: str, bot_token: str) -> bool:
    data = dict(item.split("=") for item in init_data.split("&") if "=" in item)

    hashed = data.pop("hash", None)

    if not hashed:
        return False

    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))

    secret_key = hmac.new(
        key=bytes(f"WebAppData{bot_token}", "utf-8"),
        msg=b"",
        digestmod=hashlib.sha256
    ).digest()

    expected_hash = hmac.new(secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256).hexdigest()

    return hmac.compare_digest(hashed, expected_hash)