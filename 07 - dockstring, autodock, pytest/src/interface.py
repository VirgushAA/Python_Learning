import json
import inquirer
import random
import os
from colorama import init as colorama_init, Style, Fore
from analysis import Analyzer

colorama_init()


def validate_respiration(_, number):
    """
    Validate user input for respiration rate.

    :param _: Unused parameter (required by inquirer validation).
    :type _: Any
    :param number: User input for respiration rate.
    :type number: str
    :raises inquirer.errors.ValidationError: If the input is not a positive integer.
    :return: True if the input is valid.
    :rtype: bool
    """

    if not number.isdigit():
        raise inquirer.errors.ValidationError("", reason="Respiration must be a positive integer!")
    return True


def validate_heart_rate(_, number):
    """
    Validate user input for heart beat rate.

    :param _: Unused parameter (required by inquirer validation).
    :type _: Any
    :param number: User input for heart beat rate.
    :type number: str
    :raises inquirer.errors.ValidationError: If the input is not a positive integer.
    :return: True if the input is valid.
    :rtype: bool
    """

    if not number.isdigit():
        raise inquirer.errors.ValidationError("", reason="Heart rate must be a positive integer!")
    return True


def validate_blushing(_, number):
    """
    Validate user input for blushing level.

    :param _: Unused parameter (required by inquirer validation).
    :type _: Any
    :param number: User input for blushing level.
    :type number: str
    :raises inquirer.errors.ValidationError: If the input is not in bounds of 1 and 6.
    :return: True if the input is valid.
    :rtype: bool
    """

    if not number.isdigit() or int(number) > 6:
        raise inquirer.errors.ValidationError("", reason="Blushing level must be between 1 and 6!")
    return True


def validate_pupillary(_, number):
    """
    Validate user input for pupillary dilation.

    :param _: Unused parameter (required by inquirer validation).
    :type _: Any
    :param number: User input for pupillary dilation.
    :type number: str
    :raises inquirer.errors.ValidationError: If the input is not in bounds of 2 and 8.
    :return: True if the input is valid.
    :rtype: bool
    """

    if not number.isdigit() or not (2 <= int(number) <= 8):
        raise inquirer.errors.ValidationError("", reason="Pupillary dilation must be between 2 and 8 mm!")
    return True


def failure_text(text):
    """
    Color output text for very unexpected case, where test subject nether human nor replicant.
    :param text: Output string to color.
    :return: None
    """

    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    return "".join(random.choice(colors) + char for char in text) + Style.RESET_ALL


def start_test(path: str = 'questions/questions.json'):
    """
    Simulate the Voight-Kampff test to determine if a subject is human or a replicant.

    :param path: Path to the JSON file containing test questions.
    :type path: str
    :raises FileNotFoundError: If the question file is missing.
    :raises json.JSONDecodeError: If the question file is empty or malformed.
    :return: None
    """

    if not os.path.exists(path):
        print('File with questions not found.')
        return None

    if os.stat(path).st_size == 0:
        print('File with questions is empty.')
        return None

    try:
        with open(path, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print('File with questions is not valid JSON.')
        return

    a = Analyzer()

    for q in data:
        question = [
            inquirer.questions.List(
                name=q,
                message=q,
                choices=data[q]
            )
        ]
        answer = inquirer.prompt(question)
        questions = [
            inquirer.Text('Respiration', message="What's your respiration?", validate=validate_respiration),
            inquirer.Text('Rate', message="What's your heart rate?", validate=validate_heart_rate),
            inquirer.Text('Level', message="What's your blushing level", validate=validate_blushing),
            inquirer.Text('Dilation', message="What's your pupillary dilation", validate=validate_pupillary)
        ]
        answers = inquirer.prompt(questions)
        a.add_measurements(answers)
    decision = a.decision()
    if decision == 'палюбому человек aga':
        print(f"{Fore.GREEN}You're {decision}{Style.RESET_ALL}")
    elif decision == 'уже не человек sadding':
        print(f"{Fore.RED}You're {decision}{Style.RESET_ALL}")
    else:
        print(failure_text("Что ты такое?"))
