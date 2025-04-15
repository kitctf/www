import os
import subprocess
from ics import Calendar, Event
import requests
from typing import List, Tuple

# Paths
generate_script: str = os.path.dirname(os.path.realpath(__file__)) + "/generate.py"
generated_ics_path: str = (
    os.path.dirname(os.path.realpath(__file__)) + "/../hack_harder.ics"
)
existing_ics_path: str = (
    os.path.dirname(os.path.realpath(__file__)) + "/../hack_harder.ics.old"
)


def die() -> str:
    """Exit the script with an error message if the GITHUB_TOKEN is not set."""
    print("GITHUB_TOKEN environment variable is not set.")
    exit(1)


# GitHub repository details
GITHUB_REPO: str = "kitctf/www"
GITHUB_API_URL: str = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN") or die()


def run_generate_script() -> None:
    """Run the generate.py script to create a new .ics file."""
    result = subprocess.run(
        ["python3", generate_script], check=True, capture_output=True
    )
    print(result.stdout.decode())


def load_calendar(file_path: str) -> Calendar:
    """Load a calendar from an .ics file."""
    with open(file_path, "r") as f:
        return Calendar(f.read())


def compare_calendars(
    existing_calendar: Calendar, generated_calendar: Calendar
) -> List[Tuple[str, Event, Event]]:
    """Compare two calendars and return a list of events with date changes."""
    existing_events: dict[str, Event] = {
        event.uid: event for event in existing_calendar.events
    }
    generated_events: dict[str, Event] = {
        event.uid: event for event in generated_calendar.events
    }
    print(
        f"Existing events: {len(existing_events)}, Generated events: {len(generated_events)}"
    )

    changes: List[Tuple[str, Event, Event]] = []
    for uid, generated_event in generated_events.items():
        existing_event = existing_events.get(uid)
        if existing_event and (
            existing_event.begin != generated_event.begin
            or existing_event.end != generated_event.end
        ):
            changes.append((uid, existing_event, generated_event))
    return changes


def create_github_issue(title: str, body: str) -> None:
    """Create an issue in the GitHub repository."""
    headers: dict[str, str] = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    data: dict[str, str] = {
        "title": title,
        "body": body,
    }
    response = requests.post(GITHUB_API_URL, json=data, headers=headers)
    if response.status_code == 201:
        print(f"Issue created: {response.json()['html_url']}")
    else:
        print(f"Failed to create issue: {response.status_code}, {response.text}")


def main() -> None:
    """
    Main function to compare two calendar files and create a GitHub issue if changes are detected.
    Steps:
    1. Backup the existing `.ics` file by renaming it.
    2. Run the `generate.py` script to create a new `.ics` file.
    3. Load the existing and newly generated calendar files.
    4. Compare the two calendars for changes in event dates.
    5. If changes are detected, create a GitHub issue summarizing the differences.
    6. Remove the backed-up existing `.ics` file.
    Raises:
        FileNotFoundError: If any of the required `.ics` files are missing.
        Exception: If there are issues during the comparison or GitHub issue creation.
    """

    # Step 0: Ensure the existing .ics file is backed up
    os.rename(generated_ics_path, existing_ics_path)

    # Step 1: Run the generate.py script
    run_generate_script()
    print("Generated new .ics file.")

    # Step 2: Load the existing and generated calendars
    existing_calendar: Calendar = load_calendar(existing_ics_path)
    generated_calendar: Calendar = load_calendar(generated_ics_path)

    # Step 3: Compare the calendars
    changes: List[Tuple[str, Event, Event]] = compare_calendars(
        existing_calendar, generated_calendar
    )

    # Step 4: Batch all changes into a single GitHub issue
    if changes:
        title: str = f"Date changes detected for {len(changes)} events"
        body_lines: List[str] = ["The following events have detected date changes:\n"]
        for uid, existing_event, generated_event in changes:
            body_lines.append(
                f"**Event UID:** {uid}\n"
                f"**Event Name:** {generated_event.name}\n"
                f"**Existing Start Date:** {existing_event.begin}\n"
                f"**New Start Date:** {generated_event.begin}\n"
                f"**Existing End Date:** {existing_event.end}\n"
                f"**New End Date:** {generated_event.end}\n\n"
            )
        body: str = "\n".join(body_lines)
        create_github_issue(title, body)

    # Step 5: Remove the existing .ics file
    os.remove(existing_ics_path)


if __name__ == "__main__":
    main()
