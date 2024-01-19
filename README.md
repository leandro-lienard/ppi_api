# Documentacion api ppi
https://itatppi.github.io/ppi-official-api-docs/api/documentacionPython/

## Para correr el script
### Imports
>pip install requests  
>pip install ppi_client
   
libreria de "bs4 import BeautifulSoup"

### Keys
Necesitamos keys para la api ppi  
Esto se consigue logueandote en  
>    ppi -> mis gestiones -> api    

Luego, deberán crear un archivo 'config.config' en el root del proyecto con este contenido

```
[Keys]
private_key:<private_key>
public_key:<public_key>
``` 
Completando con las credenciales otorgadas en el paso anterior

Por último, corremos el programa desde "ppi_api.py" :D 
>    /bin/python3 /home/leandrolienard/utn-repos/ppi_api/ppi_api.py

### How to Run
Set-ExecutionPolicy Bypass -Scope Process
.\env\Scripts\Activate

> flask --app flask_app.py run