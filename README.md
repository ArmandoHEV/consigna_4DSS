# Consigna_4DSS
## Setup
1) Descargar python3 para tu sistema operativo:

Windows -https://www.python.org/downloads/windows/

Ubuntu (Generalmente ya viene preinstalado):
- Abrir consola, y usar comandos:
```
sudo apt update #Actualizamos la lista de repositorios
```
```
sudo apt install python3 #Instalamos Python
```
```
python --version #Verificar que se instaló, y versión
```

2) Instalamos pip
```
sudo apt install python3-pip
```
```
pip3 --version #Verificar que se instaló, y versión
```

3) Instalamos librerias
```
pip install os-sys
```
```
pip install requests
```

## Utilización de los códigos:
Para utilizar los scripts y hacer las pruebas se ve necesario hacer los pasos indicados en el setup. Posteriormente se deben descargar los archivos, y abrir una consola en la cual se debe cambiar de repositorio, usando el comando cd <ruta_script>, hasta aquel donde se encuentra el script, y por ultimo ingresar python3 <nombre_script> para ejecutar el código.

### Prueba sql_injection_test.py
Primer se importan las librerias requests, y sys. Sus funcionalidades son crear los requests al servidor, e indicar un valor de exit code.
```
import requests 
import sys
```
En la variable url se indica la url base para hacer la consulta, de cambiar de puerto el servidor, o poseer otro dominio, esta deberá ser modificada con los nuevos valores.
```
url = "http://localhost:8080/AltoroJ"
```
Primero se hace un get a la url para obtener el JSESSIONID que es necesario para poder recrear correctamente la request con la inyección al servidor.
```
s = requests.Session()

jSessionId = s.get(url, verify=0).cookies.get("JSESSIONID")
```
Luego se indican los headers del request, en este caso recreamos los mismos headers que en una request común que se genera desde la página al hacer el login.
```
headers = {
    "Host": "localhost:8080",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux aarch64; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "http://localhost:8080/AltoroJ/login.jsp",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://localhost:8080",
    "Connection": "keep-alive",
    "Cookie": "JSESSIONID="+str(jSessionId),
    "Upgrade-Insecure-Requests": "1",
}
```
Posteriormente se crea el payload, que en este caso se ve en la variable data, allí se encuentra la información de usuario, y contraseña, para esta inyección se hizo que el usuario pasara a ser ' OR 1=1 -- para intentar iniciar sesión con el primer usuario de la base de datos, ya que con la comilla simple detenemos el valor usuario evaluado en la consulta SQL, y agregamos un OR 1=1 el cual siempre se va a cumplir, para evitar el AND y el resto de la consulta que pueda obstruir la inyección o no ser de nuestro interés se agrega el doble guion --. 
```
data = "uid=%27+OR+1%3D1+--&passw=1234&btnSubmit=Login"
```
En el post que se genera con el método .post() se le añade a la url /doLogin/ para hacer el pedido a la localización que deseamos, se añaden los headers, y además el data que contiene el payload. Al final del método se añade también un parámetro allow_redirects=false, esto es porque de ser una prueba exitosa se nos da el token de AltoroAccount en el response de redirección, de no indicar el allow_redirects en false nos devolverá el segundo response que se obtiene posterior al redirect, el cual actualmente no posee la información necesaria para reconocer si se dejó paso a la inyección o no. 
```
response = s.post(url+"/doLogin", headers=headers, data=data, allow_redirects=False)
```
Por último, revisamos si el response nos devolvió un AltoroAccounts token, que indica la autenticación del primer usuario o no. En caso de que lo devuelva significa que se dejó pasar la inyección y por lo tanto se da un exit code 1, de no devolverse el token significa que no paso la inyección, es decir esta mitigada, y por ende la prueba falla dando un exit code 0.
```
if response.status_code == 302 and response.cookies.get("AltoroAccounts"):
    sys.exit(1)
else:
    sys.exit(0)
```
### Prueba xss_test.py:
En esta prueba hacemos los mismos imports, y hay que tener en cuenta las mismas indicaciones para la variable url que en la primera.
```
import requests 
import sys

url = "http://localhost:8080/AltoroJ"
```
Nuevamente se recrea un request, en este caso estamos recreando el request generado al buscar algo en la searchbar.
```
s = requests.Session()

jSessionId = s.get(url, verify=0).cookies.get("JSESSIONID")
headers = {
    "Host": "localhost:8080",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux aarch64; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "http://localhost:8080/AltoroJ/login.jsp",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://localhost:8080",
    "Connection": "keep-alive",
    "Cookie": "JSESSIONID="+str(jSessionId),
    "Upgrade-Insecure-Requests": "1",
}
```
En este caso el ataque se encuentra en intentar agregar una etiqueta <script> con un alert() al html de la página web, mediante el añadido del ataque en la query.
```
injection = "<script>alert('Vulnerabilidad XSS')</script>"
```
El request en este caso es un método get, se le añade a la url /search.jsp?query=+injection para hacer el pedido a la localización deseada y para mandar en la query el ataque.
```
response = s.get(url+"/search.jsp?query="+injection, headers=headers, allow_redirects=False)
```
La response devuelve el html de la página, si en este se encuentra la etiqueta <script> con el alert(), es decir el ataque, significa que la vulnerabilidad no está mitigada, y la prueba da positivo con un exit code 1, y en caso de que el ataque no se encuentre en el html la prueba falla con un exit code 0, significando que esta mitigada la vulnerabilidad.
```
if injection in response.text:
    sys.exit(1)
else:
    sys.exit(0)
```
