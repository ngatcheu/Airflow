FROM apache/airflow:3.1.2

USER root
# Librairies pour compiler python-ldap
RUN apt-get update && apt-get install -y \
    libsasl2-dev \
    libldap2-dev \
    libssl-dev \
    gcc \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /opt/airflow/

USER airflow
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt