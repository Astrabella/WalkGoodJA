from rapidsms.contrib.handlers import KeywordHandler
from reports.models import Report

import sys
import logging
logger = logging.getLogger('rapidsms')

class ReportHandler(KeywordHandler):
    """ Handles the initialization of the reporting process. """
    keyword = "Report|R"
    report = 0

    def help(self):
        # Create a new report in the DB
        self.report = Report(identity=self.msg.connection.identity, state=1)
        self.report.save()

        # Send initial response to user
        self.respond("Hello. Please text a number for the incident you are reporting..." +
                      "1-Verbal Abuse,  2-Physical Abuse,  3-Sexual Assault,  4-Robbery,  5-Rape")

    def handle(self, text):
        self.help()


class ResponseHandler(KeywordHandler):
    keyword="1|2|3|4|5"

    def help(self):
        # Retrieve last report associated with current identity (phone number)
        try:
            r = Report.objects.filter(identity=self.msg.connection.identity).order_by('-last_modified')[0]
            logger.debug("Report received")

            # Check the state (ID of last question sent)
            state = r.get_state()
            if(state == 1):
                logger.debug("State identified")
                # Save current response
                keyword = self._keyword().match(self.msg.text).group(0)
                r.response_set.create(qid=1, details=keyword)
                logger.debug("Response set created")

                # Send second response to user
                r.set_state(2)
                r.save()
                self.respond("Where did the incident occur? (Community name and parish)")
        except:
            # Log error
            logger.debug(sys.exc_info()[0])

            # User does not exist in DB, send instructions for beginning report
            self.respond("Hello. To begin a report please text 'Report' or 'R' to 123456.")
            raise


    def handle(self, text):
        self.help()
