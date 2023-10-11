# Consigna_4DSS
## Setup
1) Descargar python3 para tu sistema operativo:

Windows -https://www.python.org/downloads/windows/

Ubuntu (Generalmente ya viene preinstalado):
- Abrir consola, y usar comandos: 
* sudo apt update #Actualizamos la lista de repositorios
* sudo apt install python3 #Instalamos Python
* python --version #Verificar que se instaló, y versión

2) Instalamos pip
* sudo apt install python3-pip
* pip3 --version #Verificar que se instaló, y versión

3) Instalamos librerias
* pip install os-sys
* pip install requests

## Utilización de los códigos:

### Prueba sql_injection_test.py
En la variable url se indica la url base para hacer la consulta, de cambiar de puerto el servidor, o poseer otro dominio esta deberá ser modificada con los nuevos valores.
Primero se hace un get a la url para obtener el JSESSIONID que es necesario para poder crear correctamente la request con la inyección al servidor, luego se indican los headers del request, en este caso recreamos los mismos headers que en una request común que se genera desde la página al hacer el login, la diferencia radica en el payload, que en este caso se ve en la variable data, allí se encuentra la información de usuario, y contraseña, para esta inyección se hizo que el usuario pasara a ser ' OR 1=1 -- para intentar iniciar sesión con el primer usuario de la base de datos, ya que con la comilla simple detenemos el valor usuario evaluado en la consulta SQL, y agregamos un OR 1=1 el cual siempre se va a cumplir, para evitar el AND y el resto de la consulta que pueda obstruir la inyección o no ser de nuestro interés se agrega el doble guion --. En el post que se genera con el método .post se le añade a la url /doLogin/ para hacer el pedido a la localización que deseamos, se añaden los headers, y además el data que contiene el payload. Al final del método se añade también un parámetro allow_redirects=false, esto es porque de ser una prueba exitosa se nos da el token de AltoroAccount en el response de redirección, de no indicar el allow_redirects en false nos devolverá el segundo response que se obtiene posterior al redirect, el cual no posee la información necesaria para reconocer si se dejó paso a la inyección o no. Por último, revisamos si el response nos devolvió un AltoroAccounts token, que indica la autenticación del primer usuario o no. En caso de que lo devuelva significa que se dejó pasar la inyección y por lo tanto se da un exit code 1, de no devolverse el token significa que no paso la inyección, es decir esta mitigada, y por ende la prueba falla dando un exit code 0.

### Prueba xss_test.py:
En esta prueba hay que tener en cuenta las mismas indicaciones para la variable url que en la primera.
