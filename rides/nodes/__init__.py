from rides.util import domains
from typing import Tuple, Union


class person:
    def __init__(self, data: dict):
        self.fname = data['fname']
        self.lname = data['lname']
        self.phone = data['phone']
        self.carrier = data['carrier']
        self.address = data['address']
        self.last_step = None

    def email(self):
        return self.phone + '@' + domains[self.carrier]

    def step_start(self, mode: str, error: bool = False) -> Tuple[str, str]:
        self.last_step = self.step_start

        if error:
            return 'Let\'s try again.', f'Are you able to drive for {mode}? If you don\'t wish to drive, answer no. (yes/no)'
        return f'Hi, {self.fname}!', f'Are you able to drive for {mode}? (yes/no)'

    def step_can_drive(self, mode: str, error: bool = False) -> Tuple[str, str]:
        self.last_step = self.step_can_drive

        if error:
            return 'I didn\'t understand!', 'As a number, how many people can you take?'
        return 'Thanks!', 'How many people are you able to take?'

    def step_not_driving(self, mode: str, error: bool = False) -> Tuple[str, str]:
        self.last_step = self.step_not_driving
        
        return 'No worries.', 'We will try to find you a ride ASAP.'
    
    def wrap_next_step(self, mode: str, error: bool = False, result: Union[str, None] = None) -> Tuple[str, str]:
        if not self.last_step:
            return self.step_start(mode, error)
        
        elif self.last_step is self.step_start:
            return self.step_can_drive(mode, error)
        
        elif self.last_step is self.step_can_drive:
            pass

        elif self.last_step is self.step_not_driving:
            pass
