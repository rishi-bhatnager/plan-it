from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta
import time

class Task(models.Model):

    class Meta:
        #earliest() gets first result, meaning earliest addDate is selected; dueDate = tiebreaker
        get_latest_by = ['addDate', 'dueDate']

        #priority order of fields to use when ordering Task objects
        #this order prioritizes (in this order): earliest addDate, earliest dueDate, greatest expTime,
            #and name is ascending order
        ordering = ['addDate', 'dueDate', '-expTime', 'name', ]


    # NOTE: Django auto adds an auto-incrementing 'id' field --> create a field and set primary_key=True
        # to create custom id fields for tasks
    # ALSO: can specify IDs when saving Tasks to database

    name = models.CharField("Task Name", max_length=50, db_index=True)
        # optional first positional arg = human readable name
    notes = models.TextField(help_text="Notes", default="")
    category = models.CharField(max_length=5, choices = [
        ('Ex', 'Exercise'),
        ('Leis', 'Leisure'),
        ('House', 'Household'),
        ('Pers', 'Personal'),
        ('Work', 'Work'),
        ('', 'None'),
        ], default='')

    # The user to which this task belongs
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
        # NOTES:
        #   - Used ForeignKey so that if associated user is deleted then their tasks are also deleted (that's what the
        #       on_delete parameter does), but may need to switch to ManyToManyField for task sharing (so a single task
        #       can be associated with multiple users if, for example, the creating user invites other users onto the task)
        #   - Since there is a default of None, be sure to check that users aren't None before dealing with them

    addDate = models.DateTimeField("Time When Task was Added", default=timezone.now)
    dueDate = models.DateTimeField("Due Date",
        help_text="Enter by when must this task be completed in the following format: MM/DD/YYYY HH:MM")
    expTime = models.DurationField("Expected Time for Completion",
        help_text="Enter the amount of time you expect to need to complete this task in the following format: HH:MM")



    '''List containing tuples of length 3

        Collectively, the list represents all the times at which this task is scheduled
        Each tuple represents a time at which the task is scheduled in the user's planner
        Each tuple contains (in this order):
            1. A DateTimeField representing the start time at which this particular instance is scheduled
            2. A DurationField representing for how long this particular instance is scheduled
            3. A BooleanField representing whether this particular instance was scheduled effectively

        Assuming (for now) multiple tasks can be scheduled during the same istance, this represents a many-to-many
            relationship (one task maps to many times, and a time can map to multiple tasks). Since this maps both ways,
            you can list all the ScheduleInstances associated with a particular Task as well as all Tasks associated
            with a particular ScheduleInstance.
        The times field will map to ScheduleInstance objects containing the fields described above.
        To determine whether a task was effectively scheduled, use the function defined below (towards end of Task class),
            which returns the proportion of ScheduledInstances of that task that were considered effectively-scheduled.
              --> NOTE: since we may not receive feedback on particular (or any) instances, this method may not some
                  instances in the proportion or possibly even return None
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

    #returns None if no feedback was received, otherwise returns proportion of instances that were effectively-scheduled
    def effectiveTask(self):
        count = 0
        num_effective = 0

        for instance in self.times.all():
            if instance != None:
                count += 1
                if instance.effective == True:
                    num_effective += 1

        if count == 0:
            return None
        return num_effective / count


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
        self.orig = time

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
        unique_together = ['startTime',]

    startTime = models.DateTimeField("Start time of this scheduled instance")
    duration = models.DurationField("Duration of this scheduled instance")
    effective = models.BooleanField("Whether this instance was scheduled effectively", default=None)
        # ^ give a default of True if None gives errors

    def __str__(self):
        return f'Scheduled Instance at {CustomDateTime(self.startTime).convertToET()} for {self.duration}'

    def __repr__(self):
        return str(self)



# class AddTaskForm(UserCreationForm):
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
