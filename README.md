# Update für samsingw/it-notfall-orchestrator

Dieses Archiv gehört ausschließlich in das Repository, das das Container-Image baut.

Zu ersetzen/übernehmen:

```text
app/main.py
```

Der vorhandene Dockerfile-, requirements.txt- und GitHub-Actions-Stand bleibt unverändert.

Implementiert:

- GET /health
- GET /
- POST /incidents
- GET /incidents/{id}

Incidents liegen absichtlich nur im RAM.
