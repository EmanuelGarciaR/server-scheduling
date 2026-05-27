# Server Scheduling Optimizer

[![Live Demo](https://img.shields.io/badge/Live_Demo-Disponible-success?style=for-the-badge&logo=netlify)](https://dazzling-elf-93cbf5.netlify.app/)
[![Next.js](https://img.shields.io/badge/Next.js-React-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Python-Backend-blue?style=for-the-badge&logo=python)](#)

Una plataforma web interactiva diseñada para visualizar, simular y comparar el rendimiento de diferentes algoritmos de asignación de servidores (Server Scheduling). Analiza las diferencias, tiempos de ejecución y *makespan* entre enfoques voraces (Greedy) y de búsqueda exhaustiva (Backtracking).




---

## Características Principales

- **Visualización de Algoritmos**: Observa paso a paso cómo se distribuyen las tareas entre los servidores con simulaciones interactivas.
- **Múltiples Estrategias**: Comparativa directa entre diferentes algoritmos de optimización.
- **Dashboard de Benchmarking**: Analiza métricas clave (tiempo de ejecución vs tamaño del problema) mediante gráficos intuitivos.
- **Interfaz Moderna y Responsiva**: Diseño atractivo y fluido construido con Next.js y Tailwind CSS.

## Demo en Vivo

Explora la aplicación funcionando en vivo aquí:  
[https://dazzling-elf-93cbf5.netlify.app/](https://dazzling-elf-93cbf5.netlify.app/)

<img src="docs/qr_server.png" alt="QR Code Server Scheduling App" width="150">

## Tecnologías

- **Frontend:** React, Next.js, Tailwind CSS
- **Backend:** Python, FastAPI

## Ejecución Local

Si deseas correr el proyecto en tu entorno local:

### 1. Frontend
```bash
cd frontend
npm install
npm run dev
```

### 2. Backend
```bash
cd backend
python -m venv .venv

# Activar entorno virtual:
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate

pip install -r requirements.txt
# Comando para iniciar el backend (ej. uvicorn, fastapi dev, etc.)
```

---
*Proyecto desarrollado para el análisis y optimización de algoritmos de planificación.*