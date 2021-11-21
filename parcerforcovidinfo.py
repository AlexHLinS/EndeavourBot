from bs4 import BeautifulSoup
import requests

COVID_INFO_URL = 'https://www.worldometers.info/coronavirus/'


def getDataForCountry(country):
    result = ''
    req = requests.get(COVID_INFO_URL).text

    parsed = BeautifulSoup(req, features='lxml')

    table = parsed.find('tbody').find_all('tr')

    dataF = list()
    for row in table:
        cells = row.find_all('td')
        buffer = list()
        for i in range(len(cells)):
            buffer.append(cells[i].text)
        dataF.append(buffer)

    for line in dataF:
        if line[1].lower().find(country.lower()) != -1:
            result += f'Данные по {line[1]}:\n - всего случаев: {line[2]} (новых {line[3]});\n - смертность {line[4]} (новых {line[5]});\n - выздоровивших {line[6]}.'

    return result


print(getDataForCountry('world'))
