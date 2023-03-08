FROM python:3.8

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Installing all python dependencies
ADD requirements/ requirements/
RUN pip install -r requirements/local.txt

# Adds our application code to the image
COPY . code
WORKDIR code

# Run the production server
CMD newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT --access-logfile - src.wsgi:application
