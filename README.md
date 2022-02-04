# Kairos College Rides Organizer

A text messaging bot that automatically organizes rides for those who are off-campus.

## Getting Started

### Setup

Requires Python 3.10+ and a virtual environment.

Copy `keys_blank.json` to `keys.json` and `people_blank.json` to `people.json` and fill as appropiate.

```bash
pip install wheel
pip install -r requirements.txt
```

### Running

```bash
python app.py
```

## To-Do

Please help me with these issues and to-do!

* Process all people and save the number of people they can take. Automatically let people know if they don't actually have to drive.
* Sometimes replies are not processed. Proposed fix: offset the start time so that all messages since the start are processed.
* Better logging.
