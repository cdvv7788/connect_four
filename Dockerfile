FROM python:3.8-slim-buster
WORKDIR /app
COPY ./ /app/

RUN apt-get update \
    # dependencies for building Python packages
    && apt-get install -y build-essential 

RUN pip install --upgrade pip &&\
    pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0:8000"]
