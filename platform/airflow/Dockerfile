FROM apache/airflow:3.1.1

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends openjdk-17-jre-headless \
    && arch="$(dpkg --print-architecture)" \
    && ln -sfn "/usr/lib/jvm/java-17-openjdk-${arch}" /usr/lib/jvm/java-17 \
    && rm -rf /var/lib/apt/lists/*
USER airflow
RUN pip install --no-cache-dir \
    "pyspark==3.5.0" \
    "pandas==2.2.3" \
    "kafka-python-ng==2.2.3" \
    "dbt-core==1.9.4" \
    "dbt-duckdb==1.9.4" \
    "boto3==1.35.90"
ENV JAVA_HOME=/usr/lib/jvm/java-17
