import statistics


class Analyzer:
    """
    Analyzes physiological indicators (respiration, heart rate, blushing level, and pupillary dilation)
    to determine if a test subject is human or a replicant.

    :ivar respiration: A list of recorded respiration values.
    :vartype respiration: list[int]
    :ivar heart_rate: A list of recorded heart rate values.
    :vartype heart_rate: list[int]
    :ivar blushing_level: A list of recorded blushing level values.
    :vartype blushing_level: list[int]
    :ivar pupillary_dilation: A list of recorded pupillary dilation values.
    :vartype pupillary_dilation: list[int]
    """

    respiration: list[int]
    heart_rate: list[int]
    blushing_level: list[int]
    pupillary_dilation: list[int]

    def __init__(self):
        self.respiration = []
        self.heart_rate = []
        self.blushing_level = []
        self.pupillary_dilation = []

    def add_measurements(self, res):
        """
        Add physiological measurements to the analyzer.

        :param res: A dictionary containing the latest physiological measurements.
        :type res: dict[str, int]
        :raises ValueError: If any measurement is missing or not convertible to an integer.
        :return: None
        """
        try:
            self.respiration.append(int(res['Respiration']))
            self.heart_rate.append(int(res['Rate']))
            self.blushing_level.append(int(res['Level']))
            self.pupillary_dilation.append(int(res['Dilation']))
        except ValueError as e:
            print(f'Measurements are not viable: {e}')
            raise ValueError(e)

    def check_respiration(self):
        """
        Checks list of respiration measures.

        :return: True if mean of list is more or equal than 12 and less or equal than 16.
        :rtype: bool
        """

        return 12 <= statistics.median(self.respiration) <= 16

    def check_heart_rate(self):
        """
        Checks list of heart rate measures.

        :return: True if mean of list is more or equal than 60 and less or equal than 100.
        :rtype: bool
        """

        return 60 <= statistics.median(self.heart_rate) <= 100

    def check_blushing_level(self):
        """
        Checks list of blushing level measures.

        :return: True if mean of list is less or equal than 5.
        :rtype: bool
        """

        return statistics.median(self.blushing_level) <= 5

    def check_pupillary_dilation(self):
        """
        Checks list of heart pupillary dilation measures.

        :return: True if mean of list is more or equal than 2 and less or equal than 8.
        :rtype: bool
        """

        return 2 <= statistics.median(self.pupillary_dilation) <= 8

    def decision(self):
        """
        Determine whether the test subject is human or a replicant based on the recorded physiological measurements.

        :return: A string indicating whether the subject is human or a replicant.
        :rtype: str
        """
        return 'палюбому человек aga' if (self.check_respiration()
                                               and self.check_heart_rate()
                                               and self.check_blushing_level()
                                               and self.check_pupillary_dilation()) \
            else 'уже не человек sadding'
