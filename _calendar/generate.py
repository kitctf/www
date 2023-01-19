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
    ctftime_id: int = None


# CHANGE ME
events = [
    CTFEvent("Insomni'hack teaser", ctftime_id=1831),
    CTFEvent('perfect blue ctf', ctftime_id=1763),
    CTFEvent('hxp CTF', ctftime_id=1845),
    CTFEvent('Dice CTF', ctftime_id=1838),
    CTFEvent("Insomni'hack", ctftime_id=1850)
]
# DON't CHANGE ME


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

        e.name = event.name or e.name
        e.begin = event.begin or e.begin
        e.end = event.end or e.end
        e.description = event.comment

        c.events.add(e)

    with open(os.path.dirname(os.path.realpath(__file__)) + '/../hack_harder.ics', 'w') as f:
        f.writelines(c.serialize_iter())


if __name__ == "__main__":
    main()
