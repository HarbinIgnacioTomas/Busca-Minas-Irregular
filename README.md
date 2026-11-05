# Busca Minas Irregular

Aplicación de escritorio que modifica la estructura de un clásico juego de Buscaminas integrando celdas el doble de grandes.
Incorpora grillas irregulares cambiando la dinámica del juego. Donde antes cada celda contaba con 8 vecinas, ahora hay celdas que pueden tener hasta 12, manteniendo la misma lógica de números basados en minas circundantes.
Desarrollado en Python, con un patrón MVC y fuerte orientación a objetos.

---

## Características Principales

* Arquitectura Limpia (MVC): Desacoplamiento total entre la lógica del juego y la interfaz gráfica, garantizando un código mantenible, escalable y fácil de testear, con una fuerte distribución de responsabilidades entre clases.
* Soporte para Grillas Irregulares y Bloques 2x2: Lógica avanzada de cálculo de vecinas adaptada para manejar coordenadas complejas y valores numéricos extendidos.
* Versatilidad y personalización: Permite la modificación de los parámetros clásicos del juego (filas y columnas del tablero, cantidad de minas), así como la cantidad de celdas irregulares, soportando tanto tableros tradicionales como nuevos tableros con variable cantidad de bloques 2x2. (Nota: Actualmente configurable a nivel de código, con vistas a implementar próximamente en un menú de configuración en la interfaz).

---

## Tecnologías y Herramientas Utilizadas
* Lenguaje: Python 3.11
* Interfaz Gráfica: PyQt5
* Patrón de Diseño: MVC (Modelo_Vista_Controlador) y principios de programación orientada a objetos (POO)
* Control de Versiones: Git y GitHub

---

