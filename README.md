# Herramienta de Estimación de Adopción SaaS B2B Latam

Esta aplicación Streamlit proporciona una herramienta interactiva para estimar la tasa de adopción de nuevas funcionalidades en software SaaS B2B, con un enfoque en el mercado de Latinoamérica.

## Funcionalidades

*   **Calculadora Predictiva:** Ingresa las características de una nueva funcionalidad (tipo, complejidad, valor percibido, esfuerzo de marketing, etc.) y obtén una estimación del rango de adopción esperado a los 3 meses, con escenarios base, optimista y pesimista.
*   **Explorador de Benchmarks:** Consulta datos de benchmarks de la industria para métricas clave de adopción y retención en software contable en Latam.
*   **Generador de Informes (Placeholder):** Funcionalidad futura para generar informes resumidos.

## Despliegue en Streamlit Community Cloud

Para desplegar esta aplicación en Streamlit Community Cloud:

1.  Asegúrate de tener una cuenta en [GitHub](https://github.com/) y en [Streamlit Community Cloud](https://streamlit.io/cloud).
2.  Crea un nuevo repositorio en GitHub (puede ser público o privado).
3.  Sube los siguientes archivos a la raíz de tu repositorio de GitHub:
    *   `app.py` (este es el código principal de la aplicación)
    *   `requirements.txt` (lista las dependencias de Python necesarias)
    *   `README.md` (este archivo)
4.  Ve a tu [dashboard de Streamlit Community Cloud](https://share.streamlit.io/).
5.  Haz clic en "New app" o "Crear aplicación".
6.  Conecta tu cuenta de GitHub y selecciona el repositorio que acabas de crear.
7.  Asegúrate de que la rama principal (generalmente `main` o `master`) esté seleccionada.
8.  Verifica que el archivo principal (Main file path) esté configurado como `app.py`.
9.  Haz clic en "Deploy!".

Streamlit Community Cloud instalará las dependencias de `requirements.txt` y desplegará tu aplicación. Una vez completado, tendrás un enlace público para acceder a ella.

