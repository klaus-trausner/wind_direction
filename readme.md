# Wetterstation mit Raspberry Pi Pico W

<!-- Optional: Füge hier ein Bild deines Projekts ein -->
<!-- ![Pico W Wetterstation](pfad/zum/bild.jpg) -->

## Projektbeschreibung

Diese kompakte Wetterstation basiert auf dem Raspberry Pi Pico W und erfasst Temperatur, Luftfeuchtigkeit sowie Windrichtung. Die gesammelten Daten werden sowohl auf einem lokalen OLED-Display visualisiert als auch über das MQTT-Protokoll zur weiteren Verarbeitung in einem Netzwerk bereitgestellt.

## Funktionen

- **Temperatur- und Luftfeuchtigkeitsmessung** mit DHT22 Sensor
- **Windrichtungsmessung** über Modbus RTU (Windrichtungsgeber)
- **OLED-Anzeige** (128x64 Pixel) für lokale Datenvisualisierung
- **MQTT-Integration** zur Datenübertragung
- **WLAN-Verbindung** für Netzwerkanbindung
- **Status-LED** für Verbindungsstatus

## Benötigte Hardware

1. Raspberry Pi Pico W
2. SSD1306 OLED Display (128x64, I2C)
3. DHT22 Temperatur- und Feuchtigkeitssensor
4. Windrichtungsgeber mit Modbus RTU Schnittstelle
5. Externe Stromversorgung (5V)

## Pinbelegung (Raspberry Pi Pico W)

| Pin | Verwendung                | Anschluss            |
|-----|---------------------------|----------------------|
| 3V3 | Display Stromversorgung   | OLED VCC             |
| GND | Gemeinsame Masse          | OLED GND, Sensoren   |
| 0   | Modbus RTU RX             | Windgeber TX         |
| 1   | Modbus RTU TX             | Windgeber RX         |
| 5   | Status-LED                | Interne LED          |
| 15  | DHT22 Daten               | DHT22 Datenpin       |
| 16  | I2C SDA                   | OLED SDA             |
| 17  | I2C SCL                   | OLED SCL             |
| LED | Onboard-LED               | Systemstatus         |

## Software & Bibliotheken

- MicroPython Firmware für Raspberry Pi Pico W
- Bibliotheken:
  - `simple.py` (MQTT Client)
  - `robust.py` (MQTT Reconnect Logic)
  - `ssd1306.py` (OLED Treiber)
  - `dht.py` (DHT22 Treiber)
  - `umodbus` (für Modbus RTU)

## Konfiguration (`config.py`)

Die Konfiguration erfolgt in `config.py`:

```python
wifi_ssid = 'DEIN_WLAN_SSID'
wifi_password = 'DEIN_WLAN_PASSWORT'
mqtt_server = 'DEINE_MQTT_BROKER_IP'
mqtt_username = 'DEIN_MQTT_BENUTZER' # Optional, falls benötigt
mqtt_password = 'DEIN_MQTT_PASSWORT' # Optional, falls benötigt

Installation & Inbetriebnahme
MicroPython flashen: Installiere die aktuelle MicroPython-Firmware auf deinem Raspberry Pi Pico W.
Dateien übertragen: Kopiere die folgenden Dateien auf den Pico W:
Hauptprogramm: main.py
Konfiguration: config.py (angepasst mit deinen Daten)
Module: mqtt.py, wlan.py, wind.py, robust.py, simple.py
Treiber: ssd1306.py, dht.py
Bibliothek: den Ordner umodbus (falls als Ordnerstruktur vorhanden)
Hardware verbinden: Schließe alle Sensoren und das Display gemäß der Pinbelegung an.
System starten: Versorge den Pico W mit Strom oder starte ihn neu.
MQTT-Topics
Die Station publiziert auf folgenden Topics:

ext2/temperature: Aktuelle Temperatur in °C
ext2/humidity: Relative Luftfeuchtigkeit in %
wind_dir: Windrichtung als Gradzahl und Himmelsrichtung (z.B. "45, NE")
Bedienung
Nach dem Start verbindet sich das Gerät automatisch mit dem in config.py definierten WLAN.
Die gemessenen Werte werden auf dem OLED-Display angezeigt:
Obere Zeile: Gerätename (oder ein statischer Text)
Mittlere Zeilen: Temperatur und Luftfeuchtigkeit
Untere Zeile: Windrichtung
Die Daten werden zyklisch aktualisiert (Standard: alle 3 Sekunden).
Die interne LED des Pico W blinkt während des Betriebs, um Aktivität anzuzeigen.
Projektstruktur (Beispiel)
plaintext
/
│── main.py            # Hauptprogramm
│── config.py          # WLAN und MQTT Konfiguration
│── mqtt.py            # MQTT Client Logik
│── robust.py          # MQTT Reconnect Handler
│── simple.py          # MQTT Basisklasse
│── wlan.py            # WLAN Verbindungsmanagement
│── wind.py            # Windrichtungsmessung
│── ssd1306.py         # OLED Display Treiber
│── dht.py             # DHT22 Sensor Treiber
└── lib/               # Optionaler Ordner für Bibliotheken wie umodbus
    └── umodbus/
        └── ...
Details zur Windrichtungsmessung
Der Windrichtungsgeber liefert Werte über Modbus RTU:

Baudrate: 4800
Datenbits: 8
Stopbits: 1
Parity: None
Slave-Adresse: 1
Register: 0-4 (je nach Sensor-Spezifikation)
Die Werte werden in Himmelsrichtungen umgewandelt (N, NE, E, SE, S, SW, W, NW).

Troubleshooting
Keine WLAN-Verbindung:
SSID und Passwort in config.py überprüfen.
WLAN-Signalstärke und Erreichbarkeit des Routers sicherstellen.
Die Status-LED (interne LED des Pico) sollte während des Verbindungsaufbaus blinken.
Keine Sensordaten:
Verkabelung der Sensoren (DHT22, Windgeber) gemäß Pinbelegung prüfen.
Stromversorgung der Sensoren sicherstellen.
Für den DHT22 Sensor wird ein Pull-Up-Widerstand (typischerweise 4.7kΩ bis 10kΩ) zwischen dem Datenpin und VCC benötigt.
Display bleibt schwarz:
I2C-Adresse des Displays prüfen (oft 0x3C oder 0x3D).
Verkabelung der I2C-Leitungen (SDA, SCL) und der Stromversorgung des Displays kontrollieren.
Lizenz
Dieses Projekt steht unter der MIT-Lizenz. Details finden Sie in der LICENSE-Datei (falls vorhanden) oder unter opensource.org/licenses/MIT.

Mögliche Erweiterungen
Datenlogging: Hinzufügen einer SD-Karte für lokale Datenspeicherung.
OTA Updates: Implementierung von Over-The-Air Updates für die Firmware.
Energiesparmodus: Bei Batteriebetrieb einen Sleep-Modus integrieren, um Energie zu sparen.
Webinterface: Eine einfache Statusseite über einen integrierten Webserver auf dem Pico W bereitstellen.
Zusätzliche Sensoren: Integration weiterer Sensoren, z.B. für Luftdruck (BME280/BMP280) oder einen Regenmesser.