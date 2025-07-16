import os

from fastembed import LateInteractionTextEmbedding, SparseTextEmbedding, TextEmbedding
from qdrant_client import QdrantClient, models

from pprint import pprint

HOST = os.getenv("QDRANT_HOST", "localhost")
PORT = int(os.getenv("QDRANT_PORT", 6333))

COLLECTION_NAME = "full_hybrid"

client = QdrantClient(host=HOST, port=PORT)

dense_embedding_model = TextEmbedding("mixedbread-ai/mxbai-embed-large-v1")
bm25_embedding_model = SparseTextEmbedding("Qdrant/bm25")
late_interaction_embedding_model = LateInteractionTextEmbedding(
    "colbert-ir/colbertv2.0"
)

if not client.collection_exists(COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={
            "questions": models.VectorParams(
                size=1024,
                distance=models.Distance.COSINE,
            ),
            "answers": models.VectorParams(
                size=1024,
                distance=models.Distance.COSINE,
            ),
            "colbert": models.VectorParams(  # Matryoshka ColBERTv2
                size=128,
                distance=models.Distance.COSINE,
                multivector_config=models.MultiVectorConfig(
                    comparator=models.MultiVectorComparator.MAX_SIM,
                ),
            ),
        },
        sparse_vectors_config={
            "bm25": models.SparseVectorParams(
                modifier=models.Modifier.IDF,
            )
        },
    )


def search(query: str, threshold: float = 0.6):
    question_query_vector = next(dense_embedding_model.embed(query)).tolist()
    answer_query_vector = next(dense_embedding_model.query_embed(query)).tolist()
    sparse_query_vector = next(
        bm25_embedding_model.embed(query)
    )
    late_query_vector = next(
        late_interaction_embedding_model.embed(query)
    ).tolist() 

    prefetches = [
        models.Prefetch(
            query=question_query_vector,
            using="questions",
            limit=10,
        ),
        models.Prefetch(
            query=answer_query_vector,
            using="answers",
            limit=10,
        ),
        models.Prefetch(
            query=models.SparseVector(**sparse_query_vector.as_object()),
            using="bm25",
            limit=10,
        ),
    ]

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        prefetch=prefetches,
        query=late_query_vector,
        limit=10,
        with_payload=False,
        using="colbert",
        # score_threshold=threshold
    )

    return results


def add_question_answer(question: str, answer: str, id: int):
    question_vector = next(dense_embedding_model.embed(question)).tolist()
    answer_vector = next(dense_embedding_model.embed(answer)).tolist()
    sparse_vector = next(bm25_embedding_model.embed(question)).as_object()
    late_vector = next(late_interaction_embedding_model.embed(question)).tolist()

    client.upload_points(
        COLLECTION_NAME,
        points=[
            models.PointStruct(
                id=id,
                vector={
                    "questions": question_vector,
                    "answers": answer_vector,
                    "bm25": sparse_vector,
                    "colbert": late_vector,
                },
                payload={"frage": question, "antwort": answer},
            )
        ],
    )


if __name__ == "__main__":
    test_data = [
        {
            "id": 1,
            "frage": "Ich kann mich mit meinem iPhone nicht mit dem WLAN verbinden, was muss ich machen?",
            "antwort": "Wenn Ihr iPhone keine WLAN-Verbindung herstellen kann, beginnen Sie damit, die WLAN-Funktion am iPhone aus- und wieder einzuschalten. Überprüfen Sie anschließend, ob das richtige Netzwerk ausgewählt ist und das korrekte Passwort eingegeben wurde (achten Sie auf Groß- und Kleinschreibung). Starten Sie gegebenenfalls den Router neu. Falls eine Fehlermeldung bezüglich eines Zertifikats erscheint, navigieren Sie zu den 'Einstellungen' > 'WLAN', tippen Sie auf das 'i' neben dem betroffenen Netzwerk und scrollen Sie nach unten, um die Option 'Vertrauen' oder 'Zertifikat vertrauen' zu finden und zu aktivieren. Manchmal hilft es auch, das Netzwerk zu 'ignorieren' und sich neu zu verbinden.",
        },
        {
            "id": 2,
            "frage": "Mein Computer ist sehr langsam geworden. Was kann ich tun, um ihn zu beschleunigen?",
            "antwort": "Ein langsamer Computer kann verschiedene Ursachen haben. Beginnen Sie mit einem Neustart. Überprüfen Sie im Task-Manager (Windows: Strg+Umschalt+Esc) oder Aktivitätsmonitor (macOS: Befehl+Leertaste, 'Aktivitätsmonitor' eingeben), welche Programme viele Ressourcen (CPU, RAM, Festplatte) verbrauchen und schließen Sie nicht benötigte Anwendungen. Deinstallieren Sie Programme, die Sie nicht mehr benötigen. Führen Sie eine Datenträgerbereinigung durch, um temporäre Dateien zu entfernen. Überprüfen Sie, ob Ihre Festplatte fast voll ist und schaffen Sie Speicherplatz. Ein Virenscan kann auch helfen, schädliche Software auszuschließen. Zuletzt sollten Sie prüfen, ob ausreichen RAM vorhanden ist, gegebenenfalls wäre ein Upgrade sinnvoll.",
        },
        {
            "id": 3,
            "frage": "Ich habe versehentlich eine wichtige Datei gelöscht. Kann ich sie wiederherstellen?",
            "antwort": "Wenn Sie eine Datei versehentlich gelöscht haben, prüfen Sie zuerst den Papierkorb (Windows) oder den 'Mülleimer' (macOS). Falls die Datei dort nicht ist oder der Papierkorb bereits geleert wurde, ist die Wiederherstellung schwieriger. Hören Sie sofort auf, den Speicherplatz zu nutzen, auf dem die Datei gespeichert war, um ein Überschreiben zu verhindern. Sie können versuchen, Wiederherstellungssoftware wie Recuva (für Windows) oder EaseUS Data Recovery Wizard zu verwenden. Die Erfolgschancen hängen davon ab, wie schnell Sie reagieren und ob der Speicherbereich bereits überschrieben wurde. Im schlimmsten Fall kann ein professioneller Datenrettungsdienst helfen.",
        },
        {
            "id": 4,
            "frage": "Mein Drucker druckt nicht. Was sind die ersten Schritte zur Fehlerbehebung?",
            "antwort": "Überprüfen Sie zunächst, ob der Drucker eingeschaltet und ordnungsgemäß mit dem Computer (USB-Kabel) oder Netzwerk (WLAN/LAN-Kabel) verbunden ist. Stellen Sie sicher, dass genügend Papier eingelegt und keine Papierstaus vorhanden sind. Prüfen Sie den Füllstand der Tintenpatronen oder des Toners. Sehen Sie in der Druckerwarteschlange nach, ob Aufträge feststecken, und versuchen Sie, diese zu löschen. Starten Sie sowohl den Drucker als auch den Computer neu. Installieren Sie zuletzt die Druckertreiber neu oder aktualisieren Sie diese.",
        },
        {
            "id": 5,
            "frage": "Mein Internet funktioniert nicht. Wie gehe ich bei der Fehlersuche vor?",
            "antwort": "Beginnen Sie damit, Ihren **Router und Ihr Modem** für etwa 30 Sekunden vom Strom zu trennen und dann wieder anzuschließen. Warten Sie einige Minuten, bis alle Lichter wieder stabil leuchten. Überprüfen Sie, ob alle Kabel fest sitzen (WAN, LAN, Strom). Testen Sie, ob das Problem nur bei einem Gerät auftritt oder bei allen Geräten im Haushalt. Wenn es nur ein Gerät betrifft, liegt das Problem möglicherweise dort (WLAN aus/einschalten, Geräteneustart). Wenn das Internet weiterhin nicht funktioniert, kontaktieren Sie Ihren Internetanbieter, da die Störung an deren Leitung liegen könnte.",
        },
        {
            "id": 6,
            "frage": "Ich habe ein Pop-up gesehen, das besagt, mein Computer sei infiziert und ich soll eine Nummer anrufen. Was soll ich tun?",
            "antwort": "Ignorieren Sie solche Pop-ups **unbedingt** und rufen Sie keinesfalls die angegebene Nummer an! Dies ist eine gängige Taktik von Betrügern (Scareware oder Tech-Support-Betrug), die versuchen, Sie unter Druck zu setzen, um Geld für unnötige Dienstleistungen zu verlangen oder Malware zu installieren. Schließen Sie den Browser, notfalls über den Task-Manager (Strg+Umschalt+Esc in Windows). Führen Sie danach einen vollständigen Scan mit Ihrem aktuellen Antivirenprogramm durch. Wenn Sie unsicher sind, trennen Sie den Computer vom Internet und lassen Sie ihn von einem Fachmann überprüfen.",
        },
        {
            "id": 7,
            "frage": "Wie erstelle ich ein sicheres Passwort, das ich mir auch merken kann?",
            "antwort": "Ein sicheres Passwort sollte lang sein (mindestens 12-16 Zeichen), eine Mischung aus Groß- und Kleinbuchstaben, Zahlen und Sonderzeichen enthalten und keine leicht zu erratenden persönlichen Informationen. Eine gute Methode ist die 'Passphrase'-Methode: Denken Sie sich einen Satz aus, der für Sie leicht zu merken ist, und verwenden Sie die Anfangsbuchstaben jedes Wortes, fügen Sie Zahlen und Sonderzeichen ein. Beispiel: 'Mein Hund Bello isst am liebsten 7 Knochen!' könnte zu 'MhBiAl7K!' werden. Verwenden Sie außerdem für jeden Dienst ein einzigartiges Passwort und nutzen Sie einen Passwort-Manager.",
        },
        {
            "id": 8,
            "frage": "Mein Laptop-Akku hält nicht mehr lange. Was kann ich tun, um die Lebensdauer zu verlängern?",
            "antwort": "Die Akkulebensdauer kann durch verschiedene Maßnahmen verbessert werden. Reduzieren Sie die Bildschirmhelligkeit, da dies ein großer Stromverbraucher ist. Deaktivieren Sie WLAN und Bluetooth, wenn Sie sie nicht benötigen. Schließen Sie nicht verwendete Anwendungen im Hintergrund. Überprüfen Sie die Energieeinstellungen Ihres Betriebssystems und wählen Sie einen energiesparenden Modus. Versuchen Sie, den Akku zwischen 20% und 80% Ladung zu halten und vermeiden Sie es, ihn dauerhaft bei 100% am Stromnetz zu lassen. Extreme Temperaturen (Hitze und Kälte) schaden dem Akku ebenfalls.",
        },
        {
            "id": 9,
            "frage": "Ich habe eine E-Mail erhalten, die verdächtig aussieht. Worauf muss ich achten, um Phishing zu erkennen?",
            "antwort": "Seien Sie misstrauisch bei E-Mails, die unerwartet kommen und dringenden Handlungsbedarf vortäuschen. Achten Sie auf **Rechtschreib- und Grammatikfehler**. Überprüfen Sie den Absender: Stimmt die E-Mail-Adresse wirklich mit der angeblichen Organisation überein? Fahren Sie mit der Maus über Links (aber klicken Sie nicht!), um die tatsächliche Ziel-URL zu sehen – oft weicht sie vom angezeigten Text ab. Seriöse Unternehmen fragen niemals per E-Mail nach Passwörtern oder sensiblen Daten. Wenn Sie unsicher sind, kontaktieren Sie das Unternehmen direkt über die offizielle Website oder Telefonnummer, nicht über die in der E-Mail angegebenen Kontaktdaten.",
        },
        {
            "id": 10,
            "frage": "Mein Computer startet nicht richtig, er bleibt beim Logo hängen. Was könnte das Problem sein?",
            "antwort": "Dieses Problem kann auf verschiedene Ursachen hindeuten. Versuchen Sie zunächst einen **Hard-Reset**: Trennen Sie alle externen Geräte (USB-Sticks, Drucker etc.), schalten Sie den Computer aus, ziehen Sie das Stromkabel und halten Sie den Einschaltknopf für 15-30 Sekunden gedrückt, dann wieder anschließen und versuchen zu starten. Es könnte ein Problem mit dem Betriebssystem, dem Bootloader oder der Festplatte sein. Versuchen Sie, in den abgesicherten Modus zu booten (oft F8 oder Shift+F8 beim Start, je nach System). Wenn das nicht funktioniert, müssen Sie möglicherweise von einem Wiederherstellungsmedium (USB-Stick oder DVD) booten, um Systemreparaturen durchzuführen oder eine Neuinstallation in Betracht zu ziehen.",
        },
        {
            "id": 11,
            "frage": "Was ist der Unterschied zwischen einem Festplattenlaufwerk (HDD) und einer Solid-State-Disk (SSD)?",
            "antwort": "Ein **HDD (Hard Disk Drive)** ist ein traditionelles Speichergerät, das Daten auf rotierenden Magnetscheiben speichert. Es ist günstiger und bietet mehr Speicherplatz pro Euro, aber es ist langsamer, lauter und anfälliger für physische Beschädigungen. Eine **SSD (Solid State Disk)** hingegen speichert Daten auf Flash-Speicherchips, ähnlich einem USB-Stick. SSDs sind erheblich schneller (sowohl beim Starten des Systems als auch beim Laden von Anwendungen), leiser, energieeffizienter und robuster, da sie keine beweglichen Teile haben. Allerdings sind sie pro Gigabyte teurer als HDDs.",
        },
        {
            "id": 12,
            "frage": "Mein Bildschirm zeigt kein Bild, obwohl der Computer eingeschaltet ist. Was kann ich überprüfen?",
            "antwort": "Stellen Sie sicher, dass der Monitor eingeschaltet ist und das richtige Eingangssignal (HDMI, DisplayPort, DVI, VGA) ausgewählt ist. Überprüfen Sie, ob das Videokabel sowohl am Monitor als auch am Computer fest angeschlossen ist. Versuchen Sie, den Computer und den Monitor neu zu starten. Falls Ihr Computer eine separate Grafikkarte und Onboard-Grafik hat, stellen Sie sicher, dass das Kabel an der richtigen Buchse angeschlossen ist (oft an der Grafikkarte). Testen Sie den Monitor gegebenenfalls mit einem anderen Gerät oder ein anderes Kabel, um die Fehlerquelle einzugrenzen.",
        },
        {
            "id": 13,
            "frage": "Wie führe ich ein Backup meiner wichtigen Daten durch?",
            "antwort": "Regelmäßige Backups sind entscheidend. Die einfachste Methode ist, Ihre wichtigen Dateien manuell auf eine **externe Festplatte** oder einen **USB-Stick** zu kopieren. Für automatisierte Backups können Sie die integrierten Funktionen Ihres Betriebssystems nutzen (z.B. 'Dateiversionsverlauf' in Windows oder 'Time Machine' in macOS). Eine weitere sichere Methode ist die Nutzung von **Cloud-Speicherdiensten** wie Google Drive, Dropbox oder OneDrive, die Ihre Daten automatisch synchronisieren und online speichern. Es wird empfohlen, die **3-2-1-Regel** zu befolgen: Drei Kopien Ihrer Daten, auf zwei verschiedenen Medientypen, davon eine Kopie extern (off-site).",
        },
        {
            "id": 14,
            "frage": "Was ist der Unterschied zwischen HTTP und HTTPS?",
            "antwort": "**HTTP (Hypertext Transfer Protocol)** ist das Protokoll zur Übertragung von Daten im World Wide Web. **HTTPS (Hypertext Transfer Protocol Secure)** ist die sichere Version von HTTP. Der Hauptunterschied besteht darin, dass HTTPS eine verschlüsselte Verbindung zwischen Ihrem Browser und dem Server herstellt, typischerweise über **SSL/TLS**. Dies schützt Ihre Daten (z.B. Passwörter, Kreditkarteninformationen) vor dem Abfangen durch Dritte. Sie erkennen HTTPS an dem 'https://' in der Adressleiste und einem Schlosssymbol in Ihrem Browser.",
        },
        {
            "id": 15,
            "frage": "Meine Tastatur oder Maus funktioniert nicht mehr. Was kann ich tun?",
            "antwort": "Überprüfen Sie zuerst die physische Verbindung: Ist das Kabel fest eingesteckt oder sind bei kabellosen Geräten die Batterien leer oder der USB-Empfänger (Dongle) korrekt angeschlossen? Versuchen Sie, das Gerät an einen anderen USB-Port anzuschließen. Starten Sie den Computer neu. Bei kabellosen Geräten prüfen Sie, ob sie eingeschaltet sind und die Verbindung (Pairing) zum Computer korrekt ist. Bei Bluetooth-Geräten überprüfen Sie die Bluetooth-Einstellungen des Computers. Manchmal hilft es auch, die Treiber für Tastatur oder Maus neu zu installieren oder zu aktualisieren.",
        },
        {
            "id": 16,
            "frage": "Was ist eine Firewall und wofür brauche ich sie?",
            "antwort": "Eine **Firewall** ist ein Netzwerksicherheitssystem, das den ein- und ausgehenden Netzwerkverkehr überwacht und steuert, basierend auf vordefinierten Sicherheitsregeln. Sie fungiert als Barriere zwischen einem vertrauenswürdigen internen Netzwerk und einem nicht vertrauenswürdigen externen Netzwerk (wie dem Internet). Sie schützt Ihren Computer oder Ihr Netzwerk vor unbefugtem Zugriff, bösartiger Software und Hackern, indem sie unerwünschten Datenverkehr blockiert. Sowohl Router als auch Betriebssysteme (Windows Firewall, macOS Firewall) haben oft integrierte Firewalls, die aktiviert sein sollten.",
        },
        {
            "id": 17,
            "frage": "Wie erkenne und vermeide ich Malware auf meinem Computer?",
            "antwort": "Malware (Malicious Software) umfasst Viren, Trojaner, Spyware, Ransomware usw. Anzeichen können eine plötzliche Verlangsamung des Systems, unerwartete Pop-ups, Änderungen der Startseite oder Browser-Einstellungen sein. Um Malware zu vermeiden: Verwenden Sie eine **zuverlässige Antivirensoftware** und halten Sie diese stets aktuell. Seien Sie extrem vorsichtig beim Öffnen von E-Mail-Anhängen oder Klicken auf Links von unbekannten Absendern. Laden Sie Software nur von vertrauenswürdigen Quellen herunter und halten Sie Ihr Betriebssystem und alle Anwendungen durch **regelmäßige Updates** auf dem neuesten Stand, um bekannte Sicherheitslücken zu schließen.",
        },
        {
            "id": 18,
            "frage": "Warum ist es wichtig, Software-Updates zu installieren?",
            "antwort": "Software-Updates, ob für Ihr Betriebssystem, Anwendungen oder Browser, sind aus mehreren Gründen wichtig: Erstens enthalten sie oft **Sicherheitsupdates**, die Schwachstellen schließen, die von Hackern ausgenutzt werden könnten. Zweitens bringen sie **Fehlerbehebungen** mit sich, die die Stabilität und Leistung der Software verbessern. Drittens können sie **neue Funktionen** oder Verbesserungen der Benutzerfreundlichkeit einführen. Das Ignorieren von Updates kann Ihren Computer anfällig für Angriffe machen und zu Stabilitätsproblemen führen.",
        },
        {
            "id": 19,
            "frage": "Mein E-Mail-Postfach ist voll. Wie kann ich Speicherplatz freigeben?",
            "antwort": "Wenn Ihr E-Mail-Postfach voll ist, kann das den Empfang neuer Nachrichten verhindern. Beginnen Sie damit, den Ordner 'Spam' oder 'Junk-E-Mail' zu leeren. Löschen Sie große Anhänge: Suchen Sie nach E-Mails mit großen Anhängen und löschen Sie diese (oder speichern Sie die Anhänge lokal, bevor Sie die E-Mail löschen). Löschen Sie alte und unnötige E-Mails aus dem Posteingang, gesendeten Objekten und anderen Ordnern. Denken Sie daran, auch den **Papierkorb** oder 'Gelöschte Objekte'-Ordner in Ihrem E-Mail-Programm oder Webmail-Interface zu leeren, da gelöschte E-Mails oft dort verbleiben und weiterhin Speicherplatz belegen.",
        },
        {
            "id": 20,
            "frage": "Was ist Cloud Computing und welche Vorteile hat es für mich?",
            "antwort": "**Cloud Computing** bedeutet, dass Computing-Dienste (wie Server, Speicher, Datenbanken, Netzwerke, Software, Analysen und Intelligenz) über das Internet ('die Cloud') bereitgestellt werden, anstatt dass Sie physische Hardware und Software besitzen und verwalten müssen. Für Sie als Nutzer bedeutet das **Zugriff auf Ihre Daten und Anwendungen von überall und jederzeit**, sofern Sie eine Internetverbindung haben. Vorteile sind **Kosteneinsparungen** (Sie zahlen nur für das, was Sie nutzen), **Skalierbarkeit** (Sie können Ressourcen flexibel anpassen), **Datensicherung** (Anbieter kümmern sich um Backups) und **automatische Updates**, sodass Sie sich nicht um die Wartung kümmern müssen. Beispiele sind Google Drive, Dropbox, Microsoft 365, Netflix oder Spotify.",
        },
    ]
    for item in test_data:
        add_question_answer(item["frage"], item["antwort"], item["id"])
    print("Testdaten hinzugefügt.")
    search_results = search("Wie kann ich das WLAN reparieren?")
    pprint(search_results)
