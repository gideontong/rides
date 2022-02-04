from datetime import datetime
from pytz import UTC
from rides.util import domains
from rides.util.chat import parse_number, parse_yes_no
from typing import Tuple, Union


class person:
    def __init__(self, data: dict) -> 'person':
        self.fname = data['fname']
        self.lname = data['lname']
        self.phone = data['phone']
        self.carrier = data['carrier']
        self.address = data['address']
        self.last = datetime.utcnow().replace(tzinfo=UTC)
        self.last_step = None

        self.needs_ride = False
        self.has_car = False
        self.passengers = 0

    def email(self) -> str:
        return self.phone + '@' + domains[self.carrier]

    def step_start(self, mode: str, error: bool = False) -> Tuple[str, str]:
        self.last = datetime.utcnow().replace(tzinfo=UTC)
        self.last_step = self.step_start

        if error:
            return 'Let\'s try again.', f'Are you able to drive for {mode}? If you don\'t wish to drive, answer no. (yes/no)'
        return f'Hi, {self.fname}!', f'Are you able to drive for {mode}? (yes/no)'

    def step_can_drive(self, mode: str, error: bool = False) -> Tuple[str, str]:
        self.last = datetime.utcnow().replace(tzinfo=UTC)
        self.last_step = self.step_can_drive

        if error:
            return 'I didn\'t understand!', 'As a number, how many people can you take (do not include yourself)?'
        return 'Thanks!', 'Not including yourself, how many people are you able to take?'

    def step_not_driving(self, mode: str, error: bool = False) -> Tuple[str, str]:
        self.last = datetime.utcnow().replace(tzinfo=UTC)
        self.last_step = self.step_not_driving
        
        if error:
            return 'I didn\'t understand!', f'Will you need a ride to {mode}? (yes/no)'
        return 'No worries.', f'Will you need a ride to {mode}? (yes/no)'

    def step_find_passengers(self, mode: str, error: bool = False) -> Tuple[str, str]:
        self.last = datetime.utcnow().replace(tzinfo=UTC)
        self.last_step = self.step_find_passengers

        return 'Thanks!', 'If anyone needs a ride, we will let you know. We really appreciate you :)'

    def step_find_drivers(self, mode: str, error: bool = False) -> Tuple[str, str]:
        self.last = datetime.utcnow().replace(tzinfo=UTC)
        self.last_step = self.step_find_drivers

        return 'Hold on tight.', 'We will try to find someone take you soon, and you should get an update text.'
    
    def step_no_ride(self, mode: str, error: bool = False) -> Tuple[str, str]:
        self.last_step = self.step_no_ride
        
        return 'No worries.', 'Hopefully you can make it anyways!'

    def wrap_next_step(self, mode: str, result: Union[str, None] = None) -> Tuple[str, str]:
        if not self.last_step:
            return self.step_start(mode)
        
        elif self.last_step == self.step_start:
            answer, confident = parse_yes_no(result)

            if not confident:
                return self.step_start(mode, error=True)
            
            if answer:
                self.has_car = True
                return self.step_can_drive(mode)
            else:
                return self.step_not_driving(mode)
        
        elif self.last_step == self.step_can_drive:
            answer, confident = parse_number(result)
            
            if not confident:
                return self.step_can_drive(mode, error=True)
            
            if answer > 0:
                self.passengers = answer
                return self.step_find_passengers(mode)
            else:
                return self.step_not_driving(mode, error=True)

        elif self.last_step == self.step_not_driving:
            answer, confident = parse_yes_no(result)

            if not confident:
                return self.step_not_driving(mode, error=True)
            
            if answer:
                self.needs_ride = True
                return self.step_find_drivers(mode)
            else:
                return self.step_no_ride(mode)
