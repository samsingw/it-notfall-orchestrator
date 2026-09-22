# UI-Verbesserungen für die Incident-Seite

Dieses Update gehört ausschließlich in das Source-/Image-Repository
`samsingw/it-notfall-orchestrator`.

Enthalten:

```text
app/main.py
README.md
```

## Änderungen

- `Status`, `Checkliste`, `Ergebnis` und `Angelegt` werden jetzt als einfache
  Tabelle angezeigt statt als button-artige Felder.
- Der bisherige Link zur Maßnahme wurde durch einen auffälligen Button ersetzt:

```text
Jetzt Checkliste öffnen und Schritt für Schritt durchführen
```

Funktional ändert sich nichts.

## Kurztest

1. Incident anlegen
2. prüfen, ob die Incident-Daten tabellarisch angezeigt werden
3. prüfen, ob der neue große Button gut sichtbar ist
4. Button anklicken
5. kontrollieren, dass M-ST-001 geöffnet wird
