# MLOps1 – CEIA – FIUBA  
**Ejemplo de ambiente productivo – Entrega Trabajo Final**

## Integrantes  
- Nicolás Werner (a1825)  
- Pablo Menardi (a1814)

---

## 1 Resumen del proyecto
La empresa ficticia **ML Models and Something More Inc.** ofrece modelos de ML mediante una API REST y utiliza un stack de servicios para sus flujos de DataOps ∕ MLOps:

| Servicio | Propósito |
|----------|-----------|
| **Apache Airflow** | Orquestación de pipelines (ETL + Entrenamiento + Deploy) |
| **MLflow** | Tracking de experimentos, artefactos y model registry |
| **FastAPI** | Exposición del modelo entrenado (endpoint `/predict`) |
| **MinIO (S3‑like)** | Data Lake y storage de artefactos ML |
| **PostgreSQL** | Backend DB para Airflow y MLflow |

El diagrama completo se encuentra en `final_assign.png`.

---

## 2 Validación 
| Requisito mínimo | Cumplimiento |
|------------------|--------------|
| **DAG en Airflow** | `airflow/dags/etl_wine_to_minio.py` (ETL ⇢ S3) **y** `airflow/dags/wine_sentiment_analysis_dag.py` (vectorizado + entrenamiento). |

| **Experimento en MLflow** | Ejecutado desde el Task `train_models` del DAG de entrenamiento → registra baseline, LogReg y SVM con métricas y artefactos. |

| **Modelo servido por REST API** | Contenedor `fastapi` listo; pendiente de registrar modelo en MLflow «Production» para que el microservicio deje de reiniciarse – planificado para la Fase 2. |

| **Documentación** | Docstrings en código + OpenAPI generado por FastAPI (`/docs`).  |

El ETL se validó subiendo **`raw/wine_profiles6.csv`** al bucket **`data`** (`mc ls myminio/data/raw/`).  
La tarea `upload_csv` aparece con estado **SUCCESS** en Airflow y los registros en MinIO confirman la carga.

---

## 3 Dataset
Se utiliza el dataset *Wine Profiles* (trabajo final de AM1) ubicado en `data/wine_profiles6.csv`.

---

## 4 Estructura del repositorio
```
├── airflow
│   ├── dags
│   │   ├── etl_wine_to_minio_dag.py
│   │   └── wine_sentiment_analysis_dag.py
│   ├── plugins/
│   ├── secrets/
│   ├── logs/            ← se crea en runtime
│   └── config/
├── data/                ← dataset .cron
├── dockerfiles/
│   ├── airflow/         ← Imagen extendida con boto3
│   ├── fastapi/
│   └── mlflow/
├── docker‑compose.yml
├── .env
└── docs/
    └── final_assign.png
```

---

## 5 Pasos de instalación
1. **Pre‑requisitos**: [Docker Desktop](https://docs.docker.com/get-docker/) instalado.  
2. Clonar el repo:
   ```bash
   git clone https://github.com/<usuario>/mlops1‑wine‑sentiment.git
   cd mlops1‑wine‑sentiment
   ```
3. Crear carpetas locales:  
   ```bash
   mkdir -p airflow/{dags,logs,plugins,config,secrets}
   ```
4. Ajustar UID en `.env` (solo Linux/Mac):
   ```env
   AIRFLOW_UID=$(id -u)
   ```
5. Levantar **todos** los servicios:
   ```bash
   docker compose --profile all up -d
   ```
6. Verificar en navegador:
   * Airflow ➜ <http://localhost:8080> (`airflow/airflow`)
   * MLflow ➜ <http://localhost:5001>
   * MinIO ➜ <http://localhost:9001> (`minio/minio123`)
   * API REST ➜ <http://localhost:8800/docs>

---

## 6 Ejecución de los pipelines
### 6.1 ETL → S3
```bash
# Lanzar desde CLI (también se puede desde la UI)
docker compose exec airflow-scheduler \
  airflow dags trigger etl_wine_to_minio
```
Resultado esperado: objeto `data/raw/wine_profiles6.csv` en MinIO.

### 6.2 Entrenamiento y tracking
Desde la UI de Airflow activar y disparar `wine_sentiment_analysis_dag`.  
Al finalizar, en MLflow se verán los tres runs con sus métricas y los modelos serializados.

---

## 7 Compartir el proyecto
1. **Repositorio Git** (GitHub / GitLab): subir todo el código, `docker‑compose.yml`, `.env.example` (sin credenciales sensibles) y el presente `README-Implementacion.md`.
2. **Carga inicial de datos**: incluir el CSV comprimido o un enlace público (por tamaño).
3. **Instrucciones**: este README actúa como guía end‑to‑end; basta con clonarlo y ejecutar los comandos de la sección *Instalación*.
4. **Opcional – Imágenes pre‑construidas**: publicar en Docker Hub con el tag `mlops1/wine‑airflow:latest`, etc., y ajustar el `docker‑compose.yml`.

---

## 8 Trabajo futuro
- Automatizar el registro del mejor modelo a **Production** y hacer que `fastapi` lo cargue correctamente (cerrar issue de restart).  
- Implementar búsqueda de hiper‑parámetros con `MLflow Autolog` + `scikit‑optimize`.  
- Dashboard de métricas en Grafana usando la DB de MLflow.

---

© 2025 | MLOps1 – CEIA – FIUBA

