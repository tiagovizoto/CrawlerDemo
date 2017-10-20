import os
import time

import requests
from bs4 import BeautifulSoup
from captcha.captcha_resolver import resolver
from robobrowser import RoboBrowser


def sign_up_decea_with_cpf():
    while True:
        browser = RoboBrowser(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36")
        browser.open("http://servicos.decea.gov.br/sarpas/?i=cadastro&passo=1&doc=cpf", verify=False, timeout=3)

        with open('old.html', 'w') as f:
            f.write(browser.parsed.prettify())
            f.close()

        with open('cookies_old.html', 'w') as f:
            f.write(str(browser.response.cookies))
            f.close()

        print(browser.session.cookies)
        time.sleep(5)
        form = browser.get_form(id='frmSignUp')

        form['nome'].value = 'Thiago Vizoto'

        form['email'].value = 'vizoto123@gmail.com'
        form['nac'].value = 'BRA'
        form['pais'].value = 'BRA'
        form['telefone_celular'].value = '(41) 99702-0434'
        form['cpf'].value = "06068195414"
        form['dt_nasc'].value = '09/04/1988'
        form['doc'].value = open(os.getcwd() + '/cpf.jpg', 'rb')
        form['senha'].value = "M1NH4s3nh4!"
        form['senha_igual'].value = "M1NH4s3nh4!"
        form['vef'] = resolver(patch=browser.find_all('img')[1]['src'])
        print(browser.session.headers)
        browser.submit_form(form)
        print(browser.session.cookies)

        with open('result.html', 'w') as f:
            f.write(browser.parsed.prettify())
            f.close()

        with open('cookies_result.html', 'w') as f:
            f.write(str(browser.response.cookies))
            f.close()

        if not browser.find(class_="fa fa-exclamation-circle"):
            break


def testes():
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
    r = requests.Session()
    r.headers.update({'User-Agent': user_agent})

    html_text = r.get("http://servicos.decea.gov.br/sarpas/?i=cadastro&passo=1&doc=cpf")
    soup = BeautifulSoup(html_text.content, "html.parser")
    with open('htmls/antes_do_cadastro.html', 'w') as f:
        f.write(soup.prettify())
        f.close()

    payload = {
        'nome': 'Luciano Carvalho Ribeiro',
        'email': 'lucianoribeiro56@yahoo.com.br',
        'nac': 'BRA',
        'pais': 'BRA',
        'telefone_celular': '(41) 99999-0994',
        'cpf': '78068863893',
        'dt_nasc': '19/09/1956',
        'senha': 'M1NH4s3nh4!',
        'senha_igual': 'M1NH4s3nh4!',
        'vef': resolver(soup.find_all('img')[1]['src']),
        'doc': ('cpf.jpg', os.getcwd() + '/cpf.jpg'),
    }
    # files = {'doc': os.getcwd() + '/crawler/flights/cpf.jpg', 'filesname':'cpf.jpg'}

    r.headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                      'Connection': 'keep-alive',
                      'Upgrade-Insecure-Requests': '1',
                      'Referer': 'http://servicos.decea.gov.br/sarpas/?i=cadastro&passo=1&doc=cpf'})

    print(r.headers)
    html_text = r.post("http://servicos.decea.gov.br/sarpas/view/cadastro/act.cfm?passo=1", data=payload)

    with open('htmls/cadastro.html', 'w') as f:
        f.write(html_text.text)
        f.close()

    with open('htmls/headers.html', 'w') as f:
        f.write(str(html_text.headers))
        f.close()

sign_up_decea_with_cpf()
