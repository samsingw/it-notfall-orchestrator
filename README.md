# Update für samsingw/it-notfall-orchestrator

Aktueller Walking-Skeleton-Schritt: **M-ST-001 wird korrekt angezeigt**.

Enthalten:

- `app/main.py`
- `checklists/M-ST-001.json`
- `Dockerfile`

Die bestehende Fleet-HTTPRoute mit `PathPrefix: /` benötigt keine Änderung. Incidents und Checklistenstatus bleiben weiterhin nur im RAM; es gibt noch keine Abschlusslogik und keine Persistenz.

Nach Push und erfolgreichem GitHub-Actions-Build das Deployment neu starten, solange `latest` verwendet wird. Dann über Android einen Incident anlegen und den Link zu `M-ST-001` öffnen.
