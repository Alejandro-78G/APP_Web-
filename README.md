# 📊 Jose Alejandro Cristancho | Data Analyst Portfolio

Este es mi portafolio profesional, diseñado para mostrar mis capacidades en **Ingeniería de Datos**, **Análisis de Marketing** y **Visualización Avanzada**. A diferencia de los portafolios estáticos convencionales, este sistema está construido sobre un backend robusto que permite una gestión dinámica de proyectos y una experiencia de usuario premium.

## 🛠️ Stack Tecnológico

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11+)
- **Frontend:** Jinja2 Templates & Vanilla CSS (Custom Design System)
- **Visualización:** Power BI Embedded
- **Gestión de Datos:** Estructura dinámica basada en JSON
- **Despliegue:** Preparado para Docker / Render / Railway

## ✨ Características Principales

- **Arquitectura Dinámica:** Los proyectos se cargan automáticamente desde un archivo `proyectos.json`, facilitando la actualización de contenido sin tocar el código base.
- **Visualización de Dashboards:** Integración directa con reportes interactivos de Power BI.
- **Narrativa Técnica:** Secciones detalladas de "Implementación y Hallazgos" con un diseño enfocado en la legibilidad del código y decisiones de arquitectura.
- **Diseño Premium:** Estética dark-mode inspirada en herramientas de ingeniería (GitSpec), con glassmorphism y micro-animaciones.

## 📁 Estructura del Proyecto

- `/templates`: Archivos HTML con motor de plantillas Jinja2.
- `/static`: Assets visuales, CSS personalizado y lógica JavaScript.
- `proyectos.json`: La "Base de Datos" del portafolio que orquestará todo el contenido.
- `app.py`: Servidor de alto rendimiento con FastAPI.

## 🚀 Instalación Local

1. Clona el repositorio:
   ```bash
   git clone https://github.com/Alejandro-78G/APP_Web-.git
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta el servidor:
   ```bash
   uvicorn app:app --reload
   ```

---
Diseñado y desarrollado por **Jose Alejandro Cristancho Gaona**
