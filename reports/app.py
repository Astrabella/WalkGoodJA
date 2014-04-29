from rapidsms.apps.base import AppBase
from .models import Report, Response

import re
import logging
logger = logging.getLogger('rapidsms')

class FreeformHandler(AppBase):
    """ Handles all the freeform responses,
        aka responses to questions 2, 3, 4 and 5"""

    def handle(self, msg):
        r = Report.objects.filter(identity=msg.connection.identity).order_by('-last_modified')[0]
        logger.debug("Current report: " + str(r))
        state = r.get_state()
        logger.debug("Current state: " + str(state))

        if(state == 2): # msg is answer to question 2
            # Store response in DB
            r.response_set.create(qid=2, details=msg.text)

            #Send question 3
            r.set_state(3)
            r.save()
            msg.respond("When did the incident occur? Give time and MM/DD/YY")

        elif(state == 3): # msg is answer to question 3
            # Store response in DB
            r.response_set.create(qid=3, details=msg.text)

            # Send question 4
            r.set_state(4)
            r.save()
            msg.respond("Please give details of the incident. Use multiple texts if necessary. When you are finished type END.")

        elif(state == 4): # msg is answer to question 4
            # Check if message matches 'END'
            matchObj = re.match( r'.*[\s\.]*END[\s\.]*$', msg.text, re.I)
            if not matchObj is None:
                # Change state and send next question
                r.set_state(5)
                msg.respond("How old are you? Type your age.")

            # Otherwise save response and wait for END
            r.response_set.create(qid=4, details=msg.text)
            r.save()

        elif(state == 5):
            r.response_set.create(qid=5, details=msg.text)
            r.set_state(6)
            r.save()
            msg.respond("Please text a number for your gender. 1-Female, 2-Male, 3-Other")


        return True
