# Kairos College Rides Organizer

A text messaging bot that automatically organizes rides for those who are off-campus.

## Getting Started

### Setup

Requires Python 3.10+ and a virtual environment.

Copy `keys_blank.json` to `keys.json` and `people_blank.json` to `people.json` and fill as appropriate.

> You need to fill out the section of keys that you are using.

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

* Switch backend to Twilio completely
* Remaining drivers are assigned after all passengers are assigned, but they really should be assigned to any empty cars left.
* Optimizer savestates via files, import and export support.
* Sometimes passengers are assigned to a driver farther away when they really could be assigned to someone that lives with them. This needs additional optimization.
* Automatically optimize once everyone has responded or the deadline has been reached.
* Notify people who they are taking, or if they don't have to drive.
* Add command line arguments.
* Post-service rides.
