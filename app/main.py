from datetime import datetime, timezone
from html import escape
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI(title="IT-Notfall Orchestrator")

# Walking skeleton only:
# Incidents intentionally live only in process memory.
incidents: dict[str, dict[str, str]] = {}


def page(title: str, body: str) -> HTMLResponse:
    return HTMLResponse(
        f"""<!doctype html>
<html lang="de">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <style>
      body {{
        font-family: system-ui, sans-serif;
        max-width: 48rem;
        margin: 2rem auto;
        padding: 0 1rem;
        line-height: 1.5;
      }}
      button {{
        font: inherit;
        padding: .8rem 1rem;
      }}
      .status {{
        display: inline-block;
        padding: .2rem .5rem;
        border: 1px solid currentColor;
        border-radius: .3rem;
      }}
    </style>
  </head>
  <body>
    {body}
  </body>
</html>"""
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    return page(
        "IT-Notfall Orchestrator",
        """
        <h1>IT-Notfall Orchestrator</h1>
        <p>Walking Skeleton: Incident anlegen.</p>

        <form method="post" action="/incidents">
          <button type="submit">Incident „SmartTag funktioniert nicht“ anlegen</button>
        </form>
        """,
    )


@app.post("/incidents")
def create_incident() -> RedirectResponse:
    incident_id = f"INC-{uuid4().hex[:8].upper()}"

    incidents[incident_id] = {
        "id": incident_id,
        "title": "SmartTag funktioniert nicht",
        "status": "OPEN",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    return RedirectResponse(
        url=f"/incidents/{incident_id}",
        status_code=303,
    )


@app.get("/incidents/{incident_id}", response_class=HTMLResponse)
def show_incident(incident_id: str) -> HTMLResponse:
    incident = incidents.get(incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident nicht gefunden")

    return page(
        incident["id"],
        f"""
        <h1>{escape(incident["title"])}</h1>

        <dl>
          <dt>Incident-ID</dt>
          <dd><code>{escape(incident["id"])}</code></dd>

          <dt>Status</dt>
          <dd><span class="status">{escape(incident["status"])}</span></dd>

          <dt>Angelegt</dt>
          <dd>{escape(incident["created_at"])}</dd>
        </dl>

        <p><a href="/">Zurück</a></p>
        """,
    )
