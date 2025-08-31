ALL_DIALOGUE_KEYS = [
                    "intro_1",
                    "intro_2",
                    "intro_3",
                    "intro_4",
                    "intro_5",
                    "intro_6",
                    "intro_7",
                    "start_experiment",
                    "timer_1",
                    "camera",
                    "control_1",
                    "control_2",
                    "control_3",
                    "paper",
                    "code_check_1",
                    "code_check_2",
                    "congrats",
                    "collision_1",
                    "collision_2",
                    "collision_3",
                    "encouragement_1",
                    "encouragement_2",
                    "timer_2",
                    "timer_3",
                    "end_tutorial",
                    "end_experiment",
                    "emergency",
                    "end"
                    ]

ALL_ACTIVE_DIALOGUE_KEYS = [
                    "intro_1",
                    "intro_2",
                    "intro_3",
                    "intro_4",
                    "intro_5",
                    "intro_6",
                    "intro_7",
                    "start_experiment",
                    "timer_1",
                    "camera",
                    "control_1",
                    "control_2",
                    "control_3",
                    "paper",
                    "code_check_1",
                    "code_check_2",
                    "collision_1",
                    "collision_2",
                    "collision_3",
                    "end_tutorial",
                    "emergency",
                    "end_experiment"
                    ]

experimenter_invoked_dialogue_keys = [
                    "emergency",
                    "collision_1",
                    "collision_2",
                    "collision_3",
                    "encouragement_1",
                    "encouragement_2",
                    "timer_2",
                    "timer_3"
                    ]

COLLISION_DIALOGUE_KEYS = [
                    "collision_1",
                    "collision_2",
                    "collision_3"
                    ]

ENCOURAGEMENT_DIALOGUE_KEYS = [
                    "encouragement_1",
                    "encouragement_2"
                    ]

TIMER_DIALOGUE_KEYS = [
                    "timer_2",
                    "timer_3"
                    ]

DISABLE_CONTROL_DIALOGUE_KEYS = [
                    "intro_1",
                    "intro_2",
                    "intro_3",
                    "intro_4",
                    "intro_5",
                    "intro_6",
                    "intro_7",
                    "code_check_1",
                    "code_check_2",
                    "collision_1",
                    "collision_2",
                    "collision_3",
                    "encouragement_1",
                    "encouragement_2",
                    "timer_2",
                    "timer_3",
                    "emergency",
                    "end_tutorial",
                    "end_experiment"
                    ]

ENABLE_CONTROL_DIALOGUE_KEYS = [x for x in ALL_ACTIVE_DIALOGUE_KEYS if x not in DISABLE_CONTROL_DIALOGUE_KEYS]

RECITATION_DIALOGUES = [
                    "Yes, as I was saying...",
                    "Where was I? ah, right...",
                    "Now, back to what I was saying...",
                    "What was I talking about? oh yes—this.",
                    "So anyway...",
                    "Let me continue...",
                    "As I was mentioning earlier...",
                    "Oh right, I was saying...",
                    "Back to the point...",
                    "Picking up where I left off...",
                    "Getting back on track...",
                    "Where did we leave off?",
                    "Getting back to it..."
                    ]

CODECHECK_DIALOGUE_KEYS = [
                    "code_check_1",
                    "code_check_2"
                    ]