# KI-basiertes Ticketsystem

Eine Projektarbeit für das Studium, die ein intelligentes Ticketsystem mit KI-gestützter Antwortgenerierung implementiert.

## Überblick

Das KI-basierte Ticketsystem ist eine vollständige Webanwendung, die es Benutzern ermöglicht, Fragen zu stellen und automatisch relevante Antworten aus einer Wissensdatenbank zu erhalten. Das System verwendet moderne KI-Technologien wie Vector Embeddings und Large Language Models (LLMs), um intelligente und kontextbezogene Antworten zu generieren.

## Theoretische Grundlagen

### Information Retrieval und Similarity Search

Das System basiert auf modernen Information Retrieval (IR) Techniken, die darauf abzielen, relevante Informationen aus einer großen Sammlung von Dokumenten oder Daten zu finden. Im Kontext dieses Ticketsystems werden zwei komplementäre Ansätze verwendet:

#### Dense Retrieval
Dense Retrieval verwendet neuronale Netzwerke, um sowohl Anfragen als auch Dokumente in einen gemeinsamen, hochdimensionalen Vektorraum zu transformieren. Diese Embeddings erfassen semantische Beziehungen zwischen Texten, auch wenn sie keine gemeinsamen Begriffe enthalten. Die Ähnlichkeit wird typischerweise durch Cosine-Similarity oder Dot-Product berechnet.

**Vorteile:**
- Erfassung semantischer Ähnlichkeiten
- Robustheit gegenüber Paraphrasierung
- Bessere Performance bei konzeptionellen Anfragen

**Nachteile:**
- Weniger präzise bei exakten Keyword-Matches
- Höhere Rechenkosten
- "Black Box" Verhalten

#### Sparse Retrieval
Sparse Retrieval basiert auf klassischen IR-Techniken wie TF-IDF oder BM25, die auf der Häufigkeit und Verteilung von Begriffen in Dokumenten beruhen. Diese Methoden erstellen sparse Vektoren, in denen die meisten Dimensionen null sind.

**Vorteile:**
- Hohe Präzision bei exakten Keyword-Matches
- Interpretierbarkeit der Ergebnisse
- Geringere Rechenkosten

**Nachteile:**
- Schwäche bei semantischen Beziehungen
- Anfälligkeit für Vocabulary Mismatch
- Begrenzte Kontextberücksichtigung

#### Hybrid Retrieval
Der hybride Ansatz kombiniert die Stärken beider Methoden durch Fusion-Techniken wie Reciprocal Rank Fusion (RRF). RRF aggregiert die Rankings verschiedener Retrieval-Systeme, ohne die absoluten Scores zu benötigen, was es robust gegenüber unterschiedlichen Score-Verteilungen macht.

### Vector Embeddings und Similarity Search

Vector Embeddings transformieren Text in numerische Repräsentationen, die semantische Beziehungen in einem kontinuierlichen Vektorraum kodieren. Das verwendete Modell "mixedbread-ai/mxbai-embed-large-v1" ist ein speziell für Retrieval-Aufgaben optimiertes Transformer-basiertes Modell.

#### Eigenschaften der verwendeten Embeddings:
- **Dimensionalität**: 1024 Dimensionen bieten einen guten Kompromiss zwischen Ausdruckskraft und Effizienz
- **Normalisierung**: Einheitsvektoren ermöglichen die Verwendung von Cosine-Similarity
- **Kontextualisierung**: Bidirektionale Attention-Mechanismen erfassen den gesamten Kontext

### Large Language Models (LLMs) und Prompt Engineering

Das System nutzt Gemma 3:1b, ein Transformer-basiertes Large Language Model, für die finale Antwortgenerierung. LLMs haben die Fähigkeit, natürliche Sprache zu verstehen und zu generieren, basierend auf statistischen Mustern aus großen Textkorpora.

#### Funktionsweise im System:
1. **Kontextuelle Analyse**: Das LLM bewertet die Relevanz der gefundenen Frage-Antwort-Paare
2. **Antwortgenerierung**: Basierend auf den relevanten Kontexten wird eine kohärente Antwort formuliert
3. **Strukturierte Ausgabe**: Durch Pydantic-Schemas wird eine konsistente JSON-Ausgabe gewährleistet

#### Prompt Engineering Strategien:
- **Few-Shot Learning**: Beispiele in den Prompts verbessern die Antwortqualität
- **Instruktions-basierte Prompts**: Klare Anweisungen definieren das gewünschte Verhalten
- **Strukturierte Ausgabe**: JSON-Schema enforcement für maschinell verarbeitbare Antworten

### Retrieval-Augmented Generation (RAG)

Das System implementiert eine RAG-Architektur, die die Stärken von Information Retrieval und Textgenerierung kombiniert:

1. **Retrieval Phase**: Relevante Dokumente werden über Vector Search gefunden
2. **Augmentation Phase**: Die gefundenen Dokumente werden als Kontext für das LLM verwendet
3. **Generation Phase**: Das LLM generiert eine Antwort basierend auf dem erweiterten Kontext

#### Vorteile von RAG:
- **Faktische Genauigkeit**: Antworten basieren auf verfügbaren Dokumenten
- **Aktualität**: Wissensbasis kann ohne Model-Retraining aktualisiert werden
- **Nachvollziehbarkeit**: Quellen der Antworten sind identifizierbar
- **Effizienz**: Kleinere LLMs können durch externen Kontext verstärkt werden

### Vector Databases und Qdrant

Qdrant ist eine spezialisierte Vector Database, die für Similarity Search optimiert ist. Im Gegensatz zu traditionellen relationalen Datenbanken speichert sie hochdimensionale Vektoren und bietet effiziente Nearest Neighbor Search.

#### Technische Eigenschaften:
- **HNSW-Index**: Hierarchical Navigable Small World Algorithmus für schnelle ANN-Suche
- **Multi-Vector Support**: Separate Vektoren für verschiedene Modalitäten (Fragen/Antworten)
- **Filtering**: Kombination von Vektor-Similarity und traditionellen Filtern
- **Skalierbarkeit**: Horizontale Skalierung für große Datenmengen

## Architektur

Das System besteht aus drei Hauptkomponenten:

- **Frontend (React)**: Benutzeroberfläche für die Interaktion mit dem System
- **Backend (FastAPI)**: REST API für die Geschäftslogik und KI-Integration
- **Datenbank Stack**: Qdrant (Vector Database) + MongoDB für Datenpersistierung

## Hauptfunktionen

### Für Benutzer:
- **Frage stellen**: Neue Tickets/Fragen über das Frontend einreichen
- **Automatische Antworten**: KI-generierte Antworten basierend auf ähnlichen vergangenen Fragen
- **Antwort-Feedback**: Möglichkeit, Antworten als korrekt zu markieren oder abzulehnen

### Für Administratoren:
- **Unbeantwortete Fragen**: Übersicht über Fragen ohne automatische Antworten
- **Manuelle Bearbeitung**: Möglichkeit, Antworten manuell hinzuzufügen
- **Qualitätskontrolle**: Verwaltung und Verbesserung der Wissensdatenbank

## Technischer Aufbau

### Backend-Technologien
- **FastAPI**: Moderne, schnelle Web-API Framework
- **Qdrant**: Vector Database für Similarity Search
- **Ollama**: Lokale LLM-Integration (Standard: Gemma 3:1b)
- **FastEmbed**: Text-Embeddings mit "mixedbread-ai/mxbai-embed-large-v1"
- **MongoDB**: Dokumentendatenbank für Metadaten

### Frontend-Technologien
- **React 19**: Moderne Frontend-Bibliothek
- **Vite**: Build-Tool und Development Server
- **Tailwind CSS**: Utility-First CSS Framework
- **Headless UI**: Accessible UI-Komponenten
- **React Router**: Client-side Routing

### Vector Search und KI
Das System implementiert einen **hybriden Ansatz** für die Suche:

1. **Dense Embeddings**: Semantische Ähnlichkeit durch BERT-ähnliche Modelle
2. **Sparse Embeddings**: Klassische Keyword-basierte Suche (BM25-ähnlich)
3. **Fusion**: Kombination beider Ansätze mit Reciprocal Rank Fusion (RRF)

### Workflow der Antwortgenerierung

```
1. Benutzer stellt Frage
   ↓
2. Frage wird in Vector Embeddings umgewandelt
   ↓
3. Similarity Search in Qdrant Vector Database
   ↓
4. Top-5 ähnliche Frage-Antwort-Paare werden abgerufen
   ↓
5. LLM analysiert die Ergebnisse und generiert Antwort
   ↓
6. Antwort wird zurückgegeben und gespeichert
```

## Implementierungsdetails

### Backend-Architektur
Das Backend folgt einer modularen Architektur mit klarer Trennung der Verantwortlichkeiten:

- **main.py**: FastAPI-Anwendung mit CORS-Middleware und Routing
- **handlers.py**: Business Logic für Request/Response-Verarbeitung
- **stores_dense.py**: Qdrant-Integration und Vector Operations
- **llm.py**: LLM-Integration mit strukturierter Ausgabe
- **db.py**: Datenbankabstraktionen und CRUD-Operationen

### Frontend-Architektur
Das React-Frontend implementiert eine Single Page Application (SPA) mit:

- **Component-basierte Architektur**: Wiederverwendbare UI-Komponenten
- **State Management**: React Hooks für lokalen State
- **Routing**: Client-side Navigation mit React Router
- **API Integration**: RESTful API-Kommunikation

### Datenmodell
Das System verwendet ein hybrides Datenmodell:

**Qdrant (Vector Storage):**
```json
{
  "id": "uuid",
  "vector": {
    "questions": [1024 float values],
    "answers": [1024 float values]
  },
  "payload": {
    "question": "string",
    "answer": "string",
    "isCorrect": "boolean",
    "omittedAnswers": ["array of strings"]
  }
}
```

**MongoDB (Metadata):**
- Zusätzliche Metadaten und Relationen
- User-Management und Session-Daten
- Audit-Logs und Analytics

## Projektstruktur

```
Projektarbeit/
├── docker-compose.yaml          # Container Orchestrierung
├── README.md                    # Diese Datei
├── notes.md                     # Entwicklungsnotizen
├── backend/                     # Python FastAPI Backend
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src/
│       ├── main.py             # FastAPI Anwendung
│       ├── handlers.py         # Request Handler
│       ├── llm.py              # LLM Integration (Ollama)
│       ├── stores_dense.py     # Qdrant Vector Store
│       ├── db.py              # Datenbankoperationen
│       ├── embeddings/         # Embedding-Module
│       └── vector_stores/      # Vector Store Implementierungen
└── frontend_user/              # React Frontend
    ├── Dockerfile
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── App.jsx             # Haupt-App-Komponente
        ├── main.jsx            # React Entry Point
        └── components/         # UI-Komponenten
            ├── chat-window.jsx
            ├── new-question.jsx
            ├── sidebar.jsx
            └── views.jsx
```

## Installation und Setup

### Voraussetzungen
- Docker und Docker Compose
- Ollama (für lokale LLM-Inferenz)

### 1. Repository klonen
```bash
git clone <repository-url>
cd Projektarbeit
```

### 2. Ollama installieren und Model laden
```bash
# Ollama installieren (siehe https://ollama.ai)
ollama pull gemma3:1b
```

### 3. System starten
```bash
docker-compose up -d
```

### 4. Services überprüfen
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Qdrant Dashboard**: http://localhost:6333/dashboard
- **MongoDB**: localhost:27017

## API Endpoints

### Fragen
- `GET /questions` - Alle Fragen abrufen
- `POST /questions` - Neue Frage stellen
- `GET /questions/{id}` - Spezifische Frage abrufen

### Antworten
- `POST /questions/{id}/answer` - Manuelle Antwort hinzufügen
- `POST /questions/{id}/omit` - Antwort ablehnen
- `POST /questions/{id}/correct` - Antwort als korrekt markieren

## Besondere Features

### Intelligente Suche
- **Multi-Vector Search**: Separate Embeddings für Fragen und Antworten
- **Fusion Query**: Kombiniert verschiedene Suchstrategien
- **Filtering**: Sucht nur in beantworteten Fragen

### LLM Integration
- **Strukturierte Ausgabe**: Pydantic-Modelle für konsistente Antworten
- **Kontextuelle Analyse**: LLM entscheidet, ob gefundene Antworten relevant sind
- **Mehrsprachigkeit**: Antwortet in der Sprache der ursprünglichen Frage

### Feedback-System
- **Antwort-Bewertung**: Benutzer können Antworten als korrekt/falsch markieren
- **Iterative Verbesserung**: Omitted Answers werden für spätere Verbesserungen gespeichert
- **Admin-Interface**: Separate Ansicht für unbeantwortete Fragen

## Evaluation und Metriken

### Qualitätsmessung
Das System implementiert verschiedene Metriken zur Bewertung der Antwortqualität:

#### Retrieval-Metriken:
- **Precision@k**: Anteil relevanter Dokumente in den Top-k Ergebnissen
- **Recall@k**: Anteil gefundener relevanter Dokumente von allen relevanten
- **Mean Reciprocal Rank (MRR)**: Durchschnittlicher Kehrwert der Position der ersten relevanten Antwort

#### Generation-Metriken:
- **BLEU Score**: N-gram basierte Ähnlichkeit zu Referenzantworten
- **ROUGE Score**: Overlap-basierte Bewertung der Antwortqualität
- **Semantic Similarity**: Cosine-Similarity zwischen generierten und Referenz-Embeddings

#### User Experience Metriken:
- **User Satisfaction Score**: Explicit Feedback durch Bewertungssystem
- **Answer Acceptance Rate**: Prozentsatz als korrekt markierter Antworten
- **Response Time**: Latenz von Anfrage bis Antwort

### Performance Optimierung

#### Vector Search Optimierung:
- **Index-Tuning**: HNSW-Parameter für optimale Balance zwischen Geschwindigkeit und Genauigkeit
- **Batch Processing**: Gruppenweise Verarbeitung von Embedding-Anfragen
- **Caching**: Redis-basiertes Caching häufiger Anfragen

#### LLM Optimierung:
- **Model Quantization**: Reduzierte Präzision für schnellere Inferenz
- **Prompt Caching**: Wiederverwendung von Prompt-Templates
- **Parallel Processing**: Asynchrone Verarbeitung mehrerer Anfragen

## Herausforderungen und Lösungsansätze

### Technische Herausforderungen

#### Cold Start Problem
**Problem**: Neue Systeme ohne historische Daten können keine qualitativ hochwertigen Antworten generieren.
**Lösung**: Implementation synthetischer Datengeneration durch LLMs zur Erstellung initialer Frage-Antwort-Paare.

#### Embedding Drift
**Problem**: Änderungen im Embedding-Model können bestehende Vektoren inkompatibel machen.
**Lösung**: Versionierung der Embeddings und schrittweise Migration mit Backward-Compatibility.

#### Scalability Bottlenecks
**Problem**: Wachsende Datenmengen führen zu Performance-Problemen bei der Suche.
**Lösung**: Hierarchische Indizierung und Partitionierung der Vector Database.

### Qualitätssicherung

#### Halluzination Prevention
**Problem**: LLMs können Informationen erfinden, die nicht in den Quelldaten enthalten sind.
**Lösung**: Strenge Kontextbindung und Confidence-Scoring für generierte Antworten.

#### Bias Mitigation
**Problem**: Vorurteile in Trainingsdaten können zu unfairen oder diskriminierenden Antworten führen.
**Lösung**: Diversitäts-Checks in der Trainingsdatenauswahl und Bias-Detection in Antworten.

#### Answer Consistency
**Problem**: Unterschiedliche Antworten auf identische oder sehr ähnliche Fragen.
**Lösung**: Deduplication-Mechanismen und Konsistenz-Checks über die Wissensbasis.

## Geplante Verbesserungen

Basierend auf den Entwicklungsnotizen sind folgende Erweiterungen geplant:

1. **Synthetische Datengeneration**: Automatische Generierung ähnlicher Fragen für besseres Training
2. **RAG in Dokumenten**: Integration von Dokumenten-basierter Suche
3. **Erweiterte Embeddings**: 
   - Matryoshka Embeddings für bessere Effizienz
   - Late Interaction Embeddings für präzisere Suche
4. **Verbessertes Prompt Engineering**: Optimierung der LLM-Prompts
5. **User Feedback Integration**: Systematische Nutzung von Nutzerfeedback

### Erweiterte Funktionalitäten

#### Multi-Modal Support
Integration von Bild- und Dokumenten-basierter Suche für umfassendere Antworten:
- **Vision-Language Models**: Verarbeitung von Screenshots und Diagrammen
- **Dokument-Parser**: Extraktion von Text aus PDFs und Office-Dokumenten
- **Cross-Modal Retrieval**: Suche über verschiedene Datentypen hinweg

#### Advanced Analytics
Implementation von Analytics-Dashboards für bessere Systemtransparenz:
- **Usage Patterns**: Analyse häufiger Fragetypen und Antwortqualität
- **Performance Monitoring**: Real-time Überwachung von System-Metriken
- **A/B Testing**: Experimentelle Evaluation verschiedener Algorithmus-Varianten

#### Personalization
Benutzer-spezifische Anpassung der Antwortgenerierung:
- **User Profiling**: Erlernen individueller Präferenzen und Expertise-Level
- **Contextual Adaptation**: Anpassung an Benutzerkontext und -historie
- **Federated Learning**: Privacy-preserving Personalisierung

## Entwicklung

### Lokale Entwicklung
```bash
# Backend (in backend/ Verzeichnis)
pip install -r requirements.txt
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (in frontend_user/ Verzeichnis)
npm install
npm run dev
```

### Testing
```bash
# Backend Tests
pytest

# Frontend Tests
npm test
```

### Continuous Integration/Continuous Deployment (CI/CD)

#### Testing Strategy
```bash
# Unit Tests
pytest backend/tests/unit/

# Integration Tests  
pytest backend/tests/integration/

# End-to-End Tests
npm run test:e2e
```

#### Deployment Pipeline
```yaml
# GitHub Actions Workflow
stages:
  - lint: ESLint, Black, mypy
  - test: Unit, Integration, E2E
  - build: Docker Images
  - deploy: Staging, Production
```

## Technische Details

### Vector Embeddings
- **Model**: mixedbread-ai/mxbai-embed-large-v1
- **Dimensionen**: 1024
- **Distance Metric**: Cosine Similarity
- **Prefetch Limit**: 10 pro Vector Type

### LLM Configuration
- **Default Model**: Gemma 3:1b
- **Host**: Ollama (localhost:11434)
- **Response Format**: Strukturiert über Pydantic
- **Streaming**: Deaktiviert für konsistente Ergebnisse

### Database Configuration
- **Qdrant**: Vector Database mit HNSW-Index
- **MongoDB**: Dokumentendatenbank für Metadaten
- **Connection Pooling**: Optimierte Datenbankverbindungen
- **Backup Strategy**: Automatische Sicherung kritischer Daten

### Security Considerations
- **API Rate Limiting**: Schutz vor DDoS-Attacken
- **Input Sanitization**: Validierung aller Benutzereingaben
- **CORS Policy**: Konfigurierte Cross-Origin-Policies
- **Data Privacy**: DSGVO-konforme Datenverarbeitung

## Related Work und Literatur

### Relevante Forschungsarbeiten

#### Dense Passage Retrieval
Karpukhin et al. (2020) führten Dense Passage Retrieval (DPR) ein, das duale Encoder für Fragen und Passagen verwendet. Ihre Arbeit zeigte, dass dense Retrieval traditionelle sparse Methoden bei Open-Domain Question Answering übertreffen kann.

#### Retrieval-Augmented Generation
Lewis et al. (2020) stellten RAG vor, welches parametrisches Wissen (LLM) mit non-parametrischem Wissen (externe Wissensbasis) kombiniert. Dies ermöglicht aktuellere und faktisch genauere Antworten.

#### Hybrid Retrieval Systems
Ma et al. (2021) untersuchten die Kombination von dense und sparse Retrieval-Methoden und entwickelten Fusion-Techniken wie Reciprocal Rank Fusion für verbesserte Retrieval-Performance.

#### ColBERT und Late Interaction
Khattab & Zaharia (2020) entwickelten ColBERT, ein Late Interaction Model, das die Effizienz von sparse Retrieval mit der Effektivität von dense Retrieval kombiniert.

### Technologische Grundlagen

#### Transformer Architecture
Vaswani et al. (2017) "Attention Is All You Need" legte den Grundstein für moderne NLP-Modelle durch die Einführung der Transformer-Architektur.

#### BERT und Bidirectional Encoding
Devlin et al. (2018) entwickelten BERT, das bidirektionale Encoder-Repräsentationen aus Transformers nutzt und den Standard für viele NLP-Aufgaben setzte.

#### Vector Databases
Pinecone, Weaviate, Qdrant und andere spezialisierte Vector Databases entstanden als Antwort auf den Bedarf nach effizienter Similarity Search in hochdimensionalen Räumen.

## Fazit und Ausblick

Das entwickelte KI-basierte Ticketsystem demonstriert erfolgreich die Integration moderner KI-Technologien in ein praktisches Anwendungsszenario. Durch die Kombination von Vector Embeddings, hybrider Suche und Large Language Models wurde ein System geschaffen, das automatisch relevante Antworten auf Benutzeranfragen generieren kann.

### Zentrale Erkenntnisse

1. **Hybrid Retrieval übertrifft einzelne Ansätze**: Die Kombination von dense und sparse Retrieval liefert bessere Ergebnisse als jeder Ansatz allein.

2. **Strukturierte LLM-Ausgaben erhöhen Zuverlässigkeit**: Pydantic-basierte Schema-Validierung verhindert inkonsistente API-Responses.

3. **User Feedback ist essentiell**: Das Bewertungssystem ermöglicht kontinuierliche Verbesserung der Antwortqualität.

4. **Modulare Architektur erleichtert Erweiterungen**: Die klare Trennung von Retrieval, Generation und Präsentation ermöglicht einfache Upgrades einzelner Komponenten.

### Limitationen

- **Kaltstartproblem**: Ohne ausreichende historische Daten ist die Antwortqualität initial begrenzt
- **Sprachabhängigkeit**: Das System ist primär für deutsche/englische Texte optimiert
- **Computational Overhead**: LLM-Inferenz und Vector Search erfordern erhebliche Rechenressourcen
- **Halluzination Risk**: LLMs können trotz RAG-Architektur gelegentlich erfundene Informationen generieren

### Zukunftsperspektiven

Die Weiterentwicklung des Systems könnte folgende Richtungen einschlagen:

1. **Multimodale Integration**: Erweiterung um Bild- und Dokumentenverarbeitung
2. **Federated Learning**: Privacy-preserving Verbesserung über mehrere Organisationen hinweg
3. **Causal Reasoning**: Integration kausaler Inferenz für komplexere Problemlösungen
4. **Real-time Learning**: Online-Adaptation basierend auf Benutzerinteraktionen

Das Projekt zeigt, dass moderne KI-Technologien bereits heute in der Lage sind, praktische Probleme in Unternehmensumgebungen zu lösen, während es gleichzeitig wichtige Forschungsrichtungen für zukünftige Entwicklungen aufzeigt.

## Beitrag

Dieses Projekt ist eine Studienarbeit. Für Verbesserungsvorschläge oder Fragen zum Code, bitte Issues erstellen oder Pull Requests einreichen.

## Lizenz

Dieses Projekt ist für Bildungszwecke erstellt und unterliegt den entsprechenden akademischen Richtlinien.

---

**Projektarbeit**: KI-basiertes Ticketsystem  
**Entwickelt mit**: modernen KI-Technologien und bewährten Software-Engineering-Praktiken
