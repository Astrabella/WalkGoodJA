from rapidsms.apps.base import AppBase
from .models import Report, Response

import re
import logging
logger = logging.getLogger('rapidsms')

class FreeformHandler(AppBase):
    """ Handles all the freeform responses,
        aka responses to questions 2 and 3"""

    def handle(self, msg):
        r = Report.objects.filter(identity=msg.connection.identity).order_by('-last_modified')[0]
        state = r.get_state()

        if(state == 2): # msg is answer to question 2
            # Store response in DB
            r.response_set.create(qid=2, details=msg.text)

            # Send question 3
            r.set_state(3)
            r.save()
            msg.respond("Please give details of the incident. Use multiple texts if necessary. When you are finished type END.")

        elif(state == 3): # msg is answer to question 3
            # Check if message matches 'END'
            matchObj = re.match( r'.*[\s\.]*END[\s\.]*$', msg.text, re.I)
            if not matchObj is None:
                # Change state and send next question
                r.set_state(4)
                msg.respond("Please text a number for your gender. 1-Female, 2-Male, 3-Other")

            # Otherwise save response and wait for END
            r.response_set.create(qid=3, details=matchObj.group())
            r.save()

        return True
