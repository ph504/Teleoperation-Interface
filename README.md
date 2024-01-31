# Social Teleoperation Interface
Our main goal was
to find out whether adding social elements to an interface would increase trust in a teleoperation (remote control of a robot from a distance) system. More information about the methodology, research goals and task design is explained in my master's thesis.



<p align="center">
    <img src="https://github.com/PouyaJigsaw/teleop-interface/assets/33330581/b231f326-f8bd-4cff-8c81-9c21d73edf17" alt="Image 1" width="320", height="320"/>
    <img src="https://github.com/PouyaJigsaw/teleop-interface/assets/33330581/1225a286-ca2d-457b-a927-b36c6d9d6822" alt="Image 2" width="320", height="320"/>
</p>



## Setup
To create a teleoperation system, I used Robot Operating System (ROS) to program a robot called Jackal. 
We connected our robot to a PC and dualshock4 controller, each of them considered a node,using message-passing system of ROS written with python language. 
The controller passes commands to robot [2], and the robot sends camera data to PC [3].



## Dialogue System (Model-View-Controller)
Just like conventional dialogue-driven video games that shows a dialogue box and an avatar, I
implemented a dialogue system called Avalogue that follows the Model-Control-View (MVC)
pattern.

The model is basically two spreadsheets (instead of database) that contains information related to
each dialogue object [5], and each sprite of animations such as talking, sad or happy face, etc.[6] .
The dialogue is shown word by word, accompanied by a brief sound to mimic old dialogue driven
games (e.g., Star Fox 64). Unlike video games, since our system was real-time, the agent had to
react to different events while talking, so my main challenge was to pause the middle of the agent’s
dialogue, enable the agent to react to the event, and then continue the conversation; something that
is not common in other conventional dialogue systems. 
To fix this, I created a Control class called Avalogue [6], a composition of dialogue [7] and avatar [8]
class I implemented before, with a deque [9] that contains each Avalogue object. By using Update
loop pattern in the Avalogue class (or Control), new events, which creates new Avalogues, will be
at the top of the stack, and then data will be sent to dialogue View[10] and avatar View[11].I tried to
use semaphores to control the flow of dialogues (since each dialogue could be considered a thread)
before switching to this solution [12].

## Experiment Design
To create our social interface, we created a social agent using human-like language and simple
avatar with animations in comparison to a conventional machine-like terminal. Both represents the
AI (or Agent) that is embedded into the robot and communicates with the user who controls the robot.
We had to create a narrative where: (a) trust forms between user and agent (trust formation), (b)
the agent breaks trust by performing badly (trust violation), (c) the agent asks the user about
delegating tasks to itself in the future. All of these had to happen in a rigid narrative, like
Uncharted, or Call of Duty (single player) where the game is linear, so each person experiences
the same narrative regardless of their performance. I used State Pattern to control each part of the
experiment [13].

![image](https://github.com/PouyaJigsaw/teleop-interface/assets/33330581/642a8349-ad64-4dfc-b667-8e67cb9a2b82)


## Technical Aspects
For other features, I used other behavioral patterns such as Singleton [14] and Observer [15]. Using
baseCanvas as a parent class for numerous UI Elements helped me to re-position or re-size each
element in general[16]. I wrote a Shell script which automated the start of each experiment (giving
arguments, opening different scripts, etc.)[17]. I also had to do socket programming to send
messages from my personal laptop to PC, to control parts of the experiment[18]. Version Controlling
using git saved my life, as I added new features (each in its own branch) which broke the system,
so I had to revert to main branch [19].

## Lessons Learned
Making this system single-handedly was a difficult but rewarding experience. Writing
5,000 lines of code with numerous components, while acting simultaneously, made me learn a lot
of Software Engineering concepts. If I had to redo it again, I would not use State Pattern and would
make the system stateless (e.g., using Update loop instead) since for debugging each state, I had
to go through each state one by one to reach the one I wanted. I wish I refactored my code more
(something like a refactor day) and made it easier to debug; at the end of the project the debugging
process was frustrating. Each new feature broke another thing, where I realized the mental toll of
technical debt. But overall, I am proud of this project.
