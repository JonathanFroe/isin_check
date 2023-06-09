from bs4 import BeautifulSoup
import requests

dezimaltrennzeichen = "."

def get_data(ISIN):
    search_url = "https://www.onvista.de/suche?searchValue=%s" %ISIN
    response = requests.get(search_url, headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
    soup = BeautifulSoup(response.content, 'html.parser')
    if response.url != search_url:
        return get_name(soup), get_wkn(soup), response.url, get_volatilität(soup), get_performence(soup)
    return None

def get_name(soup):
    table = soup.find(lambda tag:tag.name=="h1")
    if table is not None:
        return table.text
    return None

def get_wkn(soup):
    table = soup.find(lambda tag:tag.name=="span" and "WKN" in tag.text)
    if table is not None:
        table = table.find_next_siblings("span")
        return table[0].text[:6]
    return None

def get_volatilität(soup):
    table = soup.find(lambda tag:tag.name=="td" and "Volatilität" in tag.text)
    if table is not None:
        table = table.parent
        list = table.find_all('td')
        werte = []
        for arg in list:
            werte.append(arg.text.replace(',',dezimaltrennzeichen))
        werte = werte[1:]
        for i in range(len(werte)):
            if werte[i] != "–":
                werte[i] = float(werte[i].replace(' %',''))
            else:
                werte[i] = None
        return werte

def get_performence(soup):
    table = soup.find(lambda tag:tag.name=="td" and "Performance" in tag.text)
    if table is not None:
        table = table.parent
        list = table.find_all('td')
        werte = []
        for arg in list:
            werte.append(arg.text.replace(',',dezimaltrennzeichen))
        werte = werte[1:]
        for i in range(len(werte)):
            if werte[i] != "–":
                werte[i] = float(werte[i].replace(' %',''))
            else:
                werte[i] = None
        return werte
    return None

#For testing
if __name__ == "__main__":
    print(get_data("LI0148578169"))