import re

def extract_json(text):
    json_pattern = re.compile(r"\{.*\}", re.DOTALL)
    match = json_pattern.search(text)
    if match:
        return match.group(0)
    return None