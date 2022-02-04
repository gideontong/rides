from re import sub

def parse_yes_no(text: str) -> bool:
    text = sub('[^A-Za-z]+', '1', text)
