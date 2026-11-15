# Sistema de Gestión y Cierre de Caja (Python & SQLite)

Aplicación de consola (CLI) desarrollada en Python para la administración de clientes, registro de movimientos diarios y cierre de caja de una agencia de quiniela.

## Evolución del Proyecto
Este repositorio documenta la progresión técnica del sistema desde un prototipo académico hasta una solución con persistencia relacional:
1. **v1 - Prototipo Base:** CRUD inicial en consola con persistencia básica en archivos `.txt`.
2. **v2 - Refactorización y UX:** Limpieza de código, validaciones estrictas de entrada y navegación interactiva mediante `questionary`.
3. **v3 - Lógica de Negocio:** Incorporación de categorías de movimiento (Efectivo, Transferencia, Fiado, Telekino, Egresos) y cálculo de cierre de caja.
4. **v4 - Migración a SQL (Versión Actual):** Reemplazo de archivos planos por base de datos relacional **SQLite3**, separando la capa de acceso a datos de la interfaz de usuario.

## Aspectos Técnicos Destacados
* **Arquitectura Desacoplada:** Separación clara entre las consultas SQL y la lógica de interacción por consola.
* **Seguridad:** Uso de consultas parametrizadas (`?`) para prevenir inyección SQL.
* **Optimización en Base de Datos:** Delegación de cálculos y filtros al motor SQL mediante `SUM()`, `COALESCE()` y búsquedas insensibles a mayúsculas (`LOWER` + `LIKE`).

## Tecnologías Utilizadas
* Python 3
* SQLite3
* Questionary
* Colorama

## Cómo ejecutarlo
1. Clonar el repositorio: `git clone https://github.com/MaximilianoBeron555/sistema-gestion-quiniela-sql.git`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Ejecutar el programa: `python "v4 - Migración a SQL (Versión Actual).py"`
