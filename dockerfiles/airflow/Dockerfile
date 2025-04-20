# dockerfiles/airflow/Dockerfile
FROM apache/airflow:2.8.1

###############################################################################
# 1) Instalar herramientas de sistema (git, etc) como root
###############################################################################
USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
         git \
    && apt-get autoremove -y --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

###############################################################################
# 2) Volver a airflow user para instalar boto3 y tus dependencias Python
###############################################################################
USER airflow

# pip install boto3 sin warnings de root
RUN pip install --no-cache-dir boto3

# Copiamos tu lista de requirements
COPY requirements.txt /requirements.txt

# Actualizamos pip y luego instalamos el resto
RUN pip install --upgrade pip --no-cache-dir \
    && pip install --no-cache-dir -r /requirements.txt

###############################################################################
# 3) Ya estamos listos: el ENTRYPOINT es el de airflow original
###############################################################################







