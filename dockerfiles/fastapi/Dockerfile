# FROM python:3.8-slim
# 
# WORKDIR /app
# COPY . .
# COPY requirements.txt /requirements.txt
# 
# RUN apt-get update && apt-get install -y curl
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r /requirements.txt
# 
# EXPOSE 8800

FROM python:3.11-slim
WORKDIR /app
COPY api/ .
RUN pip install --no-cache-dir fastapi uvicorn[standard] mlflow==2.12.2 boto3 pandas scikit-learn textblob
EXPOSE 8800
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8800"]
