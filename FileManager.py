import settings
import json


def read_file_subjects(file_name) -> dict[int, list[list[str]]] | ValueError:
    """
    Reads a file subjects in .txt or in .json format.
    :return: dictionary where the key is the name of the lesson, and the value is the parameters of this lesson
    """
    schedule: dict[int, list[list[str]]] = {}
    format: str = file_name.split('.')[1]
    if format == '.txt':
        with open(file_name, 'r') as SubjectFile:
            subject_t = SubjectFile.read()
            for word in subject_t:
                pass

            SubjectFile.close()
    else:
        if format == '.json':
            with open(file_name, 'r') as SubjectFile:
                subject_j = json.load(SubjectFile)
                for week, schedule_d in subject_j.item():
                    pass

                SubjectFile.close()
        else:
            return ValueError
    return schedule


def write_file_subjects(schedule: dict[int, list[list[str]]],
                        file_name: str,
                        format: str = '.json') -> None | ValueError:
    """
    write subjects in file in .txt or in .json format.
    :param schedule: schedule to write
    :param file_name: name file
    :param format: format file to write(txt or json)
    """
    file_name = file_name.split('.')[0]
    if format == '.txt':
        with open(file_name + format, 'w') as SubjectFile:
            try:
                SubjectFile.read()
                for word in SubjectFile:
                    pass
            finally:
                SubjectFile.close()
    else:
        if format == '.json':
            with open(file_name+format, 'w') as SubjectFile:
                subject_j = json.load(SubjectFile)

                SubjectFile.close()
        else:
            return ValueError

if __name__ == '__main__':
    pass