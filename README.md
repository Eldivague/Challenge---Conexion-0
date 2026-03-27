
# 🌐 **Chat Cliente-Servidor: Conexión con Sockets**

### 🚀 **¿Quién soy ahora?**
Pasé de programar juegos solitarios a construir un **sistema cliente-servidor**. Ahora entiendo cómo se conectan las máquinas usando **Sockets**, manejando direcciones **IP** y entendiendo que una app es, en el fondo, un flujo de datos que viaja de un punto a otro.

### 🛡️ **¿Cómo sobrevivió mi código?**
A base de **Hilos (Threading)** para que el servidor no se trabe con un solo usuario, y un uso estratégico de **Try/Except**. Con eso logré que, si un cliente se desconecta de golpe o algo falla, el servidor no explote y pueda seguir funcionando para los demás. Además, los hilos **Daemon** me salvaron de dejar procesos "fantasma" abiertos.

### 🛠️ **¿Qué aprendí cuando todo explotó?**
* **El "if not data":** Es la clave. Si no detectás el mensaje vacío, el servidor se queda procesando "aire" en un bucle infinito cuando alguien se va.
* **Decode/Encode:** El cable solo entiende bytes. Sin el `utf-8` para traducir los mensajes, no hay forma de que las personas se entiendan.
