import requests
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

url = 'http://www.prexcard.com.ar/transferencias-uruguay'
headers = {'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'}
proxy = {"http":'https://45.70.60.66:60061'}


session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def get_compra_value():    
    # Realizar la solicitud GET para obtener el contenido de la página

    response = session.get(url)
    
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        h2_cotizacion = soup.find_all('h2', {'class':'valor-cotizacion'})
        
        # Verificar si se encontró la etiqueta
        if h2_cotizacion:
            venta = h2_cotizacion[0].text.strip()  # este no importa
            compra = h2_cotizacion[1].text.strip()  # Este es el que nos interesa
            print("\nPREX venta: %s compra: %s " % (venta, compra))
            return compra
    else:
        print("Error trying to get prex transferencias venta y compra value")


def get_pesos_totales(monto_usd_uy):
    compra = get_compra_value()
    print(compra)
    float_compra = float(compra.replace(",", ""))
    return float_compra * float(monto_usd_uy) - float_compra

def main():
    get_pesos_totales(1000)

if __name__ == "__main__":
    main()