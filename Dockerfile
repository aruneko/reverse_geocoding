FROM python:3-slim

ENV APP_HOME /usr/src/reverse_geocoder
ENV PYTHONUNBUFFERED 1

WORKDIR $APP_HOME

COPY Pipfile Pipfile.lock ./
RUN apt update \
 && apt install -y gcc \
 && pip install pipenv \
 && pipenv install --system \
 && apt purge -y gcc \
 && apt autoremove -y \
 && rm -rf /var/lib/apt/lists/*

COPY reverse_geocoder .

EXPOSE 8000
CMD ["uvicorn", "reverse_geocoder.main:app", "--host", "0.0.0.0"]
