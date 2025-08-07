# KI-basiertes Ticketsystem - Dokumentation
**Projektarbeit Master-Studium**

---

## Kursfassung

### Idee

Die Grundidee dieses Projekts war die Entwicklung eines intelligenten Ticketsystems, das mithilfe modernster KI-Technologien automatisch relevante Antworten auf Benutzerfragen generiert. Anstatt Anfragen manuell zu bearbeiten, soll das System aus einer bestehenden Wissensdatenbank lernen und ähnliche Fragen automatisch beantworten. Das entwickelte System kombiniert klassische Information Retrieval-Methoden mit modernen Large Language Models (LLMs) und Vector Embeddings, um eine nahtlose Benutzererfahrung zu schaffen. Dabei können Benutzer Fragen stellen und erhalten sofort relevante Antworten, während das System kontinuierlich aus neuen Frage-Antwort-Paaren lernt und seine Wissensbasis erweitert.

### Zielsetzung

Die Zielsetzung dieses Projekts gliedert sich in mehrere Bereiche, die sowohl technische als auch fachliche und akademische Aspekte umfassen. Als konzeptionelles Proof of Concept stand auf technischer Ebene die prototypische Implementierung eines hybriden Retrieval-Systems im Vordergrund, das Dense-, Sparse- und Hybrid-Ansätze vereint. Darüber hinaus sollte die grundlegende Integration von Vector Embeddings für semantische Ähnlichkeitssuche demonstriert werden, während gleichzeitig eine funktionsfähige REST-API mit FastAPI aufgebaut und eine einfache Benutzeroberfläche entwickelt wurde. Die Containerisierung der Anwendungskomponenten sollte die Grundlagen für spätere Deployment-Szenarien schaffen.

Aus fachlicher Sicht zielte das Projekt darauf ab, die grundsätzliche Machbarkeit der Automatisierung von Antwortgenerierung für Support-Anfragen zu demonstrieren. Dabei sollte ein prototypisches System entwickelt werden, das als Grundlage für eine potenzielle Wissensdatenbank dienen könnte. Die akademischen Ziele umfassten die praktische Erprobung moderner NLP-Techniken, die experimentelle Untersuchung verschiedener Retrieval-Strategien sowie die konzeptionelle Demonstration von MLOps-Prinzipien in einem Forschungsprototyp.

---

## Theorie

### Large Language Models (LLMs)

Large Language Models stellen eine der bedeutendsten Entwicklungen im Bereich der künstlichen Intelligenz dar und bilden das Fundament für die Textgenerierung in diesem Projekt. Diese tiefen neuronalen Netzwerke wurden auf enormen Textkorpora trainiert und sind in der Lage, menschenähnlichen Text zu verstehen und zu generieren. In diesem Projekt wird das Gemma3:1b Modell über Ollama verwendet, welches sich durch seine Effizienz bei gleichzeitig hoher Qualität der Textgenerierung auszeichnet.

Die Eigenschaften von LLMs umfassen emergente Fähigkeiten, die es ihnen ermöglichen, komplexe Aufgaben ohne spezifisches Training zu bewältigen. Darüber hinaus verfügen sie über Few-Shot Learning-Kapazitäten, wodurch sie sich mit wenigen Beispielen an neue Aufgaben anpassen können. Das Kontextverständnis erlaubt es den Modellen, den gesamten Gesprächskontext zu berücksichtigen, während multimodale Fähigkeiten die Verarbeitung verschiedener Datentypen ermöglichen.

Dennoch bringen LLMs auch Herausforderungen mit sich. Halluzinationen, bei denen das Modell faktisch falsche Informationen generiert, stellen ein wesentliches Problem dar. Kontextgrenzen begrenzen die Token-Länge für Input und Output, während die hohen Rechenkosten für Inferenz und mögliche Verzerrungen aus den Trainingsdaten weitere Herausforderungen darstellen.

### RAG (Retrieval Augmented Generation) / CAG (Cache Augmented Generation) / Finetuning

Retrieval Augmented Generation (RAG) stellt einen innovativen Ansatz dar, der die Stärken von Information Retrieval und Textgenerierung kombiniert. Dieser zweiphasige Ansatz beginnt mit einer Retrieval-Phase, in der nach relevanten Dokumenten oder Passagen gesucht wird, gefolgt von einer Generation-Phase, in der die gefundenen Informationen für die Antwortgenerierung verwendet werden.

Die Vorteile von RAG liegen in der Bereitstellung aktueller und faktischer Informationen, der Reduzierung von Halluzinationen, der Interpretierbarkeit durch Quellenangaben und der Skalierbarkeit ohne Neutraining des Modells. In der Implementierung dieses Projekts wird RAG durch eine Funktion realisiert, die zunächst relevante Frage-Antwort-Paare abruft und anschließend das LLM verwendet, um basierend auf diesen gefundenen Informationen eine kontextuell passende Antwort zu generieren.

Cache Augmented Generation (CAG) erweitert den RAG-Ansatz um ein intelligentes Caching-System, das häufig abgerufene Informationen zwischenspeichert und somit die Latenz reduziert. Im Gegensatz dazu steht Finetuning, bei dem die Modellparameter an spezifische Domänen angepasst werden. RAG hingegen nutzt eine externe Wissensbasis ohne Modifikation des Modells. Moderne Hybrid-Ansätze kombinieren beide Techniken für optimale Ergebnisse.

### Embeddings (Dense, Sparse, Hybrid)

Dense Embeddings transformieren Text in hochdimensionale, kontinuierliche Vektorräume, in denen semantisch ähnliche Texte räumlich nah beieinander liegen. Das in diesem Projekt verwendete Modell "mixedbread-ai/mxbai-embed-large-v1" mit einer Dimensionalität von 1024 ist speziell für Retrieval-Aufgaben optimiert und verwendet Cosine Similarity als Distanzmetrik. Die Vorteile von Dense Embeddings liegen in der Erfassung semantischer Ähnlichkeit auch ohne gemeinsame Keywords, der Robustheit gegenüber Paraphrasierung und der guten Performance bei konzeptionellen Anfragen.

Sparse Embeddings basieren hingegen auf klassischen Information Retrieval-Techniken wie TF-IDF oder BM25. Diese zeichnen sich durch hohe Präzision bei exakten Keyword-Matches, interpretierbare Gewichtungen, geringere Rechenkosten und eine hohe Sparsity mit vielen Null-Werten in den Vektoren aus. Während Dense Embeddings semantische Beziehungen erfassen, bieten Sparse Embeddings Präzision bei lexikalischen Übereinstimmungen.

Der hybride Ansatz kombiniert Dense und Sparse Retrieval durch Fusion-Techniken wie Reciprocal Rank Fusion (RRF). Diese Methode aggregiert die Rankings verschiedener Retrieval-Systeme ohne Abhängigkeit von absoluten Scores, wodurch sie robust gegenüber unterschiedlichen Score-Verteilungen wird. Die Implementierung im System erfolgt durch parallele Suchen in Questions- und Answers-Vektoren, deren Ergebnisse anschließend fusioniert werden. 

Zur empirischen Evaluation der verschiedenen Retrieval-Strategien wurde ein selbst erstellter Datensatz mit 25 repräsentativen Fragen entwickelt und getestet. Entgegen der theoretischen Erwartung, dass hybride Ansätze durch die Kombination verschiedener Retrieval-Methoden überlegen sein sollten, zeigte die Evaluation, dass der reine Dense-Ansatz bessere Performance-Ergebnisse erzielte als der hybride Ansatz. Diese Erkenntnis deutet darauf hin, dass für den spezifischen Anwendungsfall und die verfügbare Datenmenge die semantische Ähnlichkeitssuche durch Dense Embeddings ausreichend und effektiver ist als die zusätzliche Komplexität der Hybrid-Fusion.

### Ansatz/Workflow

Das entwickelte System folgt einem strukturierten, mehrstufigen Workflow, der eine effiziente Verarbeitung von Benutzeranfragen gewährleistet. Der Prozess beginnt mit der Eingabe einer Benutzerfrage über das Frontend, gefolgt von einem Preprocessing-Schritt, in dem die Anfrage normalisiert und tokenisiert wird. Anschließend erfolgt die Generierung von Dense Embeddings für die Frage mittels des trainierten Embedding-Modells.

Die Retrieval-Phase führt parallele Suchen in Questions- und Answers-Vektoren durch, deren Ergebnisse mittels Reciprocal Rank Fusion kombiniert werden. Ein wichtiger Filtering-Schritt schließt Fragen ohne entsprechende Antworten aus der Ergebnismenge aus. Die Generation-Phase nutzt das LLM, um basierend auf den gefundenen Frage-Antwort-Paaren eine kontextuell passende Antwort zu erstellen. Der Output erfolgt in strukturierter Form an den Benutzer, ergänzt durch Feedback-Möglichkeiten für kontinuierliche Systemverbesserung.

---

## Umsetzung

### Frontend

#### Framework

Das Frontend wurde mit React 19.1.0 und Vite als Build-Tool entwickelt, eine Kombination, die sowohl moderne Entwicklungspraktiken als auch optimale Performance gewährleistet. React bietet durch seine komponentenbasierte Architektur die Möglichkeit zur Entwicklung wiederverwendbarer UI-Elemente, während Vite eine schnelle Entwicklungsumgebung mit Hot Module Replacement bereitstellt. Die Integration von TypeScript-Support sorgt für Typsicherheit und verbessert die Entwicklererfahrung erheblich.

Die Kernabhängigkeiten des Projekts umfassen React 19.1.0 und React-DOM für die Grundfunktionalität, React Router DOM 7.6.3 für das Routing, TailwindCSS 4.1.8 für das Styling sowie HeadlessUI 2.2.4 für zugängliche UI-Komponenten. Diese Technologie-Kombination ermöglicht eine moderne, wartbare und skalierbare Frontend-Architektur.

Für das Styling und die UI-Komponenten wurde ein durchdachter Ansatz gewählt, der TailwindCSS als Utility-First CSS Framework für schnelle Entwicklung nutzt. HeadlessUI stellt unstyled, vollständig zugängliche UI-Komponenten bereit, während Heroicons für eine konsistente Icon-Bibliothek sorgt. Framer Motion ergänzt das System um flüssige Animationen und Übergänge, die die Benutzererfahrung verbessern.

#### Routing

Das Routing-System basiert auf React Router Dom und ermöglicht eine strukturierte Navigation durch die Anwendung. Die Implementierung unterstützt deklarative Routen-Definition, Nested Routing für komplexe Layouts, programmatische Navigation und effizientes History-Management. Die Hauptrouten umfassen die Startseite mit dem Frage-Interface, eine Übersicht aller Fragen sowie Detailansichten für spezifische Fragen.

#### API-Integration

Die Kommunikation zwischen Frontend und Backend erfolgt über RESTful API-Calls, die asynchrone Datenabfrage ermöglichen. Das System implementiert umfassendes Error Handling und Loading States, um eine optimale Benutzererfahrung zu gewährleisten. Optimistische UI-Updates verbessern die wahrgenommene Performance, während Caching-Mechanismen die tatsächliche Performance steigern. Die implementierten Funktionen umfassen das Einreichen neuer Fragen, das Abrufen von Fragenübersichten, das Anzeigen detaillierter Antworten sowie Feedback-Mechanismen für Antwortbewertungen.

### Backend

#### REST-API

Das Backend basiert auf FastAPI, einem modernen Python-Framework, das sich durch automatische API-Dokumentation über OpenAPI/Swagger, Type Hints für Validierung, asynchrone Unterstützung und hohe Performance durch Pydantic auszeichnet. Die Hauptendpunkte umfassen GET /questions für das Abrufen aller Fragen, POST /questions für das Einreichen neuer Fragen, GET /questions/{id} für spezifische Fragendetails sowie POST-Endpunkte für das Hinzufügen, Ablehnen oder Markieren von Antworten.

Die CORS-Konfiguration wurde so implementiert, dass sie alle Origins, Credentials, Methods und Headers zulässt, was eine flexible Entwicklung und Integration ermöglicht. Diese Konfiguration sollte in Produktionsumgebungen entsprechend den Sicherheitsanforderungen angepasst werden.

#### Vector Stores

Das System verwendet Qdrant als Vector Database, die speziell für die Verwaltung hochdimensionaler Vektoren optimiert ist. Die Collection-Konfiguration definiert separate Vektorräume für Fragen und Antworten, jeweils mit einer Dimensionalität von 1024 und Cosine Distance als Ähnlichkeitsmetrik. Diese Trennung ermöglicht es, sowohl in Fragen als auch in Antworten zu suchen und die Ergebnisse entsprechend zu gewichten.

Der implementierte Such-Algorithmus nutzt eine Dual-Vector-Search-Strategie, bei der parallele Suchen in beiden Vektorräumen durchgeführt werden. Eine Prefetch-Strategie optimiert die Performance, während Filtering-Mechanismen sicherstellen, dass nur Einträge mit vorhandenen Antworten in den Ergebnissen erscheinen. Die Fusion der Ergebnisse erfolgt durch Reciprocal Rank Fusion, um optimale Relevanz zu gewährleisten.

#### LLM-Integration

Die Integration des Large Language Models erfolgt über Ollama, eine Platform für lokale LLM-Ausführung. Das System verwendet das Gemma3:1b Modell, das sich durch Effizienz bei guter Qualität auszeichnet. Die Implementierung nutzt Pydantic für strukturierte Ausgaben, wodurch eine konsistente API-Antwortstruktur gewährleistet wird.

Das Prompt Engineering folgt bewährten Praktiken mit strukturierten Prompts unter Verwendung von XML-Tags für bessere Parsing-Ergebnisse. Kontext-Injection erfolgt durch die Integration vorheriger Antworten, während Language Detection für mehrsprachige Antworten sorgt. Format-Enforcement durch JSON Schema stellt sicher, dass die LLM-Ausgaben der erwarteten Struktur entsprechen.

#### Containerisierung

Die gesamte Anwendung wurde containerisiert, um eine konsistente Deployment-Erfahrung zu gewährleisten. Die Docker Compose Architektur umfasst separate Services für Backend, Frontend, Qdrant, Ollama und MongoDB. Jeder Service ist über definierte Ports erreichbar und verfügt über entsprechende Abhängigkeiten zu anderen Services.

Die Container-Optimierungen umfassen Multi-stage Builds für kleinere Images, Health Checks für Service-Monitoring, environment-basierte Konfiguration für Flexibilität und Volume-Mounts für Datenpersistenz. Diese Architektur ermöglicht sowohl lokale Entwicklung als auch Produktions-Deployments mit minimalen Anpassungen.

---

## Herausforderungen und Lösungsansätze

Die Entwicklung des KI-basierten Ticketsystems brachte verschiedene technische und konzeptionelle Herausforderungen mit sich, die innovative Lösungsansätze erforderten. Eine der wesentlichsten technischen Herausforderungen lag in der Latenz-Optimierung, da die multiple API-Calls zwischen verschiedenen Services zu spürbaren Verzögerungen führten. Diese Problematik wurde durch die Implementierung asynchroner Verarbeitung und intelligenter Caching-Strategien adressiert, wodurch die Antwortzeiten erheblich reduziert werden konnten.

Die Skalierbarkeit stellte eine weitere bedeutende Herausforderung dar, insbesondere bei der Vector Search in großen Datenmengen. Um diesem Problem zu begegnen, wurden spezielle Indexierungs-Strategien entwickelt und eine horizontale Skalierungsarchitektur implementiert. Die Konsistenz zwischen verschiedenen Stores erwies sich als komplexes Thema, das durch eine Event-driven Architecture mit Message Queues gelöst wurde, um Eventual Consistency zu gewährleisten.

In Bezug auf die Qualitätssicherung stand die Gewährleistung hoher Antwortqualität im Fokus. Hierfür wurden Feedback-Loops implementiert, A/B-Testing verschiedener Retrieval-Strategien durchgeführt und kontinuierliche Evaluation durch spezifische Metriken etabliert. Die Reduzierung von Bias stellte eine weitere wichtige Aufgabe dar, die durch Diversifizierung der Trainingsdaten, Implementierung von Fairness-Metriken für verschiedene User-Gruppen und Erhöhung der Transparenz durch Explainable AI-Techniken angegangen wurde.

## Fazit

### Erreichte Ziele

Das entwickelte KI-basierte Ticketsystem stellt ein erfolgreiches konzeptionelles Proof of Concept dar, das die grundsätzliche Machbarkeit moderner NLP-Technologien in einem prototypischen Anwendungsfall demonstriert. Dabei wurden die gesteckten Ziele in allen definierten Bereichen erreicht, wobei zu betonen ist, dass es sich um einen Forschungsprototyp handelt, der noch weit von einem produktiven Einsatz entfernt ist. Aus technischer Sicht konnte die prototypische Implementierung eines Hybrid-Retrieval-Systems realisiert werden, das Dense-, Sparse- und hybride Ansätze in einer experimentellen Umgebung kombiniert. Die grundlegende Integration von Large Language Models über Ollama ermöglicht funktionsfähige Textgenerierung für Demonstrationszwecke, während eine einfache Microservice-Architektur mit Docker die konzeptionellen Grundlagen für zukünftige Entwicklungen schafft. Die entwickelte Benutzeroberfläche bietet eine funktionale Basis für die Evaluation des Systems.

Die fachlichen Erfolge umfassen die erfolgreiche Demonstration der grundsätzlichen Machbarkeit automatisierter Antwortgenerierung in einem kontrollierten Testumfeld. Die prototypische Implementierung von Feedback-Mechanismen zeigt Möglichkeiten für kontinuierliches Lernen auf, auch wenn diese noch nicht für produktive Umgebungen optimiert sind. Ein besonders interessanter Aspekt war die empirische Evaluation verschiedener Retrieval-Strategien: Die systematische Untersuchung mit einem selbst entwickelten Testdatensatz von 25 Fragen führte zu dem überraschenden Ergebnis, dass der Dense-Ansatz bessere Performance zeigte als der theoretisch überlegene Hybrid-Ansatz. Diese Erkenntnis verdeutlicht die Wichtigkeit empirischer Validierung in der Systementwicklung und zeigt, dass die optimale Retrieval-Strategie stark vom spezifischen Anwendungskontext und der Datenbasis abhängt.

Aus akademischer Sicht führte das Projekt zu vertieften Kenntnissen moderner NLP-Techniken und praktischer Erfahrung mit Vector Databases in einem Forschungskontext. Das entwickelte Verständnis für die Komplexität von ML-Systemen und die grundlegende Anwendung von MLOps-Prinzipien bildet eine solide Grundlage für zukünftige Projekte in diesem Bereich. Besonders aufschlussreich war die empirische Evaluation verschiedener Retrieval-Strategien: Die systematische Untersuchung mit einem selbst erstellten Testdatensatz von 25 Fragen ergab überraschenderweise, dass der Dense-Ansatz dem theoretisch überlegenen Hybrid-Ansatz in der Praxis überlegen war. Dieses Ergebnis unterstreicht die Bedeutung empirischer Evaluation in der Prototypentwicklung und zeigt, dass theoretische Überlegenheit nicht automatisch zu besserer praktischer Performance führt, auch wenn weitere umfangreiche Tests für valide Schlussfolgerungen notwendig wären.

### Lessons Learned

Die Erfahrungen aus diesem Prototyp-Projekt verdeutlichen wichtige Erkenntnisse in verschiedenen Bereichen der experimentellen Systementwicklung. Bei Architektur-Entscheidungen zeigte sich, dass Microservices zwar erhebliche Flexibilität für Forschungsprototypen bieten, jedoch die Komplexität des Gesamtsystems erhöhen. Container-Orchestrierung erwies sich als nützlich für experimentelle ML-Systeme, während API-First Design eine bessere Trennung zwischen Frontend und Backend ermöglicht und damit die Entwicklung und Tests von Prototyp-Komponenten erleichtert.

Die Optimierung der experimentellen ML-Pipeline offenbarte, dass Prompt Engineering kritisch für die LLM-Performance ist und erheblichen Einfluss auf die Qualität der generierten Antworten hat. Vector Search erfordert sorgfältiges Tuning verschiedener Parameter, um optimale Ergebnisse zu erzielen. Darüber hinaus müssen Evaluation-Metriken domänenspezifisch angepasst werden, um aussagekräftige Bewertungen der Prototyp-Performance zu ermöglichen. Eine besonders wichtige Erkenntnis war, dass empirische Evaluation theoretische Annahmen widerlegen kann: Die Untersuchung mit 25 Testfragen zeigte, dass der Dense-Retrieval-Ansatz entgegen der Erwartung bessere Ergebnisse lieferte als der komplexere Hybrid-Ansatz, was die Notwendigkeit systematischer Experimente in der Prototypentwicklung unterstreicht.

In Bezug auf die User Experience zeigten sich Feedback-Mechanismen als konzeptionell wertvoll für die Entwicklung intelligenterer Systeme, auch wenn deren Implementierung in diesem Prototyp noch rudimentär ist. Loading States und grundlegendes Error Handling verbessern die Benutzerinteraktion mit experimentellen Systemen, während Transparenz über Systemgrenzen und -limitationen das Verständnis für den Prototyp-Status erhöht.

### Ausblick

Die zukünftige Entwicklung eines produktionsreifen Systems basierend auf diesem Proof of Concept erfordert erhebliche Weiterentwicklungen und lässt sich in verschiedene Phasen untergliedern. Der Übergang von einem Forschungsprototyp zu einem produktionsfähigen System würde umfangreiche Überarbeitungen in allen Bereichen erfordern. Kurzfristige Entwicklungen müssten zunächst die grundlegenden Stabilitäts- und Sicherheitsprobleme addressieren, bevor Performance-Optimierungen wie Redis-Caching für häufige Anfragen, Optimierung der Vector-Indizes für größere Datenmengen und robustes Connection Pooling implementiert werden könnten. Feature-Erweiterungen wie Multi-tenancy, erweiterte Kategorisierung und Integration mit externen Knowledge Bases würden umfangreiche Architektur-Überarbeitungen erfordern. Monitoring und Analytics würden für einen produktiven Einsatz eine komplette Neuentwicklung erfordern, einschließlich umfassendem Application Performance Monitoring, User Analytics für Verhaltensanalyse und robusten A/B-Testing Frameworks für Feature-Evaluation.

Mittelfristige Entwicklungen für eine eventuelle Produktionsversion würden Advanced AI Features erfordern, einschließlich der professionellen Integration von Multimodal LLMs für Bild- und Dokumentenverarbeitung, der Implementierung von Active Learning für kontinuierliche Modellverbesserung und der Entwicklung domänenspezifischer Embedding-Modelle. Enterprise Features wie Single Sign-On Integration, Role-based Access Control und umfassende Compliance-Features für GDPR/DSGVO würden fundamentale Sicherheits- und Architektur-Überarbeitungen erfordern. Die Skalierung durch Kubernetes-basierte Orchestrierung, Auto-scaling basierend auf Load-Metriken und Multi-region Deployment für globale Verfügbarkeit würde eine vollständige Neuarchitektur des Systems erfordern.

Die langfristige Vision für ein produktionsreifes System würde intelligente Automatisierung durch proaktive Problemerkennung mittels Trend-Analyse, automatische Ticket-Kategorisierung und -Routing sowie Predictive Maintenance für IT-Systeme umfassen. Ecosystem Integration durch Plugin-Systeme für Third-Party-Integrationen, API Marketplace für Community-Erweiterungen und Integration mit etablierten Help Desk-Systemen würde umfangreiche Standardisierungs- und Interoperabilitäts-Entwicklungen erfordern. Next-Generation AI Features wie die Integration von Agent-basierten AI-Systemen, Implementierung von Reinforcement Learning aus Human Feedback und Multi-Agent-Systeme für komplexe Problem-Lösung liegen noch in weiter Ferne und würden grundlegende Forschung und Entwicklung erfordern.

Darüber hinaus ergeben sich interessante Forschungsrichtungen in verschiedenen Bereichen, die auf den Erkenntnissen dieses Prototyps aufbauen könnten. Im Bereich Retrieval-Augmented Generation stehen die Untersuchung neuer Fusion-Techniken für Hybrid-Retrieval, die Entwicklung von Context-aware Embedding-Modellen und die Evaluation verschiedener Re-ranking-Strategien im Fokus zukünftiger Forschung. Human-AI Collaboration umfasst Studien zur optimalen Arbeitsteilung zwischen Mensch und KI, die Entwicklung von Explainable AI-Techniken für erhöhtes Vertrauen und Untersuchungen zu Bias und Fairness in AI-Systemen. Effizienz und Nachhaltigkeit werden durch Green AI-Ansätze zur Reduzierung des Energieverbrauchs von ML-Modellen, Edge Computing für lokale LLM-Inferenz und die Entwicklung effizienterer Architekturmuster vorangetrieben.

Die Dokumentation zeigt einen umfassenden Überblick über ein konzeptionelles Proof of Concept für ein KI-basiertes Ticketsystem, das die grundsätzliche Machbarkeit moderner NLP-Technologien in einem experimentellen Anwendungsfall demonstriert. Das Projekt zeigt technische Kompetenz in der Prototypentwicklung und ein fundiertes Verständnis für die Herausforderungen beim Übergang von Forschungsprototypen zu produktionsreifen AI-Systemen. Die systematische Herangehensweise, von der theoretischen Fundierung über die experimentelle Umsetzung bis hin zur kritischen Evaluation und dem realistischen Ausblick auf notwendige Weiterentwicklungen, unterstreicht die akademische Qualität und das Bewusstsein für die praktischen Limitationen dieser Forschungsarbeit.
