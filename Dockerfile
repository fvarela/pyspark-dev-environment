FROM ubuntu:latest

WORKDIR /workspace 
COPY databricks-cli-config /root/.databrickscfg
RUN apt-get update && apt-get install -y \
curl \
zip \
python3.12 \
python3-pip \
python3.12-venv \
openjdk-17-jdk \
&& curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh

COPY requirements.txt .

RUN python3 -m venv /.virtualenvs/.venv-spark
RUN python3 -m venv /.virtualenvs/.venv-databricks

RUN /.virtualenvs/.venv-spark/bin/pip install -r requirements.txt 
RUN /.virtualenvs/.venv-databricks/bin/pip install -r requirements.txt  
RUN /.virtualenvs/.venv-databricks/bin/pip install databricks-connect==15.4.2
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/*
    
CMD ["/bin/bash"]