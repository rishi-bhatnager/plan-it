from django.db import models
from django.utils import timezone
from datetime import timedelta
import time
import datetime

class Task(models.Model):
    # NOTE: Django auto adds an auto-incrementing 'id' field --> create a field and set primary_key=True
        # to create custom id fields for tasks
    # ALSO: can specify IDs when saving Tasks to database

    name = models.CharField("Task Name", max_length=50, db_index=True)
        # optional first positional arg = human readable name
    category = models.CharField(max_length=50, choices = [
        ('Ex', 'Exercise'),
        ('Leis', 'Leisure'),
        ('House', 'Household'),
        ('Pers', 'Personal'),
        ('Work', 'Work'),
        ('', 'None'),
        ], default='')
    expTime = models.DurationField("Expected Time for Completion", help_text="Enter the amount of time you expect to complete this task")
    dueDate = models.DateTimeField("Due Date", help_text="Enter by when must this task be completed")
    addDate = models.DateTimeField("Time When Task was Added", default=timezone.now)

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

    #saves a task to the database by first checking its validity and then using Django's save method
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)   #calls Django's save()



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
