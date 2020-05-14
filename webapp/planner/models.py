from django.db import models
from django.utils import timezone
from datetime import timedelta
import time
import datetime

class Task(models.Model):

    class Meta:
        #earliest() gets first result, meaning earliest addDate is selected; dueDate = tiebreaker
        get_latest_by = ['addDate', 'dueDate']

        ordering = ['name', 'category', 'addDate', 'dueDate', 'expTime']


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
    addDate = models.DateTimeField("Time When Task was Added", default=timezone.now)
    dueDate = models.DateTimeField("Due Date", help_text="Enter by when must this task be completed")
    expTime = models.DurationField("Expected Time for Completion", help_text="Enter the amount of time you expect to complete this task")

    '''List containing tuples of length 3

        Collectively, the list represents all the times at which this task is scheduled
        Each tuple represents a time at which the task is scheduled in the user's planner
        Each tuple contains (in this order):
            1. A DateTimeField representing the start time at which this particular instance is scheduled
            2. A DurationField representing for how long this particular instance is scheduled
            3. A BooleanField representing whether this particular instance was scheduled effectively

        This represents a one-to-many relationship (one task maps to many times), but this doesn't exist in Django,
            hence the many-to-many field, which maps both ways: you can list all the ScheduleInstances associated with a
            particular Task as well as all Tasks associated with a particular ScheduleInstance.
        The times field will map to ScheduleInstance objects containing the fields described above.
        A task is considered effectively scheduled based on the function defined below (towards end of Task class),
            which considers a Task effective if >= 50% of its scheduled times were effective.
              --> An alternative solution to using this method would be to store a boolean at the beginning of the list
                  that represents whether the Task was scheduled effectively (and we could use any number of ways to set
                  this value). To do this the times field would need to map to a class that contains a single boolean
                  as well as a mapping to the ScheduleInstance objects.
    '''
    times = models.ManyToManyField('ScheduleInstance', db_table='Scheduled Times')

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

    #returns True if this Task was scheduled effectively
    def effectiveTask(self):
        count = 0
        num_effective = 0

        for instance in self.times.all():
            count += 1
            if instance.effective == True:
                num_effective += 1

        return num_effective / count >= .5


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
        self.hour -= 4 if time.localtime().tm_isdst == 0 else 5
        if self.hour <= 0:
            self.hour += 24
            self.day -= 1

        self.changeTimeZone("US/Eastern")
        return self

    #toString, excluded microseconds attribute
    def __str__(self):
        return f'{self.year:04}/{self.month:02}/{self.day:02} {self.hour:02}:{self.minute:02}:{self.second:02} ({self.timezone})'

    def __repr__(self):
        return str(self)


class ScheduleInstance(models.Model):

    class Meta:
        ordering = ['startTime', 'duration', 'effective']
        # unique_together = ['startTime',]
            # ^ uncomment if we want startTimes to be unique

    startTime = models.DateTimeField("Start time of this scheduled instance")
    duration = models.DurationField("Duration of this scheduled instance")
    effective = models.BooleanField("Whether this instance was scheduled effectively")
        # ^ give a default value of False???

    def __str__(self):
        return f'Scheduled Instance at {CustomDateTime(self.startTime).convertToET()} for {self.duration}'

    def __repr__(self):
        return str(self)
