# PELO FUNDAMENTUS MOBILE
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# executar tabela e navegador
tabela = pd.read_excel(
    r'C:\Users\Usuario\Documents\Programação\analise de ativos\banco de dados pesquisa.xlsx')
nav = webdriver.Chrome(
    r'C:\Users\Usuario\Downloads\chromedriver\chromedriver.exe')
nav.get('http://www.fundamentus.com.br/?interface=classic&interface=mobile')

# digitar ativo
for ativo in tabela['ATIVO']:
    nav.find_element_by_xpath(
        '//*[@id="completar"]').send_keys(ativo, Keys.ENTER)

    # coletar preço
    preco = float(nav.find_element_by_xpath(
        '/html/body/div[2]/div[3]/div[2]/div[1]/div/div[1]/span[2]').text.replace('R$', '').replace('.', '').strip().replace(',', '.'))

    # coletar P/L
    pl = float(nav.find_element_by_xpath(
        '/html/body/div[2]/div[3]/div[4]/div/div/div/div[1]/div/span[2]').text.replace('.', '').strip().replace(',', '.'))

    # coletar dividendos
    dy = float(nav.find_element_by_xpath(
        '/html/body/div[2]/div[3]/div[4]/div/div/div/div[7]/div/span[2]').text.replace('%', ' ').strip().replace('.', '').strip().replace(',', '.'))/100

    # coletar roe
    roe = float(nav.find_element_by_xpath(
        '/html/body/div[2]/div[3]/div[5]/div/div/div/div[1]/div/span[2]').text.replace('%', ' ').strip().replace(',', '.'))/100

    # coletar roic
    roic = nav.find_element_by_xpath(
        '/html/body/div[2]/div[3]/div[5]/div/div/div/div[2]/div/span[2]').text.replace(',', '.').replace('%', ' ').strip()
    if roic == '-':
        roic = float('10')
    else:
        roic = float(roic)/100

    tabela.loc[tabela['ATIVO'] == ativo, 'PREÇO'] = preco
    tabela.loc[tabela['ATIVO'] == ativo, 'PL'] = pl
    tabela.loc[tabela['ATIVO'] == ativo, 'DY'] = dy
    tabela.loc[tabela['ATIVO'] == ativo, 'ROE'] = roe
    tabela.loc[tabela['ATIVO'] == ativo, 'ROIC'] = roic

    #tabela.to_excel(r'C:\Users\Usuario\Documents\Programação\analise de ativos\Ativos\tabela ativos_pd.xlsx', index=False)
# pegar media // outro site
nav.get('https://br.advfn.com')
for ativo in tabela['ATIVO']:
    nav.find_element_by_id(
        'headerQuickQuoteSearch').send_keys(ativo, Keys.ENTER)
    # coletar media
    media = float(nav.find_element_by_xpath(
        '//*[@id="id_period_quote"]/tbody/tr[4]/td[5]').text.replace('.', '').strip().replace(',', '.'))
    tabela.loc[tabela['ATIVO'] == ativo, 'MEDIA'] = media
    tabela['%MEDIA'] = ((tabela['MEDIA'] - tabela['PREÇO']) / tabela['PREÇO'])

    tabela.to_excel(
        r'C:\Users\Usuario\Documents\Programação\analise de ativos\Ativos\tabela ativos_pd.xlsx', index=False)
nav.quit()
print(tabela)
