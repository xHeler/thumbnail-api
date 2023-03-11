FROM python:3.8

# Installing all python dependencies
ADD requirements/ requirements/
RUN pip install -r requirements/local.txt

# Adds our application code to the image
COPY . code
WORKDIR code

CMD ["gunicorn","config.wsgi:application","--bind", "0.0.0.0:8000"]