# Capstone Projekt für den Kurs *Certified Data Scientist*
Mein Abschlussprojekt für den Kurs *Certified Data Scientist* der XDI Experience Design Institut GmbH, den ich von Mai bis November 2023 absolviert habe. 

## Aufgabenstellung
Dieses Projekt soll untersuchen, welche Erkenntnisse die Drogeriekette Rossmann aus ihren historischen Verkaufs- und Werbedaten, Daten zu Schulferien und Feiertagen sowie Wettbewerberdaten gewinnen kann. Das Projekt soll die Frage adressieren, wie sich diese Daten nutzen lassen, um den Betrieb und das Management der Filialen zu optimieren, mit dem Ziel, mehr Umsatz zu generieren. Darüber hinaus soll ermittelt werden, wie sich diese Datensätze einsetzen lassen, um die wöchentlichen Verkäufe (Umsatzerlöse) für jede Filiale mit einem ausreichenden Genauigkeitsniveau vorherzusagen.
### Hintergrund
Rossmann betreibt über 4.300 Drogeriemärkte in 9 europäischen Ländern (vgl. https://de.wikipedia.org/wiki/Rossmann_(Handelskette)). Derzeit sind Rossmann-Filialleiter damit beauftragt, ihre wöchentlichen Verkaufsprognosen bis zu acht Wochen im Voraus zu erstellen. Die Verkaufsergebnisse der Filialen werden von vielen Faktoren beeinflusst, einschließlich Werbeaktionen, Wettbewerbsintensität, Schulferien und staatlichen Feiertagen, saisonalen Veränderungen und Standortbedingungen. Da Tausende von einzelnen Filialleitern Verkaufsprognosen auf der Grundlage ihrer individuellen Umstände erstellen, kann die Genauigkeit der Ergebnisse sehr unterschiedlich sein. Daher ist das Data Science Team des Unternehmens auf einer neuen Mission, eine vereinheitlichte Modellierungsmethode für Filialleiter zu erstellen, um die wöchentlichen Ergebnisse mit höherer Genauigkeit vorherzusagen. Das Management Team benötigt zudem auch einen Gesamtbericht mit machbaren bzw. umsetzbaren Strategien, um die allgemeine Leistung (Performance) aller Filialen zu verstehen und eine Möglichkeit zur Optimierung zukünftiger Verkaufsleistungen (d. h. der Umsatzerlöse) zu finden. Zuletzt muss jedem Filialleiter ein individueller Bericht zur Leistung der jeweiligen Filiale zur Verfügung gestellt werden.
### Datenquelle

Die in diesem Projekt verwendeten Daten stammen von https://www.kaggle.com/c/rossmann-store-sales/data und bestehen aus zwei Datensätzen: train.csv und store.csv. 

* Der Datensatz train.csv enthält 1.017.209 Datenpunkte und besteht aus insgesamt 9 Variablen, die von 1115 Rossmann Filialen über 942 Tage vom 01.01.2013 bis zum 31.07.2015 gesammelt wurden. Der Datensatz enthält 7 numerische Variablen und 2 kategoriale Variablen.

* Der Datensatz store.csv enthält 1115 Datenpunkte und besteht aus insgesamt 10 Variablen, die von 1115 Rossmann Filialen gesammelt wurden. Der Datensatz enthält 6 numerische Variablen und 3 kategoriale Variablen. 

### Konkrete Aufgabenstellung
* Bestimme die Schlüsselfaktoren, die die Verkaufs- bzw. Umsatzerlöse beeinflussen und stelle geeignete Strategien für das Management-Team für die zukünftige Geschäftsplanung bereit.
* Baue ein vereinheitlichtes Prognosemodell auf (z.B. mit Hilfe einer einfachen Zeitreihenmodellierung) für jede Filiale auf der Grundlage der historischen Verkaufsdaten oder mit zusätzlichen Schlüsselvariablen, falls erforderlich, um sicherzustellen, dass das Modell besser abschneidet als die durchschnittliche Methode (Mittelwertmethode - Prognose mit dem Durchschnittswert der historischen Daten).
* Generiere Berichte mit Informationen zur Gesamtleistung der 1115 Filialen sowie individueller Leistungsberichte für jede Filiale.

### Hinweise zu Einschränkungen & Umfang des Projekts
* Aufbau eines vereinheitlichten Prognosemodells für alle 1115 Filialen: Einige der Filialen waren aufgrund von Renovierungsarbeiten für einige Monate oder mehr als ein halbes Jahr geschlossen und erzielten in diesem Zeitraum keine wöchentlichen Verkäufe (Umsatzerlöse = 0). Das Vorhandensein von Nullwerten in den Beobachtungen erschwert die Erstellung von Zeitreihenmodellen mit hoher Genauigkeit.
* Es können zufällige Spitzenwerte in den täglichen Verkäufen und der Kundenanzahl in einigen Filialen beobachtet werden, unabhängig davon, ob eine Promotion bzw. Werbeaktion durchgeführt wurde oder nicht, und ob es sich um einen Schulferien- oder Feiertag handelte oder nicht. Die verfügbaren Informationen in den beiden aktuellen Datensätzen sind sehr begrenzt, um diese Spitzenwerte zu verstehen, und es könnte herausfordernd sein, die Ursachen für deren Auftreten zu entschlüsseln.
* Identifizierung der Schlüsselfaktoren (für den Umsatz) als zusätzliche/exogene Variablen, die in das Zeitreihenmodell einfließen: Wenn wir train.csv und store.csv zusammenführen, ergeben sich 18 Variablen. Es kann zeitaufwendig sein, herauszufiltern, welche Variablen bei der Vorhersage des Umsatzes von Bedeutung sind.

### Einige Hilfestellungen zur Projektdurchführung

Es müssen unterschiedliche Schritte unternommen werden, um ein Vorhersagemodell im Rahmen dieses Projekts zu erstellen und die Ergebnisse zu analysieren bzw. zu interpretieren.

1. Die Dateien train.csv und store.csv können mit Hilfe von Python bzw. Pandas importiert und bereinigt werden. Falsch dargestellte Datentypen müssen auf den richtigen Typ korrigiert werden. Die fehlenden Werte in store.csv können zum Beispiel mit optimalen Imputations-Techniken (vgl. z.B. https://de.wikipedia.org/wiki/Imputation_(Statistik)) behandelt werden, basierend auf der empirischen Verteilung jeder Variable und ihrer Korrelation mit anderen Variablen.
2. Die täglichen Verkäufe (Umsatzerlöse) in train.csv müssen zu wöchentlichen Verkäufen für jede Filiale aggregiert werden, um sie weiter zu modellieren (d. h., ein Prognosemodell auf wöchentlicher Basis zu entwickeln).
3. Im Abschnitt der explorativen Datenanalyse (EDA) müssen zunächst die Daten zu den täglichen Verkäufen, Kundenanzahlen, Öffnungstagen, Promotionen/ Werbeaktionen und Feiertagen von 1115 Geschäften auf Basis der Gesamtsumme der 942 Tage aggregiert werden. Neue Metriken wie der durchschnittliche tägliche Verkaufserlös, die durchschnittliche tägliche Kundenanzahl und die Verkäufe pro Kunde müssen erstellt werden, um die Performance einer Filiale fair zu analysieren, da einige Filialen aufgrund von Renovierungen für einen bestimmten Zeitraum geschlossen waren und die Gesamtzahl der Öffnungstage zwischen den Filialen variiert.
4. Nach Abschluss von Schritt 3 kann der Datensatz mit store.csv kombiniert werden und die EDA auf Basis dieses kombinierten Datensatzes durchgeführt werden. Nach der EDA wird ein Gesamtbericht zur Leistung/ Performance aller Rossmann Filialen für das Management Team erstellt.
5. Für den individuellen Filial-Bericht sollst du Codes bereitstellen, die die Erstellung von Berichten ermöglichen, indem nur eine Store- bzw. Filial-ID eingegeben wird.
6. Für den Modellierungsteil (d. h. die Prognose der wöchentlichen Umsatzzahlen auf Filialebene) werden die in Schritt 2 vorbereiteten wöchentlich aggregierten Verkaufsdaten als Beobachtungen verwendet, aufgeteilt in Trainings- und Testsets. Stelle bitte sicher, dass das Testset 8 wöchentliche Umsatzdaten enthält. Deine ML-Prognosemodelle sollen mit der Durchschnittsmethode* verglichen werden und das Modell mit der besten Leistung wird als endgültiges Prognosemodell ausgewählt. Überlege dir, wie du die Leistung eines Prognosemodells in diesem Anwendungsfall am besten quantifizieren kannst. Die Prognoseergebnisse für die nächsten acht Wochen sollen bereitgestellt werden. Im Idealfall stellst du auch Codes bereit, um den gesamten Prozess für Filialmanager zu vereinfachen, indem sie für die Generierung der Prognosen nur eine Store-ID eingeben müssen.



### Liefer- und Abgabeobjekte (Deliverables) 

Die Endfassung des Projekts wird in Form einer Präsentation und eines formellen Projektberichts zur Analyse der Gesamtperformance der Filialen präsentiert. Es werden Jupyter-Notebooks für die Gesamtanalyse aller Filialen, die Berichterstellung für einzelne Filialen und das Modellieren (Umsatzprognosen) für einzelne Filialen bereitgestellt, die jeden Schritt und den für die Analyse und Modellierung des Projekts geschriebenen Code detailliert beschreiben. 

**+++++[Ende der Aufgabenstellung]+++++**

## Dateien
### project_report.ipynb
* Gibt einen (ersten) Überblick über die Daten und erklärt wie ich im Projekt vorgegangen bin.

### rossmann_company_analysis.ipynb
* Untersucht die Auswirkungen verschiedener Faktoren auf die Entwicklung von Umsatz- und Kundenzahlen auf Unternehmensebene.

### rossman_store_analysis.ipynb
* Leistungsbericht für eine einzelne Filiale
* Filial-ID eingeben und alle Zellen ausführen.

### rossman_sales_weekly_prediction_vscode.ipynb
* Umsatzvorhersage (acht Wochen) für eine einzelne Filiale
* testet verschiedene ML Algorithmen und wählt den besten für diese Filale aus
* Filial-ID eingeben und alle Zellen ausführen.

### pms.py
* Hilffunktionen um Dinge zu plotten

### rms.py
* Hilfsfunktionen um Daten einzulesen und vorzubereiten

Die folgenden Dateien stammen von https://www.kaggle.com/c/rossmann-store-sales/data:

### store.csv
* filialspezifische Informationen
* assortment, store type, competition, Promo2
  
### train.csv
* Umsatz- und Kundenzahlen für 1115 Filialen an 942 Tagen
* holidays, school holidays
