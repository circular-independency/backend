def prepare_ai_category(response: dict) -> str:

    out = ""

    for category in response:
        out += f"{category['name']}\n"

    return out