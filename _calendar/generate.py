from dataclasses import dataclass
from ics import Calendar, Event
import requests
import os
import hashlib


@dataclass
class CTFEvent:
    name: str
    begin: str = None
    end: str = None
    comment: str = None
    location: str = None
    ctftime_id: int = None


# CHANGE ME
events = [
    CTFEvent("GlacierCTF 2024", ctftime_id=2402),
    CTFEvent("saarCTF 2024", ctftime_id=2490),
    CTFEvent("LakeCTF Quals 24-25", ctftime_id=2502),
    CTFEvent("snakeCTF 2024 Finals", ctftime_id=2419)

]
# DON'T CHANGE ME


def ctftime_event(id: int):
    response = requests.get(f"https://ctftime.org/api/v1/events/{id}/", headers={
        'user-agent': 'kitctf.de calendar bot'  # cloudflare kills us without this
    })
    return response.json()


def main():
    c = Calendar()

    for event in events:
        e = Event(uid="asdasd")
        e.uid = None # Explicitly remove the auto-generated uid again. Otherwise we can not distinguish between events
        # that have a default uid or one that is based on the ctftime id.

        if event.ctftime_id:
            ctftime = ctftime_event(event.ctftime_id)
            e.name = ctftime['title']
            e.begin = ctftime['start']
            e.end = ctftime['finish']
            e.location = ctftime['url']
            e.uid = f"{event.ctftime_id}@ctftime.org"

        e.name = event.name or e.name
        e.begin = event.begin or e.begin
        e.end = event.end or e.end
        e.location = event.location or e.location
        e.description = event.comment
        e.uid = e.uid or f"{hashlib.sha256(e.name.encode()).hexdigest()}@kitctf.de"

        c.events.add(e)
    uids : list[str] = [e.uid for e in c.events]
    assert len(uids) == len(set(uids)), "Duplicate UIDs detected" # For future me.
    assert all(e.uid is not None for e in c.events), "All UIDs should be set" # For future me.

    with open(os.path.dirname(os.path.realpath(__file__)) + '/../hack_harder.ics', 'w') as f:
        f.writelines(c.serialize_iter())


if __name__ == "__main__":
    main()
