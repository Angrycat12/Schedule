import settings
import numpy as np
import random
import math

from functools import cache


class Subject:
    """
    Serves for convenient management of educational subjects.
    """
    def __init__(self,
                 name: str,
                 hours: int,
                 difficult: bool = False,
                 test: dict = None):
        self.name = name
        self.hours = hours
        self.difficult = difficult
        self.MandatoryTests = test


class FileManager:
    """
    Serves for convenient management of schedule file.
    """
    def __init__(self, file_name: str = settings.STANDART_NAME_SUBJECTFILE, mode: str = 'r'):
        self.file_name = file_name
        self.mode = mode
        pass

    def __enter__(self):
        if self.mode == 'r':
            self.file = open(file=self.file_name, mode=self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
            pass


def RFS_txt(file_name: str) -> dict[str, list[int | bool]]:  # RFS - read file subjects
    """
    Reads a file subjects in .txt format.
    :param file_name: name the file
    :return: dictionary where the key is the name of the lesson, and the value is the parameters of this lesson
    """
    subjects_d: dict = {}
    with FileManager(file_name) as SubjectFile:
        try:
            SubjectFile.read()
            for word in SubjectFile:
                pass
        finally:
            SubjectFile.close()
    return subjects_d


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


def schedule_logic(day_subject_list: list) -> list:
    subject_schedule: list = []
    subject_index: int = 0
    lessons: int = 0
    previous_subject: int = 0
    
    for lessons, subject_index in enumerate(day_subject_list):
        if lessons == 0:
            print('lesson == 0')
            if subjects()[subject_index].difficult == False and subjects()[subject_index].hours > 0 and previous_subject == subject_index:
                print('subject_index: ', subject_index)
                subject_schedule.append(subjects()[subject_index].name)
                r: Subject = subjects()[subject_index]
                subjects().remove(subjects()[subject_index])
                subjects().append(Subject(name=r.name, hours=r.hours - 1, difficult=r.difficult))
            else:
                for subject in subjects():
                    if subject.hours > subjects()[subject_index].hours and subject.difficult == False:
                        if subject.hours > 0 and previous_subject == subject_index:
                            subject_index = subjects().index(subject)
                print('subject_index: ', subject_index)

                subject_schedule.append(subjects()[subject_index].name)
                r = subjects()[subject_index]
                subjects().remove(subjects()[subject_index])
                subjects().append(Subject(name=r.name, hours=r.hours - 1, difficult=r.difficult))
        else:
            print('lesson == any')
            print('subject_index: ', subject_index)
            if subjects()[subject_index].hours > 0:
                subject_schedule.append(subjects()[subject_index].name)
                r = subjects()[subject_index]
                subjects().remove(subjects()[subject_index])
                subjects().append(Subject(name=r.name, hours=r.hours - 1, difficult=r.difficult))
        previous_subject = subject_index

    return subject_schedule


def generate(seed: int = 0, school_week: int = 12, max_nld: int = 1, min_nld: int = 1) -> dict[int, list[list[str]]]:
    """
    :param seed: serves to clarify the generation: 0 - by the hour
                                                   1 - the first week is random, and after by the hour
                                                   others - by numbers the first week, and after by the hour
    :param school_week: number of school days
    :param max_nld: maximum number of lessons per day
    :param min_nld: minimum number of lessons per day
    :return: dictionary with a schedule where the key is the week,
            and value dictionary with key day, and value is the schedule itself
    """
    subject: Subject
    subject_schedule_d: list[list[str]] = []
    subject_schedule: dict[int, list[list[str]]] = {}
    subject_schedule_l: list[str] = []  #subject schedule in list
    day: int = 1
    long_subject: int = 0
    all_hours: int = 0
    max_lesson_d: int = 0
    seed_l: list[int] = []

    for subject in subjects():
        all_hours = subject.hours + all_hours
        max_lesson_d: int = math.ceil(all_hours / (5*school_week))# max lessons on day
    print(f'max_lesson_d: {max_lesson_d}')
    print(f'all_hours: {all_hours}')
    print(f'5*school_week: {5*school_week}')

    if seed == 0:
        pass
    elif seed == 1:
        seed = random.randint(10 ** max_lesson_d, 10 ** (max_lesson_d + 1) - 1) #generating numbers the size of the number of lessons per day
        seed_l = list(map(int, str(seed)))
    else:
        if 10 ** max_lesson_d < seed:
            if seed < 10 ** (max_lesson_d + 1) - 1:
                seed_l = list(map(int, str(seed)))
            else:
                seed_l = list(map(int, str(seed)))
                seed = seed / (10 ** (len(seed_l) - max_lesson_d)) #сделать через div
        else:
            seed = seed * (10 ** (max_lesson_d - len(list(map(int, str(seed))))))
            seed_l = list(map(int, str(seed)))

    for week in range(school_week):
        print(f'week: {week}')
        for day in range(5):
            print(f'day: {day}')
            if seed == 0:
                for lessons in range(max_lesson_d):
                    print(f'lessons: {lessons}')

                    for subject in subjects():
                        if subject.hours > 0:
                            # if not subjects().index(subject) == seed_l[0]:
                            if subject.hours > subjects()[long_subject].hours:
                                long_subject = subjects().index(subject)
                    seed_l.append(long_subject)

                    print('seed: ', seed_l)
                    print('long_subject: ', long_subject)
            print('seed d: ', seed_l)

            subject_schedule_l = schedule_logic(seed_l)
            subject_schedule_d.append(subject_schedule_l)
            subject_schedule_l = []
            seed_l = []
            seed = 0

        subject_schedule[week] = subject_schedule_d
        subject_schedule_d = []

    print(all_hours / (5 * school_week))
    return subject_schedule


def main() -> None:
    seed = int(input())
    print(generate(seed=seed))
    for subject in subjects():
        print(f'Name: {subject.name} \n'
              f'Hours: {subject.hours}')
    pass


if __name__ == '__main__':
    main() # 1- доделать генерацию 2- добавить работу max_nld и min_nld
