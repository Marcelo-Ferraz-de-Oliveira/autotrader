#Build the Python backend
FROM python:3.10
WORKDIR /autotrader
RUN apt update
RUN apt install chromium-driver tzdata -y
COPY ./ ./
ENV TZ="America/Belem"
ENV DISPLAY=:99
RUN pip3 install -r requirements.txt
WORKDIR /autotrader
CMD python3 main.py

