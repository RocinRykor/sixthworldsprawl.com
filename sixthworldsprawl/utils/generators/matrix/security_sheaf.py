from typing import Dict

from sixthworldsprawl.utils.constants import matrix_constants as matrix
from sixthworldsprawl.utils.rollers.dice_roller import basic_roll


def roll_trigger_step(system_security_level: int) -> int:
    """
    The roll_trigger_step function takes the system security level (Blue, Green, Orange, Red) and converts it to a modifier and rolls 1d3 as a base-step.
    It then adds the modifier to the base step
    The function returns an integer representing the trigger step.

    :param system_security_level:int: Determine the modifier for the base step
    :return: A number based on the system security level
    :doc-author: Rocin
    """
    base_step = sum(basic_roll(1, 3))

    switch = {
        0: base_step + 4,
        1: base_step + 3,
        2: base_step + 2,
        3: base_step + 1
    }
    return switch.get(system_security_level, "Invalid Number")


def print_ic_list(ic_list):
    string = ""
    if ic_list:
        if len(ic_list) > 1:
            for ic_program in ic_list:
                string += f"{ic_program}\n"
            return string
        else:
            return ic_list[0]
    else:
        return None


class SheafEvent:
    """
    The Sheaf Event is the description of any IC that is generated for a particular tally threshold
    It will also denote any change in status to the alert level of the system
    """

    def __init__(self, current_step: int):
        self.current_step = current_step
        self.title = ""
        self.ic_list = []
        self.is_construct = False
        self.is_party_cluster = False

    def __str__(self):
        if self.ic_list:
            return f"{self.current_step}: {print_ic_list(self.ic_list)}"
        else:
            return f"{self.current_step}: {self.title}"


class AlertContainer:
    def __init__(self, ic_level="", ic_category=None, is_alert_step=False):
        self.ic_level = ic_level
        self.ic_category = ic_category
        self.is_alert_step = is_alert_step

    def __str__(self):
        if self.ic_level == matrix.BLACK:
            return f"{matrix.BLACK} IC"
        else:
            return f"{self.ic_category}-{self.ic_level} IC"

    def roll_alert_table(self, system_alert_level: int, steps_since_last_alert: int,
                         limit_to_ic_generation: bool = False):
        """
        The roll_alert_table function is used to determine what alerts are generated by the system or if there is a change is System Alert Level
        It takes three arguments:
            1) The current alert level of the system (0, 1, or 2). This determines what type of IC can be generated
            2) The number of steps since the last alert was generated for this system. This value is added to any roll results and then compared against a list of possible results that can occur when rolling an Alert Table in SR5 (see matrix_constants file).
            3) A boolean to indicate whether the steps_since_last_alert will be added to the roll, if it is not added, triggering an alert step is not possible and IC will be generated

            If the final results are high enough to trigger an alert step, no IC is generated at the time.

        :param system_alert_level:int: Determine which alert level to use for the current step
        :param steps_since_last_alert:int: Track the number of steps since the last alert was triggered
        :param limit_to_ic_generation:bool: Limit the alert table to only those that are used for generating IC
        :return: AlertContainer containing information on IC Level and Category or if an alert step has been triggerd
        :doc-author: Rocin
        """
        roll_result = sum(basic_roll())

        final_results = roll_result if limit_to_ic_generation else roll_result + steps_since_last_alert

        # print(f"Final Results: {final_results}")

        if system_alert_level == 0:
            if final_results in [1, 2, 3]:
                self.add_ic(matrix.WHITE, matrix.REACTIVE)
            elif final_results in [4, 5]:
                self.add_ic(matrix.WHITE, matrix.PROACTIVE)
            elif final_results in [6, 7]:
                self.add_ic(matrix.GRAY, matrix.REACTIVE)
            else:
                self.is_alert_step = True
        elif system_alert_level == 1:
            if final_results in [1, 2, 3]:
                self.add_ic(matrix.WHITE, matrix.PROACTIVE)
            elif final_results in [4, 5]:
                self.add_ic(matrix.GRAY, matrix.REACTIVE)
            elif final_results in [6, 7]:
                self.add_ic(matrix.GRAY, matrix.PROACTIVE)
            else:
                self.is_alert_step = True
        else:
            if final_results in [1, 2, 3]:
                self.add_ic(matrix.GRAY, matrix.PROACTIVE)
            elif final_results in [4, 5]:
                self.add_ic(matrix.WHITE, matrix.PROACTIVE)
            elif final_results in [6, 7]:
                self.add_ic(matrix.BLACK)
            else:
                self.is_alert_step = True

        return self

    def add_ic(self, ic_level: str, ic_category: str = None):
        """
        The add_ic function sets the level code (color) and category (Reactive, or Proactive) for an IC

        :param self: Refer to the object itself
        :param ic_level:str: Level Code (White, Gray, Black) for an IC
        :param ic_category:str: Category (Reactive or Proactive) of an IC
        :doc-author: Rocin
        """
        self.ic_level = ic_level
        self.ic_category = ic_category


def generate_sheaf(system_security_level: int, system_security_rating: int) -> list[SheafEvent]:
    alert_level_table: Dict[int, str] = {
        0: matrix.NO_ALERT,
        1: matrix.PASSIVE_ALERT,
        2: matrix.ACTIVE_ALERT,
        3: matrix.SHUTDOWN
    }

    # Initialize Variables
    system_alert_level = 0  # Starts at No Alert
    steps_since_last_alert = 0
    current_step = 0
    # Loop Fail Safe
    max_steps = 100

    sheaf_step_list = []

    # Loop until system reaches Shutdown Status or hits fail-safe limit
    while system_alert_level < 3 and current_step < max_steps:
        # Step 1: Calculate next Trigger Step
        current_step += roll_trigger_step(system_security_level)
        print(f"Current Step: {current_step}")

        # Step 2: Generate a Sheaf Event for the current step
        sheaf_event = SheafEvent(current_step)

        # Step 3: Determine if the Alert Status of the system is changing or if the system is generating IC, packaged in an AlertContainer
        alert_container = AlertContainer().roll_alert_table(system_alert_level, steps_since_last_alert)

        # Step 4: Process The AlertContainer to check for changes in System Alert Level
        if alert_container.is_alert_step:  # Sheaf Step has triggered a change in the Alert Level
            steps_since_last_alert = 0
            system_alert_level += 1

            sheaf_event.title = alert_level_table[system_alert_level]

            print(f"Alert Status: {alert_level_table[system_alert_level]}")

            # If the Host is Blue or Green (Level Code 0 or 1), or it has reached Shutdown, it won't generate IC on an alert step and can continue
            # Otherwise, re-roll the alert table and force generation of IC alongside the alert level
            if not (system_alert_level <= 1 or system_alert_level == 3):
                alert_container.roll_alert_table(system_alert_level, steps_since_last_alert, True)
        else:
            steps_since_last_alert += 1

        # Step 5: Generate IC and add to list for Sheaf Event
        if alert_container.ic_level:
            ic_program = ICProgram(alert_container.ic_level, alert_container.ic_category).process_ic(
                system_security_rating)

            sheaf_event.ic_list.append(ic_program)

            print(ic_program)

        sheaf_step_list.append(sheaf_event)

        # Fail-safe and Debug
        current_step += 1

    print("Complete!\n\n")
    return sheaf_step_list
