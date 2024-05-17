FROM python:3.11-slim

ENV PATH="${PATH}:/usr/local/lib/python3.10/site-packages"
ENV PATH="${PATH}:/usr/local/lib/python3.10"
ENV PATH="${PATH}:/usr/local/lib"

WORKDIR /app

RUN apt-get clean
RUN apt-get update && apt-get install -y \
    ffmpeg \
    default-jre-headless 

COPY requirements.txt requirements.txt
COPY packages.txt packages.txt
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install --upgrade streamlit 

COPY . .

EXPOSE 8080

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]