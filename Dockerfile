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
# ARG SENHA
# ARG ASSINATURA
# ARG DATA_NASCIMENTO
# ARG CPF
# ARG SALDO_EXTERNO
# ARG STEP
# ENV SENHA=$SENHA
# ENV ASSINATURA=$ASSINATURA
# ENV DATA_NASCIMENTO=${DATA_NASCIMENTO}
# ENV CPF=${CPF}
# ENV SALDO_EXTERNO=${SALDO_EXTERNO}
# ENV STEP=${STEP}
CMD python3 main.py

