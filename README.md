# Update: Ergebnis „gelöst / nicht gelöst“

Dieses Update gehört ausschließlich in das Source-/Image-Repository
`samsingw/it-notfall-orchestrator`.

Enthalten:

```text
app/main.py
```

Nach Abschluss von M-ST-001 erscheinen auf der Incident-Seite zwei Buttons:

- `Gelöst`
- `Nicht gelöst`

Die Auswahl wird derzeit nur im RAM gespeichert.

`Gelöst` setzt:

```text
result = SOLVED
status = SOLVED
```

`Nicht gelöst` setzt:

```text
result = UNRESOLVED
status = UNRESOLVED
```

Noch nicht enthalten:

- Datenbank
- Persistenz
- Wiederherstellung nach Pod-Neustart

Abnahmetest auf Test und Prod:

1. neuen Incident anlegen
2. M-ST-001 öffnen
3. Checkliste abschließen
4. `Gelöst` wählen und Anzeige prüfen
5. neuen Incident anlegen
6. Checkliste abschließen
7. `Nicht gelöst` wählen und Anzeige prüfen
