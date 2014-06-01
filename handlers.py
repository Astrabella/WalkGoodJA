from rapidsms.contrib.handlers import PatternHandler
from reports.models import Report

import sys
import logging
logger = logging.getLogger('rapidsms')

class ReportHandler(PatternHandler):
    """ Handles the initialization of the reporting process. """
    pattern = r"^\s*R(eport)?\s*$"
    report = 0

    def help(self):
        # Create a new report in the DB
        self.report = Report(identity=self.msg.connection.identity, state=1)
        self.report.save()
        logger.debug("New report created")

        # Send initial response to user
        self.respond("Hello. Please text a number for the incident you are reporting..." +
                      "1-Verbal Abuse,  2-Physical Abuse,  3-Sexual Assault,  4-Robbery,  5-Rape")

    def handle(self, text):
        self.help()


class ResponseHandler(PatternHandler):
    pattern = r"^\s*([1-7])\s*$"

    def help(self):
        # Retrieve last report associated with current identity (phone number)
        try:
            r = Report.objects.filter(identity=self.msg.connection.identity).order_by('-last_modified')[0]
            logger.debug("Current report: " + str(r))
            state = r.get_state()
            logger.debug("Current state: " + str(state))
            pattern = self._pattern().match(self.msg.text).group(0)
            logger.debug("pattern: " + pattern)

            # Check the state (ID of last question sent)
            if(state == 1):
                # Save current response
                r.response_set.create(qid=1, details=pattern)

                # Send second response to user
                r.set_state(2)
                r.save()
                self.respond("Where did the incident occur? (Community name and parish)")

            elif(state == 6):
                r.response_set.create(qid=6, details=pattern)
                r.set_state(7)
                r.save()
                self.respond("Please text a number for your sexual identity. 1-Lesbian, 2-Gay, " +
                             "3-Bisexual/Allsexual, 4-Transgender, 5-Straight, 6-Other, 7-Don't Know")

            elif(state == 7):
                r.response_set.create(qid=7, details=pattern)
                r.set_state(8)
                r.save()
                self.respond("Thank you for your report. For more information please go to www.walkgoodja.info")

        except:
            # Log error
            logger.debug(sys.exc_info()[0])

            # User does not exist in DB, send instructions for beginning report
            self.respond("Hello. To begin a report please text 'Report' or 'R' to 123456.")


    def handle(self, text):
        self.help()
