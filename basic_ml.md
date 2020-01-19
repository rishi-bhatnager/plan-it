There are a lot of ideas going around for the ML but I think we need to start with something simple that will work well. I propose we use the following simple mechanism:

1. A user answers the following questions and enters details upon signing up:
  1. When do you usually sleep?
  2. When do you usually eat?
  3. Link your Google Calendar if you have one

2. We generate a matrix for them. This has length 48 (24 h / 0.5 h) and width c (c = num categories). To do so, we mark times asleep as zeros and set the remaining awake times as the average values of previous users.

3. Now, the user begins to put tasks in. They submit their tasks for the day as a batch to the python scripts.

4. Script adds in the Google Calendar events to this vector, setting those times to zero. loops through the tasks. First task is of length l. Loop through all the length l times in the day vector and pick the one with the highest associated probability in the individual's matrix. Do this for each task, putting each in the next best spot in order of priority.

5. Send this schedule back to the user. When they cross something off, mark the task as completed, and note how close it was to the expected completion time. At the end of the day, if they mark everything off at once, we only know that the schedule as a whole was good, so we can boost everything in those categories up a tiny bit. If we also know with reasonable certainly that they marked things off when completed (which can be done by comparing cross off time to task assignment time), we can infer that this time and category combination was good. So we can increase that specific value in the matrix.


Limitations:

1. Does not factor in the relationships between tasks, or how the user is feeling.
2. Could take a while to learn user vector, since only a couple indecies change each day. (Though we could implement a bleed into nearby areas to accelerate the process.)
