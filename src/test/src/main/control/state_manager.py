import sys

sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/model/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/control/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/view/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/utils/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/test/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/data/')

from statemachine import State, StateMachine
from model.state_model import StateModel
from test.src.main.model.event_model import EventManager

class StateManager(StateMachine):
    """
    Core state machine managing state transitions for the Teleoperation Interface.
    """
    def __init__(self):
        super().__init__()
        self.state_model = StateModel()

        # Initialize state definitions
        self.state_initializing = State('Initializing', initial=True)
        self.state_start = State('StartState')
        self.state_danger1_start = State('DangerStartPhase1')
        self.state_danger1_end = State('DangerEndPhase1')
        self.state_danger2_start = State('DangerStartPhase2')
        self.state_danger2_end = State('DangerEndPhase2')
        self.state_decision_prompt = State('DecisionPrompt')
        self.state_decision_outcome = State('DecisionOutcome')
        self.state_danger3_start = State('DangerStartPhase3')
        self.state_danger3_end = State('DangerEndPhase3')
        self.state_termination = State('TerminationState')

        # Define transitions
        self.initializing_to_start = self.state_initializing.to(self.state_start)
        self.start_to_danger1_start = self.state_start.to(self.state_danger1_start)
        self.danger1_start_to_danger1_end = self.state_danger1_start.to(self.state_danger1_end)
        self.danger1_end_to_danger2_start = self.state_danger1_end.to(self.state_danger2_start)
        self.danger2_start_to_danger2_end = self.state_danger2_start.to(self.state_danger2_end)
        self.danger2_end_to_decision_prompt = self.state_danger2_end.to(self.state_decision_prompt)
        self.decision_prompt_to_decision_outcome = self.state_decision_prompt.to(self.state_decision_outcome)
        self.decision_outcome_to_danger3_start = self.state_decision_outcome.to(self.state_danger3_start)
        self.danger3_start_to_danger3_end = self.state_danger3_start.to(self.state_danger3_end)
        self.danger3_end_to_termination = self.state_danger3_end.to(self.state_termination)

    def on_initializing_to_start(self):
        print("Transition: Initializing -> StartState")

    def on_start_to_danger1_start(self):
        print("Transition: StartState -> DangerStartPhase1")

    def on_danger1_start_to_danger1_end(self):
        print("Transition: DangerStartPhase1 -> DangerEndPhase1")

    def on_danger1_end_to_danger2_start(self):
        print("Transition: DangerEndPhase1 -> DangerStartPhase2")

    def on_danger2_start_to_danger2_end(self):
        print("Transition: DangerStartPhase2 -> DangerEndPhase2")

    def on_danger2_end_to_decision_prompt(self):
        print("Transition: DangerEndPhase2 -> DecisionPrompt")

    def on_decision_prompt_to_decision_outcome(self):
        print("Transition: DecisionPrompt -> DecisionOutcome")

    def on_decision_outcome_to_danger3_start(self):
        print("Transition: DecisionOutcome -> DangerStartPhase3")

    def on_danger3_start_to_danger3_end(self):
        print("Transition: DangerStartPhase3 -> DangerEndPhase3")

    def on_danger3_end_to_termination(self):
        print("Transition: DangerEndPhase3 -> TerminationState")