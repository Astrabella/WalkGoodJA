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




#class (models.Model):
#    connection = models.CharField(max_length=50)
#    current_state = models.IntegerField(default=0)
#    date_created = models.DateTimeField(auto_now_add=True)
#
#    def get_connection(self):
#        return self.connection
#
#    def get_date(self):
#        return self.date_created
#
#    def get_state(self):
#        return self.current_state
#
#    def set_state(self, new_state):
#        self.current_state = new_state
#
#    def __unicode__(self):
#        return self.connection
#
