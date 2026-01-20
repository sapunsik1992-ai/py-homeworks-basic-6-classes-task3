from __future__ import annotations

from functools import total_ordering


def average_grade(grades: dict[str, list[int]], course: str | None = None) -> float:
    """
    Return average grade from dict {course: [grades]}.
    If course is provided, average is calculated only for that course.
    If there are no grades, returns 0.0.
    """
    values: list[int] = []

    if course is not None:
        values = grades.get(course, [])
    else:
        for course_grades in grades.values():
            values.extend(course_grades)

    if not values:
        return 0.0

    return sum(values) / len(values)


def normalize_course_list(courses: list[str]) -> str:
    """Join course names into a string, trimming extra spaces."""
    return ", ".join([c.strip() for c in courses])


@total_ordering
class Student:
    def __init__(self, name: str, surname: str, gender: str):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses: list[str] = []
        self.courses_in_progress: list[str] = []
        self.grades: dict[str, list[int]] = {}

    def rate_lecture(self, lecturer: "Lecturer", course: str, grade: int):
        """Rate a lecturer for a course (1..10)."""
        if (
            isinstance(lecturer, Lecturer)
            and course in self.courses_in_progress
            and course in lecturer.courses_attached
            and 1 <= grade <= 10
        ):
            lecturer.grades.setdefault(course, []).append(grade)
        else:
            return "Ошибка"

    def avg_hw(self) -> float:
        return average_grade(self.grades)

    def __str__(self) -> str:
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за домашние задания: {self.avg_hw():.1f}\n"
            f"Курсы в процессе изучения: {normalize_course_list(self.courses_in_progress)}\n"
            f"Завершенные курсы: {normalize_course_list(self.finished_courses)}"
        )

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Student):
            return NotImplemented
        return self.avg_hw() < other.avg_hw()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Student):
            return NotImplemented
        return self.avg_hw() == other.avg_hw()


class Mentor:
    def __init__(self, name: str, surname: str):
        self.name = name
        self.surname = surname
        self.courses_attached: list[str] = []


@total_ordering
class Lecturer(Mentor):
    def __init__(self, name: str, surname: str):
        super().__init__(name, surname)
        self.grades: dict[str, list[int]] = {}

    def avg_lectures(self) -> float:
        return average_grade(self.grades)

    def __str__(self) -> str:
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за лекции: {self.avg_lectures():.1f}"
        )

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.avg_lectures() < other.avg_lectures()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.avg_lectures() == other.avg_lectures()


class Reviewer(Mentor):
    def rate_hw(self, student: Student, course: str, grade: int):
        """Rate student's homework for a course (1..10)."""
        if (
            isinstance(student, Student)
            and course in self.courses_attached
            and course in student.courses_in_progress
            and 1 <= grade <= 10
        ):
            student.grades.setdefault(course, []).append(grade)
        else:
            return "Ошибка"

    def __str__(self) -> str:
        return f"Имя: {self.name}\nФамилия: {self.surname}"


if __name__ == "__main__":
    reviewer = Reviewer("Some", "Buddy")
    reviewer.courses_attached += ["Python", "Git"]

    lecturer_1 = Lecturer("Some", "Buddy")
    lecturer_1.courses_attached += ["Python"]

    lecturer_2 = Lecturer("Ivan", "Ivanov")
    lecturer_2.courses_attached += ["Python"]

    student_1 = Student("Ruoy", "Eman", "M")
    student_1.courses_in_progress += ["Python", "Git"]  # даже если будет "Git "
    student_1.finished_courses += ["Введение в программирование"]

    student_2 = Student("Anna", "Smirnova", "F")
    student_2.courses_in_progress += ["Python"]
    student_2.finished_courses += ["Введение в программирование"]

    student_1.rate_lecture(lecturer_1, "Python", 10)
    student_1.rate_lecture(lecturer_1, "Python", 9)

    student_2.rate_lecture(lecturer_2, "Python", 8)
    student_2.rate_lecture(lecturer_2, "Python", 9)

    reviewer.rate_hw(student_1, "Python", 10)
    reviewer.rate_hw(student_1, "Git", 9)

    reviewer.rate_hw(student_2, "Python", 8)

    print(reviewer)
    print()
    print(lecturer_1)
    print()
    print(student_1)
    print()

    print("lecturer_1 > lecturer_2:", lecturer_1 > lecturer_2)
    print("lecturer_1 == lecturer_2:", lecturer_1 == lecturer_2)
    print("student_1 > student_2:", student_1 > student_2)
    print("student_1 == student_2:", student_1 == student_2)