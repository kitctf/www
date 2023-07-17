from dataclasses import dataclass
from ics import Calendar, Event
import requests
import os


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
    CTFEvent("CCCamp 2023", ctftime_id=2048),
    CTFEvent("Midnight Sun CTF 2023 Finals", ctftime_id=1922),
    CTFEvent("DEF CON Finals", begin="2023-08-10", end="2023-08-13"),
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
        e = Event()

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
        e.uid = e.uid or f"{hash(e.name)}@kitctf.de"

        c.events.add(e)

    with open(os.path.dirname(os.path.realpath(__file__)) + '/../hack_harder.ics', 'w') as f:
        f.writelines(c.serialize_iter())


if __name__ == "__main__":
    main()
