FROM openjdk:17-jdk-slim-bullseye

WORKDIR /workspace 
COPY . .

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt
CMD ["/bin/bash"]