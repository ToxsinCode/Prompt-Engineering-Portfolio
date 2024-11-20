### Note: Before we begin, I would like to highlight that this task has presented considerable challenges for some models, particularly Gemini. These models have struggled with the calculations and memory management necessary to accurately determine when simulated characters earn an extra turn. I took this into account during the process.
--------

**You:**

Are you good at suggesting, editing and fixing code?

--------

**Copilot:**

You bet. From debugging to optimizing, I’ve got your coding conundrums covered. What are we tackling today? Let's dive in.

--------

**You:**

Well first lets make sure we're on the same page before we start coding. I'm making a combat system for my RPG. The turn order system will be broken up into cycles that have a length equivalent to 100 Action Points. For characters to act during a cycle, they will have to have a Total Action Points Value equal or greater than the Cycle Length. As a result, these are the variables for the formula (and eventually the code): 
Cycle Length = 100 
Minimum Action Threshold = 100
Total Action Points = Leftover Action Points + Speed
Raw Actions Per Cycle = Total Action Points / Cycle Length
True Actions Per Cycle = (The integer of Raw Actions Per Cycle)
Leftover Actions Per Cycle = (The decimal of Raw Actions Per Cycle)
Leftover Action Points = Leftover Actions * Cycle Length
Does this make sense to you?

--------

**Copilot**

Yeah, I got it. Looks like you’ve got a solid plan! Your variables and formulas make sense. So, Total Action Points are calculated by adding Leftover Action Points from the previous cycle to Speed, then dividing by the Cycle Length gives you Raw Actions Per Cycle. The integer part is True Actions Per Cycle and the decimal part is Leftover Actions Per Cycle, which you then convert to Leftover Action Points for the next round. Nice work keeping it organized.

Ready to dive into the coding bit?

--------

**You**

Not quite yet. Lets simulate combat from Character B. Lets assume they have a speed of 150 and start with no leftover action points. How many actions will they take Cycle 1?

--------

**Copilot**

Alright, let’s run through this again with Character B’s speed.

Character B’s speed: 150 Starting Leftover Action Points: 0

So, Total Action Points for Cycle 1 = Leftover Action Points + Speed = 0 + 150 = 150

Next, calculating Raw Actions Per Cycle:

Raw Actions Per Cycle = Total Action Points / Cycle Length = 150 / 100 = 1.5

Breaking it down: True Actions Per Cycle (the integer part) = 1 Leftover Actions Per Cycle (the decimal part) = 0.5

So in Cycle 1, Character B will take 1 action and have 0.5 leftover actions (50 leftover action points) to carry into the next cycle. Ready to see how this plays out in code?

--------

**You**
