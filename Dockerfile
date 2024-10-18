FROM ubuntu:latest

WORKDIR /workspace 

RUN apt-get update && apt-get install -y \
    curl \
    zip \
    python3.12 \
    python3-pip \
    python3.12-venv \
    openjdk-17-jdk \
    git \
    && curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/*

COPY requirements.txt config_databricks.sh config_git.sh ./
RUN chmod +x config_databricks.sh config_git.sh

RUN python3 -m venv /.virtualenvs/.venv-spark \
    && /.virtualenvs/.venv-spark/bin/pip install -r requirements.txt \
    && python3 -m venv /.virtualenvs/.venv-databricks \
    && /.virtualenvs/.venv-databricks/bin/pip install -r requirements.txt \
    && /.virtualenvs/.venv-databricks/bin/pip install databricks-connect==15.4.2

CMD ["/bin/bash"]