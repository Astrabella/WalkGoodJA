from django.db import models


class Report(models.Model):
    identity = models.charField(max_length=25)
    state = models.IntegerField(default=0) # current question ID
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def get_identity(self):
        return self.identity

    def set_identity(self, identity):
        self.identity = identity

    def __unicode__(self):
        return self.identity + "--" + self.id


class Response(models.Model):
    report = models.ForeignKey(Report) 
    qid = models.IntegerField(default=0) # question ID
    time_received = models.DateTimeField(auto_now_add=True)
    details = models.CharField(max_length=165)

    def __unicode__(self):
        return self.report.id + "--" + self.qid

    def get_details(self):
        return self.details

