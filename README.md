# Update für samsingw/it-notfall-orchestrator

Aktueller Walking-Skeleton-Schritt:

```text
Checkliste lässt sich abschließen
```

Dieses Update gehört ausschließlich in das Source-/Image-Repository.

Zu ersetzen:

```text
app/main.py
```

Keine Änderung an Fleet/HTTPRoute notwendig.

## Neu

- neuer Incident-Zustand `checklist_status`
- `NOT_STARTED` beim Anlegen
- `IN_PROGRESS` beim ersten Öffnen von M-ST-001
- Button `Checkliste abgeschlossen`
- `POST /incidents/{id}/checklist/complete`
- danach `COMPLETED`
- Incident-Seite zeigt den Checklistenstatus

## Bewusst noch nicht enthalten

- Ergebnis `gelöst/nicht gelöst`
- Datenbank
- Persistenz über Pod-Neustart

## Abnahmetest

1. Source-Repo committen und pushen.
2. GitHub-Actions-Build abwarten.
3. Deployment auf Test neu starten.
4. Incident anlegen.
5. M-ST-001 öffnen.
6. Button `Checkliste abgeschlossen` drücken.
7. Erwartet auf der Incident-Seite: `Checkliste abgeschlossen`.
8. Dasselbe auf Prod testen.
