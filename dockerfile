FROM python:3.11-slim

ENV PATH="${PATH}:/usr/local/lib/python3.10/site-packages"
ENV PATH="${PATH}:/usr/local/lib/python3.10"
ENV PATH="${PATH}:/usr/local/lib"

WORKDIR /app

RUN apt-get clean
RUN apt-get update && apt-get install -y \
    ffmpeg \
    default-jre-headless 

# Upgrade pip and install requirements
COPY requirements.txt requirements.txt
COPY packages.txt packages.txt
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install --upgrade streamlit 

# Copy app code and set working directory
COPY . .

# Expose port you want your app on
EXPOSE 8080

# Run
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]