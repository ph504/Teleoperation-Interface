
## Events

| Event | Values | Explanation |
| ----- | :-----: | --------------- |
| task_advance | 1 to 13 | the time when the user scan's the  X'th code by  X being the value of the event |
| thrshldpsscntdngrttl_nrml |  X | The time when the blue bar ( in normal state) passed the threshold  X'th times by  X being the value of the event|
| thrshldpsscntttl_dngr |  X | The time when the green bar ( in critical state) passed the threshold  X'th times by  X being the value of the event|
| danger_zone_start | Enum: ai_handler, operator_handler | The time when the danger zone happens and the mode is either manual (operator_handler) or assisted (ai_handler)|
| stppsscount_dngr |  X| The time when the green bar (critical state) passed the threshold, is red, and it is step-by-step going forward as a red bar with  X being the number of steps after threshold the bar has went forward|
| ai_incorrectlogging |  X | The time when the Agent makes a mistake (passing the threshold) with  X being number of times they did mistake [it is obselete because of "thrshldpsscntdngrttl_nrml"]|
| ai_correctlogging |  X | The time when the agent is successful at logging correctly X times   |
| wrong_entry |  N/A | The time when the user writes the wrong code |
| duplicated_entry |  N/A | The time when the user writes a duplicated code |
| danger_zone_end | Enum: ai_handler, operator_handler | The time when the critical state ends  |
| CHOICE | Enum: YES, NO | The decision of the user in choosing between assisted mode (YES) and manual mode (NO) |
| collision | X | Time when collision happened with  X being the number of times it happened |
| stppsscount_nrml |  X | The time when the blue bar (normal state) passed the threshold, is red, and it is step-by-step going forward as a red bar with X being the number of steps after threshold the bar has went forward | 
| end |  N/A | The end of experiment |
