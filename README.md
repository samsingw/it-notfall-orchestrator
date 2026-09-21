# Manuelle Synchronisation von M-ST-001

Dieses Paket gehört ausschließlich in `samsingw/it-notfall-orchestrator`.

## Source of Truth

Nicht die JSON-Datei pflegen.

Maßgeblich ist:

`IT-Notfall/docs/10_Massnahmen/SmartHome/M-ST-001_Batterie-Samsung-SmartTag-1-wechseln.md`

`checklists/generated/M-ST-001.json` ist nur ein vorläufig manuell synchronisiertes
Laufzeit-Artefakt.

## Übernahme

1. `checklists/generated/M-ST-001.json` ins Orchestrator-Repo übernehmen.
2. Die alte `checklists/M-ST-001.json` entfernen.
3. In `app/main.py` den `CHECKLIST_DIR` wie in `app/CHECKLIST_DIR.patch.txt`
   auf `/app/checklists/generated` ändern.
4. Das vorhandene Dockerfile kann unverändert bleiben, sofern es bereits
   `COPY checklists ./checklists` enthält.
5. Build + Rollout durchführen.

Die echten Bilder werden in diesem Schritt noch nicht vom Orchestrator ausgeliefert.
Das JSON enthält nur deren Referenzen. Die Bildintegration kommt separat.
