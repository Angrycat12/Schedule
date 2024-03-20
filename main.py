import settings
import math
import random
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


subjectsf: dict[str, list[int | bool]] = {#'': [0, False],
                                          'Math': [60, True],
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
        subject_parametrs: list = subjectsf[subject_name]  # 0-hours, 1-difficult
        subject_list.append(Subject(name=subject_name, hours=subject_parametrs[0], difficult=subject_parametrs[1]))
    return subject_list


def generate(seed: int = 0, time: int = 70, max_nld: int = 1, min_nld: int = 1) -> dict[int, list[str]]:
    """
    :param seed: serves to clarify the generation: 0 - by the hour
                                                   1 - the first week is random, and after by the hour
                                                   others - by numbers the first week, and after by the hour
    :param time: number of school days
    :param max_nld: maximum number of lessons per day
    :param min_nld: minimum number of lessons per day
    :return: dictionary with a schedule where the key is the day, and the value is the schedule itself
    """
    subject: Subject
    subject_schedule: dict[int, list[str]] = {}
    subject_schedule_l: list[str] = []  #subject schedule in list
    day: int = 1
    long_subject: int = 0
    all_hours: int = 0
    max_lesson_d: int = 0

    for subject in subjects():
        all_hours = subject.hours + all_hours
        max_lesson_d: int = math.ceil(all_hours / time)  # max lessons on day

    if seed == 0:
        print(f'max_lesson_d: {max_lesson_d}')
        while day < time:
            lessons = 0
            print(f'day: {day}')
            while lessons < max_lesson_d:
                print(f'lessons: {lessons}')
                for subject in subjects():
                    if subject.hours > subjects()[long_subject].hours:
                        long_subject = subjects().index(subject)
                if lessons == 0:
                    if subjects()[long_subject].difficult == False:
                        subject_schedule_l.append(subjects()[long_subject].name)
                        r = subjects()[long_subject]
                        subjects().remove(subjects()[long_subject])
                        subjects().append(Subject(name=r.name, hours=r.hours - 1, difficult=r.difficult))
                    else:
                        for subject in subjects():
                            if subject.hours > subjects()[long_subject].hours and subject.difficult == False:
                                long_subject = subjects().index(subject)

                        subject_schedule_l.append(subjects()[long_subject].name)
                        r = subjects()[long_subject]
                        subjects().remove(subjects()[long_subject])
                        subjects().append(Subject(name=r.name, hours=r.hours - 1, difficult=r.difficult))
                else:
                    subject_schedule_l.append(subjects()[long_subject].name)
                    r = subjects()[long_subject]
                    subjects().remove(subjects()[long_subject])
                    subjects().append(Subject(name=r.name, hours=r.hours - 1, difficult=r.difficult))

                lessons += 1

            subject_schedule[day] = subject_schedule_l
            subject_schedule_l = []
            day += 1
    elif seed == 1:
        seed = random.randint(10 ** max_lesson_d, 10 ** (max_lesson_d + 1) - 1) #generating numbers the size of the number of lessons per day
        seed_l = list(map(int, str(seed)))

        while day < time:
            lessons = 0
            print(f'day: {day}')
            while lessons < max_lesson_d:
                print(f'lessons: {lessons}')
                if lessons == 0:
                    if subjects()[seed_l[lessons]].difficult == False:
                        subject_schedule_l.append(subjects()[seed_l[lessons]].name)
                        r = subjects()[seed_l[lessons]]
                        subjects().remove(subjects()[seed_l[lessons]])
                        subjects().append(Subject(name=r.name, hours=r.hours - 1, difficult=r.difficult))
                    else:
                        for subject in subjects():
                            if subject.hours > subjects()[long_subject].hours and subject.difficult == False:
                                long_subject = subjects().index(subject)

                        subject_schedule_l.append(subjects()[long_subject].name)
                        r = subjects()[long_subject]
                        subjects().remove(subjects()[long_subject])
                        subjects().append(Subject(name=r.name, hours=r.hours - 1, difficult=r.difficult))
                else:
                    subject_schedule_l.append(subjects()[seed_l[lessons]].name)
                    r = subjects()[seed_l[lessons]]
                    subjects().remove(subjects()[seed_l[lessons]])
                    subjects().append(Subject(name=r.name, hours=r.hours - 1, difficult=r.difficult))

                lessons += 1

            subject_schedule[day] = subject_schedule_l
            subject_schedule_l = []
            day += 1
    else:
        if 10 ** max_lesson_d < seed:
            if seed < 10 ** (max_lesson_d + 1) - 1:
                seed_l = list(map(int, str(seed)))

                while day < time:
                    lessons = 0
                    print(f'day: {day}')
                    while lessons < max_lesson_d:
                        print(f'lessons: {lessons}')
                        if lessons == 0:
                            if subjects()[seed_l[lessons]].difficult == False:
                                subject_schedule_l.append(subjects()[seed_l[lessons]].name)
                                r = subjects()[seed_l[lessons]]
                                subjects().remove(subjects()[seed_l[lessons]])
                                subjects().append(Subject(name=r.name, hours=r.hours - 1, difficult=r.difficult))
                            else:
                                for subject in subjects():
                                    if subject.hours > subjects()[long_subject].hours and subject.difficult == False:
                                        long_subject = subjects().index(subject)

                                subject_schedule_l.append(subjects()[long_subject].name)
                                r = subjects()[long_subject]
                                subjects().remove(subjects()[long_subject])
                                subjects().append(Subject(name=r.name, hours=r.hours - 1, difficult=r.difficult))
                        else:
                            subject_schedule_l.append(subjects()[seed_l[lessons]].name)
                            r = subjects()[seed_l[lessons]]
                            subjects().remove(subjects()[seed_l[lessons]])
                            subjects().append(Subject(name=r.name, hours=r.hours - 1, difficult=r.difficult))

                        lessons += 1

                    subject_schedule[day] = subject_schedule_l
                    subject_schedule_l = []
                    day += 1
            else:
                seed_l = list(map(int, str(seed)))

        else:
            seed = seed * (10 ** (max_lesson_d - len(list(map(int, str(seed))))))
            seed_l = list(map(int, str(seed)))

            while day < time:
                lessons = 0
                print(f'day: {day}')
                while lessons < max_lesson_d:
                    print(f'lessons: {lessons}')
                    if lessons == 0:
                        if subjects()[seed_l[lessons]].difficult == False:
                            subject_schedule_l.append(subjects()[seed_l[lessons]].name)
                            r = subjects()[seed_l[lessons]]
                            subjects().remove(subjects()[seed_l[lessons]])
                            subjects().append(Subject(name=r.name, hours=r.hours - 1, difficult=r.difficult))
                        else:
                            for subject in subjects():
                                if subject.hours > subjects()[long_subject].hours and subject.difficult == False:
                                    long_subject = subjects().index(subject)

                            subject_schedule_l.append(subjects()[long_subject].name)
                            r = subjects()[long_subject]
                            subjects().remove(subjects()[long_subject])
                            subjects().append(Subject(name=r.name, hours=r.hours - 1, difficult=r.difficult))
                    else:
                        subject_schedule_l.append(subjects()[seed_l[lessons]].name)
                        r = subjects()[seed_l[lessons]]
                        subjects().remove(subjects()[seed_l[lessons]])
                        subjects().append(Subject(name=r.name, hours=r.hours - 1, difficult=r.difficult))

                    lessons += 1

                subject_schedule[day] = subject_schedule_l
                subject_schedule_l = []
                day += 1

    return subject_schedule


def main() -> None:
    print(generate(seed=15))
    pass


if __name__ == '__main__':
    main() # 1- переделать генерацию по 1 и рандомному числу 2- засунуть цикл в функцию 3- добавить работу max_nld и min_nld
