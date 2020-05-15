So... how would the ML work? It needs to recognize the trends behind user completion. We need to find out which configurations of a given set of tasks lead to the best productivity. If we know what productivity previous task arrangements have caused in the past, we can infer what plans will yield the highest performance in the future. There are multiple ways we could go about this…

Option 1:

Somehow vectorize the schedule and put it into a neural net that outputs some productivity index for that arrangement. Train this net enough and we will be able to test all possible schedules to see which is the best. How can a schedule be vectorized? This is pretty much the most important theoretical question we would need to figure out. Too many features and the model will be inefficient; too few and it will not be able to find patterns. Each schedule takes in x tasks for the day. It is constrained by the number of hours the user has specified and the number of hours of the tasks. Other than that, it can presumably arrange the tasks in several ways. A schedule is characterized by how much it prioritizes early due dates, how well

Option 2:

We learn features about each individual, and insert those into a generic planning algorithm. For example, if a person seems to work well in the evening, those times are given priority. So this requires an input vector that begins as the average person and is tweaked with new data. This vector would include things like how stressed the user is on average, the time of day they work best, and how efficient they tend to be. This would necessitate a handmade algorithm that prioritizes based on these features. The upshot is that this requires essentially no complex training. Simply altering vectors by some set percentage each day would be sufficient to encapsulate changes in the user.

Option 3:

We construct a probability tensor (3D matrix) for each individual. This tensor defines how likely the user is to do work in each hour (or maybe half hour) of the day, in each category, and in each state of stressed-ness. This begins as the average tensor and eventually becomes customized with time. We can see how often a user did tasks they were assigned, and then adjust the tensor accordingly. Now, this tensor would be 24xnxm, where n and m are number of categories and number of stressed levels respectively. These two values will probably be in the realm of 5, so our tensor will have about 600 values in it. That will take a lot of training to figure out, as each day only gives a few data points. Perhaps trends can be inferred, and changes can be made to tensor positions that were never actually tested. For example, if someone tends to do well in the morning regardless of task category, we can extend this probability to tasks that weren’t necessarily tested themselves.

Option 4:

There are these things called recurrent nueral nets (RNNs) that can predict future things based on a running sequence. One example of their use has been in artificial music generation, where these systems take a handful of recent music notes and predict what the next one should be. Suppose we train an RNN on historically good schedules (regularized for stress level) to predict the difficuly level and category that each consecutive task in the sequence should ideally have. Then we simply put the closest available next task into that plan. If we assume an ideal RNN, then this model should capture the dependencies between tasks in a given list and put them into a decent plan.

Conclusion:

It seems as though options 2 and 3 are similar, with option 3 simply using more data for the user's data array than 2. Both systems also rely on a good general algorithm that does the best thing based on this learned data. This may not be that easy, as I will attempt to illustrate: Consider a user who likes to get work done at night, and that we have trained a data structure which encapsulates this behavior accurately. He has two big things on his list, one hard (3 hours) and due tomorrow, one easy (1 hour) and due in three days. Should the general algorithm put task 1 first thing in the morning to increase its chances of being completed, or task 2 to get the ball rolling for task 1 to get done later? Even with an ideal vector of this user's best working times, we still may have to make guesses with our general algorithm in an attempt to maximize user completion of tasks.

Option 1 tries to do away with this uncertainty by looking at each schedule as a whole and giving it some "fitness" value. With a vectorized representation of the schedule, we should in theory be able to train a neural net that understands the dependencies that exist within the user's preferred arrangements. The concern here is how to vectorize schedules, since there doesn't seem to be a clear way to make two schedules of different task number equal size. This is what option 4 tries to fix. By using an RNN the schedules can fit into the algorithm at any length since the algorithm trains on a per task basis. The problem here is that we may need a lot of good data before any real trend is picked up since we're trying to pull out some abstract meaning from the ordering, which could be (and likely is) highly random.

Therefore I think we should go for option 2 or 3 to begin with, as these personalized day vectors will be comparatively easier to train and understand. A general algorithm can likely be constructed to avoid serious conflicts, in which case this path seems rather desirable.

Random Thoughts:

Buffer times change based on length of blocks and types of task
Adjusting times to sleep schedules
To do list is created each day, starting at time when app is opened and schedule is sent through.

Possible Points of Failure:

1. The user could forget to remove items from the list. This would cause the app to schedule a ton of overdue shit for them to do. Should be smart enough to realize when user has a bunch of expired tasks and stop sending notifs for invalid time slots

2. In order to measure how well someone works in each hour, you would think we can just look at what they cross off at the end of the day and say the tasks that were not done had bad timing. This is not reasonable though, since a task may have been pushed forward due to bad timing before that task, only to be completed while another task was supposed to be. Thus we can only evaluate the fitness of a schedule as a whole unless they give us data during the day. How can we get data during the day? Well, if someone crosses something off their list after they finish it then we know how productive they were relative to the schedule and in what part of the day. This gives some means of editing their productivity vector.

3. User lists tasks, schedule gets complied and then they add another task midway through the day. Should the app now reschedule the day to account for this new task? Or should it leave things as they are and save this task for another time (assuming it's not due the day of)? Perhaps we leave this up to the user. We could ask them if they want to recompile the rest of the day given this change or if they would like to keep their current schedule.

4. Cross off and re-adding a task. If someone accidentally removes a task from the list then the system will think they did it, even if they didn't. We could solve this by having a check condition that sees if the same task has just been put back up. If so, disregard this as a completion.

5. The user could underestimate how long things will take. This makes the algorithm think they didn't finish things because they weren't working well when in reality they just got their estimation wrong. App should notify user if they are behind and give them the option to re-arrange their schedule. This should be triggered if user opens their list and doesn't make any changes even after they were supposed to have gotten things done.

6. Tasks can be broken up into smaller pieces. How do we handle this?

7. People can't predict how long things will take.

8. Working while eating.



Rishi's Brain Dump (it's formatted better on the Google Doc):
We create a 48x5 matrix (48 rows for each ½ hour in the day, 5 columns for each category), and each cell will correspond to a [0,1) “productivity index” (PI) that indicates how productive the user is likely to be for the corresponding category at the corresponding time
PI = 0 at times where user cannot work (sleep, meal, pre-planned event, etc), and some buffer around times when they cannot work (to account for sleeping in, eating longer than expected, travel time, or whatever)
The PI of each cell will be calculated based on a number of factors:
Proximity to predetermined “busy times” (sleep, meal, etc) → closer to busy time = lower PI (bc of chance of falling behind during the busy time, like sleeping in)
Relationship btw distance to busy time (number of slots from current to nearest busy time slot) and probability of spillover needs to be determined but I’d guess there’s a roughly-exponential dropoff
Exponential dropoff meaning that if we were to graph 1 - PI (an “unproductivity index”) vs. distance to nearest busy time, then it would probably look somewhat like a y=x^3
Survey results
Research on productivity (quantifiable metrics that our model can reasonably measure that make people more/less productive)
User history (how they have done in the past at that time slot for each category)
A little bit of randomness (our model will by no means be accurate at the start—and even as we go forward—so we need some way to get sufficient variation in our predictions for more data towards unsupervised learning)
Probably other stuff I’m forgetting
The model will then give each task a “priority rating” (PR) based on (in rough order of most to least influence):
Task priority assigned by user (if they gave that task)
Maybe: importance of associated category (if this is something we can/want to measure)
Immediacy (more immediate due date = higher PR)
Duration (longer expected time for completion = higher PR)
Likelihood of efficiency for each task (calculated based on excitement for that task, if set by user, and user’s history based on related tasks; defaults to average if none of these metrics are available)
Possibly some degree of randomness (not a lot, but enough to promote sufficient variation in the predictions the model outputs, and more variation = more data to train the model in unsupervised learning)
This is also a good idea under the assumption that our model’s prediction will be close to correct, but somewhat off, therefore randomness will give a ~50-50 shot of getting closer to the correct prediction
Maybe other stuff
Generally, for each of the 30-minute time slots, there will be a “winning” category, i.e. the category with the highest PI
If all PIs = 0, then this slot is reserved for no work
If all PIs are low (threshold TBD), then this slot should maybe be reserved for a break
Also, if there’s too many consecutive slots reserved for work, the slot with the lowest PI associated to the winning category should be reserved for a break (e.g. if there’s a string of 5 hours with winning categories having a PI > .8, then there must be 1 ½ hour break which should be chosen based on 2 criteria: closest to the middle of the interval and lowest winning category PI)
Similarly, if the user specified how many ½ hours they would like to work (either overall or for specific categories), then after we compile the full schedule we need to make sure we haven’t exceeded these limits (again, for each individual category or the schedule as a whole, depending on what the user entered)
Winning (scheduled) tasks with lowest associated PR will be reserved as buffer time (meaning we’ll suggest tasks that can be completed in priority order, but the user can do whatever they want with that time, including not work)
Maybe do this as we’re compiling the schedule, but then the model may remove more work time from the end of the day after beginning-of-the-day tasks are already scheduled, even if the user would have been more productive at night
The algorithm will assess which task within the winning category should be scheduled for this slot based on:
Tasks’ PR
Last time each task was scheduled/performed (don’t want to be doing the same task 3 distinct times within like 2 hours)
Other stuff outside of the PR metric that is dependent on the specific time slot (i.e. not generalizable to the task as a whole)
Maybe other stuff??
Apart from the buffer time scheduled around the user’s “busy times,” we can set buffer times throughout the day (mainly additional buffers around the busy times) during which we suggest that the user works (and we can maybe even give them a suggested priority list of tasks to do during each buffer or during buffers as a whole). However, we won’t schedule specific tasks during these times because…
It’ll make the algo more accurate (the less times we have to predict, the more accurate we can be)
It’ll help account for the user falling behind schedule (if they fall behind, they use the buffers to catch up, otherwise they do more work or take a break during the buffer if they feel that’s necessary)
In terms of how the algo does this, I’m thinking:
The main NN (neural net) will compute the PI matrix
A separate NN will compute the priority orderings of tasks within each category
Finally, we could probably use a simpler ML model (regression or simple classification, like SVM, KNN, or whatever, depending on how this all works out during implementation) to compute the final schedule (i.e. scheduling specific tasks during each time slot) given the results of the NNs
