import requests
from bs4 import BeautifulSoup

url = 'https://www.prexcard.com.ar/transferencias-uruguay'

def get_compra_value():    
    # Realizar la solicitud GET para obtener el contenido de la página
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        span_with_value = soup.find_all('h2', {'class':'valor-cotizacion'})
        
        # Verificar si se encontró la etiqueta
        if span_with_value:
            venta = span_with_value[0].text.strip()  # este no importa
            compra = span_with_value[1].text.strip()  # Este es el que nos interesa
            print("\nPREX venta: %s compra: %s " % (venta, compra))
            return compra


def get_pesos_totales(monto_usd_uy):
    compra = get_compra_value()
    float_compra = float(compra.replace(",", ""))
    return float_compra * float(monto_usd_uy) * float(0.99)

