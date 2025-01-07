# Używamy obrazu Pythona
FROM python:3.9-slim

# Ustawiamy katalog roboczy w kontenerze
WORKDIR /app

# Kopiujemy pliki projektu do kontenera
COPY . /app

# Instalujemy zależności
RUN pip install --no-cache-dir django requests

# Otwieramy port dla serwera Django
EXPOSE 8000

# Uruchamiamy serwer Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
