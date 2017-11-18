FROM python:3.6
MAINTAINER Germain GAU <germain.gau@gmail.com>

ADD requirements.txt .
RUN pip install -r requirements.txt && \
  rm requirements.txt

WORKDIR /app
ADD src /app

CMD ["python", "-u", "main.py"]
