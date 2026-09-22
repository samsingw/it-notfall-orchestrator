from datetime import datetime, timezone
from html import escape
import json
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI(title="IT-Notfall Orchestrator")

incidents: dict[str, dict[str, str | None]] = {}
CHECKLIST_DIR = Path("/app/checklists/generated")


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
      button, .button {{
        font: inherit;
        display: inline-block;
        padding: .8rem 1rem;
        margin: .25rem .25rem .25rem 0;
      }}
      .status {{
        display: inline-block;
        padding: .2rem .5rem;
        border: 1px solid currentColor;
        border-radius: .3rem;
      }}
      .step {{
        border-top: 1px solid #bbb;
        padding-top: 1rem;
        margin-top: 1.5rem;
      }}
      .expected {{
        margin-left: 1rem;
      }}
      .placeholder {{
        border: 1px dashed #888;
        padding: .75rem;
        margin: 1rem 0;
      }}
      .result-actions {{
        margin-top: 1.5rem;
        padding-top: 1rem;
        border-top: 1px solid #bbb;
      }}
      code {{
        overflow-wrap: anywhere;
      }}
    </style>
  </head>
  <body>
    {body}
  </body>
</html>"""
    )


def load_checklist(checklist_id: str) -> dict:
    path = CHECKLIST_DIR / f"{checklist_id}.json"
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Checkliste nicht gefunden")
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def render_list(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{escape(item)}</li>" for item in items) + "</ul>"


def get_incident(incident_id: str) -> dict[str, str | None]:
    incident = incidents.get(incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident nicht gefunden")
    return incident


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
        "checklist_id": "M-ST-001",
        "checklist_status": "NOT_STARTED",
        "result": None,
    }
    return RedirectResponse(url=f"/incidents/{incident_id}", status_code=303)


@app.get("/incidents/{incident_id}", response_class=HTMLResponse)
def show_incident(incident_id: str) -> HTMLResponse:
    incident = get_incident(incident_id)
    checklist = load_checklist(str(incident["checklist_id"]))

    checklist_status = str(incident.get("checklist_status") or "NOT_STARTED")
    checklist_status_label = {
        "NOT_STARTED": "Noch nicht begonnen",
        "IN_PROGRESS": "In Bearbeitung",
        "COMPLETED": "Checkliste abgeschlossen",
    }.get(checklist_status, checklist_status)

    result = incident.get("result")
    result_label = {
        "SOLVED": "Gelöst",
        "UNRESOLVED": "Nicht gelöst",
    }.get(result, "Noch nicht festgelegt")

    result_actions = ""
    if checklist_status == "COMPLETED" and result is None:
        result_actions = f"""
        <div class="result-actions">
          <h2>Ergebnis</h2>
          <p>Hat die Maßnahme das Problem gelöst?</p>

          <form method="post"
                action="/incidents/{escape(incident_id)}/result/solved"
                style="display:inline">
            <button type="submit">Gelöst</button>
          </form>

          <form method="post"
                action="/incidents/{escape(incident_id)}/result/unresolved"
                style="display:inline">
            <button type="submit">Nicht gelöst</button>
          </form>
        </div>
        """

    return page(
        str(incident["id"]),
        f"""
        <h1>{escape(str(incident["title"]))}</h1>

        <dl>
          <dt>Incident-ID</dt>
          <dd><code>{escape(str(incident["id"]))}</code></dd>

          <dt>Status</dt>
          <dd><span class="status">{escape(str(incident["status"]))}</span></dd>

          <dt>Checkliste</dt>
          <dd><span class="status">{escape(checklist_status_label)}</span></dd>

          <dt>Ergebnis</dt>
          <dd><span class="status">{escape(result_label)}</span></dd>

          <dt>Angelegt</dt>
          <dd>{escape(str(incident["created_at"]))}</dd>
        </dl>

        <p>
          <a class="button" href="/incidents/{escape(incident_id)}/checklist">
            {escape(checklist["id"])} – {escape(checklist["title"])}
          </a>
        </p>

        {result_actions}

        <p><a href="/">Zurück</a></p>
        """,
    )


@app.get("/incidents/{incident_id}/checklist", response_class=HTMLResponse)
def show_checklist(incident_id: str) -> HTMLResponse:
    incident = get_incident(incident_id)

    if incident.get("checklist_status") == "NOT_STARTED":
        incident["checklist_status"] = "IN_PROGRESS"

    checklist = load_checklist(str(incident["checklist_id"]))

    body = [
        f"<h1>{escape(checklist['id'])} – {escape(checklist['title'])}</h1>",
        f"<p><strong>Ziel:</strong> {escape(checklist['goal'])}</p>",
        "<h2>Benötigt</h2>",
        render_list(checklist["needed"]),
        "<h2>Werkzeugstandort</h2>",
        "<p>" + " → ".join(escape(part) for part in checklist["tool_location"]) + "</p>",
        "<h2>Checkliste</h2>",
    ]

    for step in checklist["steps"]:
        body.append('<section class="step">')
        body.append(f"<h3>{step['number']} – {escape(step['title'])}</h3>")
        body.append(render_list([f"☐ {action}" for action in step["actions"]]))

        if step.get("expected"):
            body.append('<div class="expected"><strong>Erwartet:</strong>')
            body.append(render_list(step["expected"]))
            body.append("</div>")

        if step.get("image"):
            body.append(
                '<div class="placeholder"><strong>Bild:</strong> '
                + escape(step["image"]["caption"])
                + " ("
                + escape(step["image"]["file"])
                + ")</div>"
            )

        body.append("</section>")

    body.extend([
        "<h2>Abschluss</h2>",
        f"<p>{escape(checklist['completion'])}</p>",
    ])

    if incident.get("checklist_status") != "COMPLETED":
        body.append(
            f"""
            <form method="post"
                  action="/incidents/{escape(incident_id)}/checklist/complete">
              <button type="submit">Checkliste abgeschlossen</button>
            </form>
            """
        )
    else:
        body.append("<p><strong>Checkliste abgeschlossen.</strong></p>")

    body.append(
        f'<p><a href="/incidents/{escape(incident_id)}">Zurück zum Incident</a></p>'
    )

    return page(
        f"{checklist['id']} – {checklist['title']}",
        "".join(body),
    )


@app.post("/incidents/{incident_id}/checklist/complete")
def complete_checklist(incident_id: str) -> RedirectResponse:
    incident = get_incident(incident_id)
    incident["checklist_status"] = "COMPLETED"
    return RedirectResponse(url=f"/incidents/{incident_id}", status_code=303)


@app.post("/incidents/{incident_id}/result/solved")
def mark_solved(incident_id: str) -> RedirectResponse:
    incident = get_incident(incident_id)
    if incident.get("checklist_status") != "COMPLETED":
        raise HTTPException(
            status_code=409,
            detail="Checkliste muss zuerst abgeschlossen werden",
        )
    incident["result"] = "SOLVED"
    incident["status"] = "SOLVED"
    return RedirectResponse(url=f"/incidents/{incident_id}", status_code=303)


@app.post("/incidents/{incident_id}/result/unresolved")
def mark_unresolved(incident_id: str) -> RedirectResponse:
    incident = get_incident(incident_id)
    if incident.get("checklist_status") != "COMPLETED":
        raise HTTPException(
            status_code=409,
            detail="Checkliste muss zuerst abgeschlossen werden",
        )
    incident["result"] = "UNRESOLVED"
    incident["status"] = "UNRESOLVED"
    return RedirectResponse(url=f"/incidents/{incident_id}", status_code=303)
