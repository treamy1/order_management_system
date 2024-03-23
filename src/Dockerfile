# syntax=docker/dockerfile:1

FROM python:3.12
ADD app /app
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000
ENV FLASK_APP=/app
CMD ["flask", "run", "-h", "--host 0.0.0.0", "--port=5000"]