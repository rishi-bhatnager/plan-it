import datetime
from django.db import models
from django.utils import timezone
from datetime import timedelta
import time

class Task(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=20)
    expTime = models.DurationField("expected time for completion")
    dueDate = models.DateTimeField("due date")
    addDate = models.DateTimeField("time when task was added", default=timezone.now)

    def __str__(self):
        return self.name

    #returns expTime in minutes
    def getExpTime(self):
        return self.expTime.seconds / 60
        # return timedelta(minutes = self.expTime * 10**(-6) / 60)


    #returns dueDate in Eastern time
    def getDueDate(self):
        return CustomDateTime(self.dueDate).convertToET()

    #returns addDate in Eastern time
    def getAddDate(self):
        return CustomDateTime(self.addDate).convertToET()

    #returns time from now til due date
    def timeTilDue(self):
        return self.dueDate - timezone.now()



class CustomDateTime:
    def __init__(self, time):
        self.year = time.year
        self.month = time.month
        self.day = time.day
        self.hour = time.hour
        self.minute = time.minute
        self.second = time.second
        self.microsecond = time.microsecond
        self.timezone = time.tzinfo

    def changeTimeZone(self, newTimeZone):
        self.timezone = newTimeZone
        return self

    #converts to Eastern time
    def convertToET(self):
        self.hour -= 5 if time.localtime().tm_isdst == 0 else 6
        if self.hour <= 0:
            self.hour += 24
            self.day -= 1

        self.changeTimeZone("US/Eastern")
        return self

    #toString, excluded microseconds attribute
    def __str__(self):
        return f'{self.year:04}/{self.month:02}/{self.day:02} {self.hour:02}:{self.minute:02}:{self.second:02} ({self.timezone})'
