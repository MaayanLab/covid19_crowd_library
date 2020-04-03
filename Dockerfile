FROM debian:stable

RUN set -x \
  && echo "Preparing user..." \
  && useradd -ms /bin/bash -d /app app

ADD deps.txt /app/deps.txt
RUN set -x \
  && echo "Installing system dependencies from deps.txt..." \
  && apt-get -y update \
  && apt-get -y install $(grep -v '^#' /app/deps.txt) \
  && rm /app/deps.txt

ADD requirements.txt /app/requirements.txt
RUN set -x \
  && echo "Installing python dependencies from requirements.txt..." \
  && pip3 install -Ivr /app/requirements.txt \
  && rm /app/requirements.txt

ADD alembic.ini /app/alembic.ini

EXPOSE 80
ADD boot.sh /app/boot.sh
RUN set -x && chmod +x /app/boot.sh
CMD /app/boot.sh

ADD app /app/app
RUN set -x && chown app:app -R /app/
