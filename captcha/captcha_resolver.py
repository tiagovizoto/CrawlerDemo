from PIL import Image
import pytesseract
import requests
import os


def resolver(patch):
    with open('captcha.png', "wb") as f:
        f.write(requests.get('http://servicos.decea.gov.br/' + patch).content)

    string_captcha = pytesseract.image_to_string(Image.open('captcha.png'))
    print(string_captcha)
    os.remove('captcha.png')

    return string_captcha
