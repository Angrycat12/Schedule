import settings
import numpy as np
import random
import math
import FileManager

from functools import cache


class Subject:
    def __init__(self,
                 name: str,
                 hours: int,
                 lesson_number_limitation: list = [],
                 difficult: bool = False,
                 test: dict = None):
        self.name = name
        self.hours = hours
        self.difficult = difficult
        self.MandatoryTests = test
        self.lesson_number_limitation = lesson_number_limitation


class Teacher:
    def __init__(self, first_name: str, last_name: str, subject):
        self.first_name = first_name
        self.last_name = last_name
        self.subject = subject


class Group:
    def __init__(self, name: str, subjects: list[Subject]):
        self.name = name
        self.subjects = subjects


subjectsf: dict[str, list[int | bool]] = {'Math': [60, True],
                                          'PI': [20, False],
                                          'English': [70, True],
                                          'Russian': [10, False],
                                          'Belarusian': [50, False],
                                          'Physic': [60, True],
                                          'Biology': [50, False],
                                          'Chemistry': [60, True],
                                          'Geograpy': [50, False]}


@cache
def subjects() -> list[Subject]:
    """
    :return: list of subject
    """
    subject_list: list = []
    for subject_name in subjectsf.keys():
        subject_options: list = subjectsf[subject_name]  # 0-hours, 1-difficult
        subject_list.append(Subject(name=subject_name, hours=subject_options[0], difficult=subject_options[1]))
    return subject_list


def generate(seed: int = 0, school_week: int = 10,
             max_nld: int = 1, min_nld: int = 1,
             group_list: list[str] = None) -> dict[int, list[list[str]]]:
    """
    The function generate schedule for one group.
    :param group_list:
    :param seed: serves to clarify the generation: 0 - by the hour
                                               1 - the first week is random, and after by the hour
                                               others - by numbers the first week, and after by the hour
    :param school_week: number of school days
    :param max_nld: maximum number of lessons per day
    :param min_nld: minimum number of lessons per day
    :return: dictionary with a schedule where the key is the week,
            and value dictionary with key day, and value is the schedule itself
    """

    if group_list is None:
        group_list = ['test']

    subject: Subject
    subject_schedule_l: list[str] = []
    subject_schedule_d: list[list[str]] = []
    subject_schedule: dict[int, list[list[str]]] = {}
    long_subject: Subject = Subject(name="Test", hours=0, difficult=False)
    all_hours: int = 0
    max_lesson_d: int = 9
    seed_l: list[int] = []
    previous_subject: str = 'None'
    group = Group(name='Test', subjects=subjects())
    groups: list[Group] = [group]

    if seed == 1:
        # generating numbers the size of the number of lessons per day
        seed = random.randint(10 ** max_lesson_d, 10 ** (max_lesson_d + 1) - 1)
        seed_l = list(map(int, str(seed)))
    elif seed > 1:
        if 10 ** max_lesson_d < seed:
            if seed < 10 ** (max_lesson_d + 1) - 1:
                seed_l = list(map(int, str(seed)))
            else:
                seed_l = list(map(int, str(seed)))
                seed = seed / (10 ** (len(seed_l) - max_lesson_d))  # сделать через div
        else:
            seed = seed * (10 ** (max_lesson_d - len(list(map(int, str(seed))))))
            seed_l = list(map(int, str(seed)))

    for week in range(school_week):
        print(f'week: {week}')

        for day in range(5):
            print(f'day: {day}')

            for group in groups:
                print(f'group: {group.name}')

                for lesson in range(max_lesson_d):
                    print(f'lesson: {lesson}')

                    long_subject = group.subjects[0]

                    for subject in group.subjects:
                        print(f'subject: {subject.name}')
                        print(f'{subject.hours}')

                        if subject.hours > 0:
                            if lesson == 0:
                                if subject.difficult == False:
                                    if subject.hours > long_subject.hours and subject.name != previous_subject:
                                        long_subject = subject
                            else:
                                if subject.hours > long_subject.hours and subject.name != previous_subject:
                                    long_subject = subject
                        else:
                            group.subjects.remove(subject)

                    if len(group.subjects) == 0:    #кастыль
                        group.subjects.append(Subject(name='None', hours=1000))

                    if long_subject.name != previous_subject:
                        previous_subject = long_subject.name

                    elif long_subject.name == 'None':   #часть костыля
                        previous_subject = long_subject.name

                    else:
                        long_subject = group.subjects[random.randint(0, len(group.subjects)-1)]
                        previous_subject = long_subject.name

                    print(f'Subject in this lesson: {long_subject.name}')

                    group.subjects.remove(long_subject)
                    long_subject.hours -= 1
                    group.subjects.append(long_subject)

                    subject_schedule_l.append(long_subject.name)

                # subject_schedule_g[group] = subject_schedule_l
                # subject_schedule_l = []

            subject_schedule_d.append(subject_schedule_l)   # subject_schedule_g
            # subject_schedule_g = {}
            subject_schedule_l = []

        subject_schedule[week] = subject_schedule_d
        subject_schedule_d = []

    return subject_schedule


if __name__ == '__main__':
    def main() -> None:
        #seed = int(input())
        print(generate())

    main()  # 1- доделать генерацию 2- добавить работу max_nld и min_nld
