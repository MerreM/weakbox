from django.contrib.auth.models import User
from django.db import models
import json


class Value(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=20)
    value = models.CharField(max_length=100, blank=True)

    def to_dict(self):
        return {"%s" % self.key: "%s" % self.value}

    def __unicode__(self):
        output = {"%s" % self.key: "%s" % self.value}
        return "%s  - %s " % (self.user, json.dumps(output))

    class Meta:
        unique_together = ("user", "key")


class Token(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField(max_length=512, unique=True)

    def __unicode__(self):
        return self.token
