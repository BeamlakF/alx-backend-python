FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

# Note: Port mapping with -p happens when running the container: docker run -p 8000:8000
# -p

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
