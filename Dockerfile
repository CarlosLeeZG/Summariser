FROM quay.io/unstructured-io/unstructured:latest

RUN curl -k https://curl.se/ca/cacert.pem -o /etc/pki/ca-trust/source/anchors/curl-cacert-updated.pem && update-ca-trust
COPY openai.crt /etc/pki/ca-trust/source/anchors/openai.pem 
RUN update-ca-trust


COPY requirements.txt /app/
WORKDIR /app

RUN pip3 install -i https://pypi.nerve-internal.mti.gov.sg --retries 1 --timeout 5 --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000

RUN groupadd -r nonrootgrp -g 333 && \
    useradd -u 334 -r -g nonrootgrp -s /sbin/nologin -c "non-root user" dockeruser

RUN chown dockeruser /app

USER dockeruser

#Needed for awslogs to pick up print lines
ENV PYTHONUNBUFFERED=1

EXPOSE 8501

HEALTHCHECK CMD curl --fail https://localhost:8501/doc-summary/_stcore/health


ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]


