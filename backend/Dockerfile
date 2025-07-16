# Verwende ein offizielles Python-Image als Basis
FROM python:3.10-slim-buster

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die requirements.txt in das Arbeitsverzeichnis
# und installiere die Abhängigkeiten.
# Dies wird vor dem Kopieren des gesamten Codes gemacht,
# um den Docker-Cache zu nutzen, wenn sich nur der Code ändert.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den gesamten Quellcode des Backends in das Arbeitsverzeichnis
# Hier kopieren wir den Inhalt des 'src'-Ordners in '/app/src'
COPY src /app/src

# Setze den PYTHONPATH, damit Python die Module in 'src' finden kann
ENV PYTHONPATH=/app/src

# Exponiere den Port, auf dem FastAPI standardmäßig läuft (oder den, den du konfigurierst)
EXPOSE 8000

# Befehl zum Starten der FastAPI-Anwendung mit Uvicorn
# Hier gehen wir davon aus, dass deine Haupt-FastAPI-App in 'src/main.py' liegt
# und die Anwendung als 'app' im Modul 'main' heißt.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]