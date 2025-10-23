# Propósito: Instrucciones para la instalación y ejecución de la aplicación.

# Aplicación de Simulación de Seguridad IoT

Esta es una aplicación Streamlit diseñada para demostrar conceptos de seguridad de IoT en un entorno **totalmente local y simulado**. No realiza ninguna llamada de red real ni descarga binarios externos en tiempo de ejecución.

## Requisitos

* Python 3.8+
* `pip`

## Instalación

1.  Crea un entorno virtual (recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

2.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Ejecución

1.  Navega al directorio raíz del proyecto (donde se encuentra `app.py`).
2.  Ejecuta Streamlit:
    ```bash
    streamlit run app.py
    ```
3.  Abre la URL proporcionada por Streamlit (generalmente `http://localhost:8501`) en tu navegador.

## Ejecución de Pruebas (Opcional)

Para verificar que los simuladores centrales funcionan correctamente, puedes ejecutar las pruebas unitarias:

```bash
python -m unittest discover tests
