# Projektarbeit Inbetriebnahme

Dieses Dokument beschreibt die Schritte, um die Anwendung lokal mit Docker Compose auszuführen.

## Voraussetzungen

Stellen Sie sicher, dass die folgenden Anwendungen auf Ihrem System installiert sind:

- **Docker & Docker Compose:** Wird benötigt, um die Anwendungscontainer zu erstellen und auszuführen.
- **Ollama:** Muss auf dem Host-System laufen, um die Sprachmodelle bereitzustellen. Die Anwendung ist so konfiguriert, dass sie Ollama auf `host.docker.internal` erwartet.

## Ausführung

1.  **Ollama starten:**
    Stellen Sie sicher, dass Ollama auf Ihrem Host-System läuft und das benötigte Modell geladen ist. Das in der Konfiguration verwendete Modell ist `deepseek-r1:32b`.

    ```bash
    ollama run deepseek-r1:32b
    ```

2.  **Anwendung starten:**
    Klonen Sie dieses Repository und führen Sie den folgenden Befehl im Hauptverzeichnis des Projekts aus, um die Anwendung zu starten:

    ```bash
    docker-compose up --build 
    ```

    Dieser Befehl baut die Docker-Images für das Backend und Frontend und startet alle in der `docker-compose.yaml` definierten Dienste im Hintergrund.

## Zugriff auf die Anwendung

Nachdem alle Container erfolgreich gestartet wurden, können Sie auf die verschiedenen Teile der Anwendung zugreifen:

- **Frontend:** Die Benutzeroberfläche ist unter [http://localhost:3000](http://localhost:3000) erreichbar.
- **Qdrant UI:** Die Benutzeroberfläche für die Vektordatenbank ist unter [http://localhost:6333/dashboard](http://localhost:6333/dashboard) verfügbar.
