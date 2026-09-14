Depends (Inyección de Dependencias): Sirve para aislar la lógica repetitiva (como conectarse a la base de datos o verificar un token de seguridad). FastAPI se encarga de ejecutar esa función auxiliar antes de correr el código de tu endpoint.

yield vs return: yield permite ejecutar código después de que el endpoint haya terminado (en este caso, el db.close() en el bloque finally). Un return normal terminaría la función inmediatamente y no podrías cerrar la base de datos de forma segura.

El tipado (database: Session): No cambia cómo se ejecuta el código, pero es la forma en la que le dices a tu editor de texto: "Hey, esta variable database es una Sesión de SQLAlchemy, por favor muéstrame el autocompletado para .query(), .add(), .commit(), etc.". ¡Te salvará de muchos errores de tipeo!