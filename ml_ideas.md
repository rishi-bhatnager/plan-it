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