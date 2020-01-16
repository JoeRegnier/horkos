FROM python:3.6

RUN mkdir horkos-ui
ADD . /horkos-ui
WORKDIR /horkos-ui

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "start.sh"]