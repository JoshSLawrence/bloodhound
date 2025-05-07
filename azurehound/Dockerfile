FROM --platform=linux/amd64 ubuntu:latest

WORKDIR /app

RUN apt update && \
    apt install -y zip unzip wget python3 python3-pip python3-venv

RUN python3 -m venv .venv

COPY requirements.txt .

RUN .venv/bin/pip install -r requirements.txt

COPY ingestdata.py .

COPY update.sh .

RUN wget https://github.com/SpecterOps/AzureHound/releases/download/v2.4.1/AzureHound_v2.4.1_linux_amd64.zip

RUN unzip AzureHound_v2.4.1_linux_amd64.zip

RUN rm AzureHound_v2.4.1_linux_amd64.zip

CMD ["bash", "-c", "bash update.sh"]
