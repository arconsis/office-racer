# office-racer

This is going to be the repository for every development we are doing on the by-weekly arconsis hardware stream on [Twitch](https://www.twitch.tv/arconsis)

## 1. Stream 19. April 2022

Erste Schritte in dem Projekt sind das Setup.

Dinge die wir brauchen

- Raspberry pi 4 2GB
- 8GB SD-Karten
- Elecrow 4WD Chassis Smart Car

### PC/Mac

Hier bereiten wir alles vor, um den Raspberry Pi richtig zu konfigurieren

Der [Raspberry Pi Imager](https://www.raspberrypi.com/software/) hilft dabei sehr.

Mit dem Raspberry Pi Imager können ohne großen Aufwand SD-Karten vorbereitet werden. wir haben uns für das `Raspbery Pi OS Lite (64bit)` entschieden ( `CHOOSE OS` -> `Raspberry Pi OS (other)` -> `Raspbery Pi OS Lite (64bit)`). Wenn das OS ausgewählt ist und eine SD-Karte angeschloßen ist, kann diese über den `CHOOSE STORAGE` Button ausgewählt werden.

Bevor wir nun auf `WRITE` klicken können wir noch ein paar Änderungen über das Settingsmenü eintragen, um uns sehr viel Arbeit zu sparen. Hier kann man WLAN, Hostname, User und Password und vieles mehr einstellen.

Wer es lieber auf die altmodische Art und Weise machen will kann sich gerne in dem Ordner `Raspberry Pi setup` die nötigen Dateien ändern und auf die SD-Karte kopieren. Hier ist zu beachten, dass die leere `ssh` Datei beim Raspberry den SSH zugang freischaltet. Die `wpa_supplicant. conf` Datei richtet das WLAN ein, mit welchem sich verbunden werden soll.

Bevor wir nun den Raspberry Pi anschalten könnt ihr den Download von PyCharm CE schon mal starten. Das ist die IDE, die wir nutzen werden, um Python Code zu schreiben.

### Raspberry Pi

SD-Karte in den Raspberry Pi einschieben und den Raspberry Pi starten.

Jetzt sollte der Raspberry Pi booten und sich automatisch mit dem konfigurierten WLAN verbinden.

Über den Befehl `arp -a` kann unter unix-systemen der Raspberry Pi ganz einfach gefunden werden, denn dieser Befehl listet alle ip-Adressen im Netzwerk mit kleiner Beschreibung auf.

Jetzt können wir uns über ssh in den Raspberry Pi einloggen. Standard login-daten beim Raspberry sind:

- user: `pi`
- password: `raspberry`

Bevor wir mit der Programmierung anfangen, sollte der Raspberry auf dem aktuellsten Stand sein. Dies erreichen wir mit dem Befehl `sudo apt update && sudo apt upgrade -y`
Zur Erklärung: `apt` ist ein Kommandozeilen-tool, welches deb Packages verwaltet (Pakete/Software die unter Debian und Ubuntu laufen). Der `update` Befehl aktualisiert die Softwareliste, damit alle aktuellen Versionen von Paketen und Software dem System bekannt sind.
`upgrade` führt dann schließen das updaten der Software durch. Mit dem zusatz `-y` werden alle Fragen während des update-prozesses mit Ja beantwortet. Da wir das System selbst auch updaten wollen brauchen wir dafür spezielle Rechte, die uns mit `sudo` erteilt werden.
Und zu guter Letzt, die `&&`, diese verbinden mehrere Befehle miteinander. Ohne diese wären es 2 Befehle, also 2 Zeilen.

Jetzt ist unser System so weit, dass wir mit der eigentlichen Einrichtung beginnen können. Da wir Python nutzen wollen, müssen wir dazu einige Pakete installieren.

`sudo apt install python3 python3-venv python3-pip`
`sudo` und `apt` kennt ihr schon, also konzentrieren wir uns auf `install` und `python3 python3-venv python3-pip`.
`apt install` macht genau das was der Name sagt, es installiert Pakete und in diesem Fall gleich 3 Stück.

- `python3` ist die aktuelle Version von der Programmiersprache python
- `python3-venv` ist ein virtual Enviroment tool für Python3. Damit können pro Projekt, dependencies installiert werden ohne das System voll zu müllen.
- `python3-pip` ist ein Package-manager für Python-Pakete oder -Libraries. Hiermit lassen sich ganz einfach Pakete installieren und wieder löschen.

### venv

venv (virtual environments) sind kleine Sandkästen für ein Projekt und können mit `python3 -m venv /path/to/env-folder` erstellt werden. Um das Projekt sauber zu halten, erstellen wir in unserem Projekt-Ordner einen Unterordner names `venv`(dies erstellt der Befehl automatisch, wenn der Pfad noch nicht besteht). Damit das venv auch genutzt werden kann, müssen wir es mit `source venv/bin/activate` noch aktivieren. Jetzt solltet ihr im Terminal `(venv)` sehen. Um das venv wieder zu deaktivieren könnt ihr einfach `deactivate` aufrufen.

Mit dem aktivierten venv, können wir nun Pakete via pip installieren. Analog zu apt `pip3 install .....` (wir brauchen hier keine besondere Berechtigung, also ohne `sudo`).
