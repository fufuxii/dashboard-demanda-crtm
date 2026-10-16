# 📊 Dashboard de Demanda del CRTM

Proyecto de desarrollo de un dashboard interactivo para analizar y visualizar la demanda del transporte público del **Consorcio Regional de Transportes de Madrid (CRTM)**.

## 🛠️ Tecnologías utilizadas

- **Python**: procesamiento y tratamiento de datos.
- **Streamlit**: desarrollo de la interfaz del dashboard.
- **Pandas**: gestión y análisis de datos.
- **Plotly**: creación de gráficos interactivos.
- **DB2 en z/OS**: integración y consulta de datos.
- **z/OSMF REST API**: comunicación con el entorno z/OS.

## 📁 Estructura del proyecto

```text
dashboard-demanda-crtm/
├── datos/                  # Datos y archivos de origen
├── scr/
│   ├── api/                # Comunicación con APIs
│   ├── dashboard/          # Interfaz del dashboard
│   ├── database/           # Acceso a la base de datos
│   └── logic/              # Lógica y visualizaciones
├── .env                    # Variables de entorno privadas
├── .gitignore
├── requirements.txt        # Dependencias del proyecto
└── README.md
```

## ⚙️ Instalación y ejecución

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/fufuxii/dashboard-demanda-crtm.git
   cd dashboard-demanda-crtm
   ```

2. Crear y activar un entorno virtual:

   ```bash
   python -m venv .venv
   ```

   En Windows:

   ```powershell
   .venv\Scripts\activate
   ```

3. Instalar las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Configurar las variables de entorno necesarias en el archivo `.env`.

5. Ejecutar el dashboard:

   ```bash
   streamlit run main.py
   ```

## 🔐 Configuración y seguridad

Las credenciales y los datos de conexión deben almacenarse en variables de entorno.

Los archivos `.env` y `.venv/` no deben subirse al repositorio de GitHub.

## 🚀 Estado del proyecto

Proyecto en desarrollo. Se está trabajando en el procesamiento de los datos, la integración con DB2 en z/OS y la creación de visualizaciones interactivas para analizar la demanda del transporte público.

---

Desarrollado como proyecto del Talent Campus de PSS.