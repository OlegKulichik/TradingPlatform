FROM  python:3.8.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /usr/src/app/
WORKDIR  /usr/src/app/
COPY requirements.txt /usr/src/app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


COPY entrypoint.sh /usr/src/app/
RUN chmod +x /usr/src/app/entrypoint.sh

COPY . /usr/src/app/

CMD . /usr/src/app/entrypoint.sh