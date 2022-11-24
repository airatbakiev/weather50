FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip && pip3 install -r requirements.txt --no-cache-dir

COPY start.sh /app

RUN chmod +x start.sh

COPY ./ .

# CMD ["gunicorn", "project.wsgi:application", "--bind", "0:8000"]

CMD ["/bin/bash", "-c", "./startup.sh"]