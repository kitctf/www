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
    CTFEvent("ENOWARS 7", ctftime_id=2040),
    CTFEvent("DEF CON Finals", begin="2023-08-10", end="2023-08-13"),
    CTFEvent("CCCamp 2023", ctftime_id=2048),
    CTFEvent("Midnight Sun CTF 2023 Finals", ctftime_id=1922),
    CTFEvent("SekaiCTF 2023", ctftime_id=1923),
    CTFEvent("HITCON CTF 2023 Quals", ctftime_id=2019),
    CTFEvent("FAUST CTF 2023", ctftime_id=2011),
    CTFEvent("CyberSecurityRumble Finals 2023", begin="2023-09-28T13:00:00+02:00", end="2023-09-30T13:00:00+02:00"),
    CTFEvent("Hack.lu CTF 2023", ctftime_id=1921),
    CTFEvent("HITCON CTF 2023 Final", ctftime_id=2035),
    CTFEvent("Platypwn 2023", ctftime_id=2082),
    CTFEvent("LakeCTF", ctftime_id=2069),
    CTFEvent("SquareCTF", ctftime_id=2111),
    CTFEvent("saarCTF 2023", ctftime_id=2049),
    CTFEvent("KalmarCTF 2024", ctftime_id=2227),
    CTFEvent("Midnight Sun CTF 2024 Quals", ctftime_id=2247),
    CTFEvent("CyberSecurityRumble Quals", ctftime_id=2224),
    CTFEvent("DEF CON CTF Qualifier 2024", ctftime_id=2229),
    CTFEvent("FAUST CTF 2024", ctftime_id=2351),
    CTFEvent("Hack.lu CTF 2024", ctftime_id=2438),
    CTFEvent("Platypwn 2024", ctftime_id=2407),
    CTFEvent("GlacierCTF 2024", ctftime_id=2402),
    CTFEvent("saarCTF 2024", ctftime_id=2490),
    CTFEvent("LakeCTF Quals 24-25", ctftime_id=2502)
    
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
