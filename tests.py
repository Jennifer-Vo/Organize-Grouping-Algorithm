from __future__ import annotations
import course
from course import *
import survey
from survey import *
import criterion
from criterion import *
from criterion import InvalidAnswerError
import grouper
from grouper import *
import pytest
import unittest


def test_course_class_student_str_() -> None:
    s1 = course.Student(1, 'Misha')
    assert s1.__str__() == 'Misha'


def test_course_class_student_student_has_answer() -> None:
    s1 = course.Student(1, 'Misha')
    question = survey.YesNoQuestion(1, 'Do you like food?')
    answer = survey.Answer(True)
    s1.set_answer(question, answer)
    assert s1.has_answer(question)


def test_course_class_student_get_answer() -> None:
    s1 = course.Student(1, 'Misha')
    question = survey.YesNoQuestion(1, 'Do you like food?')
    answer = survey.Answer(True)
    s1.set_answer(question, answer)
    assert s1.get_answer(question) == answer


def test_course_class_student_set_answer() -> None:
    s1 = course.Student(1, 'Misha')
    question = survey.YesNoQuestion(1, 'Do you like food?')
    answer = survey.Answer(True)
    s1.set_answer(question, answer)
    # noinspection PyProtectedMember
    assert answer in s1._answers


def test_course_class_course_enroll_students() -> None:
    s1 = course.Student(1, 'Misha')
    courses = course.Course('CSC148')
    courses.enroll_students([s1])
    assert courses.students == [s1]


def test_course_class_course_all_answered() -> None:
    s1 = course.Student(1, 'Misha')
    courses = course.Course('CSC148')
    courses.enroll_students([s1])
    question = survey.YesNoQuestion(1, 'Do you like food?')
    answer = survey.Answer(True)
    s1.set_answer(question, answer)
    surveys = survey.Survey([question])
    assert courses.all_answered(surveys)


def test_course_class_course_get_students() -> None:
    s1 = course.Student(1, 'Misha')
    s2 = course.Student(2, 'Jenni')
    courses = course.Course('CSC148')
    courses.enroll_students([s1, s2])
    assert courses.get_students() == (s1, s2)
    assert not courses.get_students() == (s2, s1)


def test__has_student() -> None:
    course1 = course.Course("CSC148")
    ted = course.Student(1, "Ted")
    fred = course.Student(2, "Fred")
    students = [ted, fred]
    course1.enroll_students(students)
    assert course1._Course__has_student(ted)
    assert not course1._Course__has_student(course.Student(3, "Bob"))


def test_survey_checkbox_question__str__() -> None:
    question1 = survey.CheckboxQuestion(1, 'Who are you?', ['A', 'B', 'C'])
    assert '1' and 'Who are you?' and 'A' and 'B' and 'C' in str(question1)


def test_survey_checkbox_question_validate_answer() -> None:
    question = survey.CheckboxQuestion(1, 'What do you want?', ['A', 'B', 'C'])
    assert question.validate_answer(survey.Answer(['B', 'C']))
    assert not question.validate_answer(survey.Answer(['Z']))


def test_survey_checkbox_question_get_similarity() -> None:
    question = survey.CheckboxQuestion(1, 'What do you want?', ['A', 'B', 'C', 'D', 'E'])
    answer1 = survey.Answer(['B', 'D'])
    answer2 = survey.Answer(['C', 'D'])
    assert question.get_similarity(answer1, answer2) == 1/3


def test_survey_multiplechoice_question__str__() -> None:
    question1 = survey.MultipleChoiceQuestion(1, 'Who are you?', ['A', 'B', 'C'])
    assert '1' and 'Who are you?' and 'A' and 'B' and 'C' in str(question1)


def test_survey_multiplechoice_question_validate_answer() -> None:
    question = survey.MultipleChoiceQuestion(1, 'ABC?', ['A', 'B', 'C'])
    assert question.validate_answer(survey.Answer('A'))
    assert not question.validate_answer(survey.Answer('G'))


def test_survey_multiplechoice_question_get_similarity() -> None:
    question = survey.MultipleChoiceQuestion(1, 'ABC?', ['A', 'B', 'C'])
    assert question.get_similarity(survey.Answer('A'), survey.Answer('A'))\
    == 1.0
    assert question.get_similarity(survey.Answer('A'), survey.Answer('B'))\
    == 0.0


def test_survey_numeric_question__str__() -> None:
    question1 = survey.NumericQuestion(1, 'Is this good?', 0, 10)
    assert '1' and 'Is this good?' and '0' and '10' in str(question1)


def test_survey_numeric_question_validate_answer() -> None:
    question = survey.NumericQuestion(1, 'Do you like food?', 0, 10)
    assert question.validate_answer(survey.Answer(5))
    assert not question.validate_answer(survey.Answer(11))
    assert not question.validate_answer(survey.Answer(-1))


def test_survey_numeric_question_get_similarity() -> None:
    question = survey.NumericQuestion(1, 'Do you like food?', 0, 10)
    assert question.get_similarity(survey.Answer(5), survey.Answer(5)) == 1.0
    assert question.get_similarity(survey.Answer(0), survey.Answer(5)) == 0.5


def test_survey_yesno_question__str__() -> None:
    question1 = survey.YesNoQuestion(1, 'Is this good?')
    assert '1' and 'Is this good?' in str(question1)


def test_survey_yesno_question_validate_answer() -> None:
    question = survey.YesNoQuestion(1, 'Do you like food?')
    assert question.validate_answer(survey.Answer(False))
    assert question.validate_answer(survey.Answer(True))
    assert not question.validate_answer(survey.Answer(2))
    assert not question.validate_answer(survey.Answer('Hello'))


def test_survey_yesno_question_get_similarity() -> None:
    question = survey.YesNoQuestion(1, 'Do you like food?')
    assert question.get_similarity(survey.Answer(False), survey.Answer(False))\
    == 1.0
    assert question.get_similarity(survey.Answer(False), survey.Answer(True))\
    == 0.0


def test_survey_answer_is_valid() -> None:
    question = survey.CheckboxQuestion(1, 'What do you want?', ['A', 'B', 'C'])
    answer1 = survey.Answer(['C', 'B'])
    answer2 = survey.Answer(5)
    assert answer1.is_valid(question)
    assert not answer2.is_valid(question)


def test_survey_class_survey__len__() -> None:
    q1 = survey.YesNoQuestion(1, 'Hello?')
    q2 = survey.YesNoQuestion(3, 'Hello who are you?')
    q3 = survey.NumericQuestion(4, 'How are you?', 0, 10)
    survey1 = survey.Survey([q1, q2, q3])
    assert survey1.__len__() == 3


def test_survey_class_survey__contains__() -> None:
    q1 = survey.YesNoQuestion(1, 'Hello?')
    q2 = survey.YesNoQuestion(3, 'Hello who are you?')
    q3 = survey.NumericQuestion(4, 'How are you?', 0, 10)
    survey1 = survey.Survey([q1, q2, q3])
    assert survey1.__contains__(q2)


def test_survey_class_survey__str__() -> None:
    question1 = survey.YesNoQuestion(1, 'Hello?')
    survey1 = survey.Survey([question1])
    assert 'Hello' in str(survey1)


def test_survey_class_survey_get_questions() -> None:
    question1 = survey.YesNoQuestion(1, 'Hello?')
    survey1 = survey.Survey([question1])
    assert survey1.get_questions() == [question1]


def test_survey_class_survey_get_criterion() -> None:
    criteria = criterion.HomogeneousCriterion()
    question1 = survey.YesNoQuestion(1, 'Hello?')
    survey1 = survey.Survey([question1])
    survey1.set_criterion(criteria, question1)
    # noinspection PyProtectedMember
    assert survey1._get_criterion(question1) == criteria


def test_survey_class_survey_set_criterion() -> None:
    criteria = criterion.HomogeneousCriterion()
    question1 = survey.YesNoQuestion(1, 'Hello?')
    survey1 = survey.Survey([question1])
    survey1.set_criterion(criteria, question1)
    # noinspection PyProtectedMember
    assert question1.id in survey1._criteria


def test_survey_class_survey_get_weight() -> None:
    question1 = survey.YesNoQuestion(1, 'Hello?')
    survey1 = survey.Survey([question1])
    weight1 = 1
    survey1.set_weight(weight1, question1)
    # noinspection PyProtectedMember
    assert survey1._get_weight(question1) == weight1


def test_survey_class_survey_set_weight() -> None:
    question1 = survey.YesNoQuestion(1, 'Hello?')
    survey1 = survey.Survey([question1])
    weight1 = 1
    survey1.set_weight(weight1, question1)
    # noinspection PyProtectedMember
    assert weight1 in survey1._weights


def test_survey_class_survey_score_students() -> None:
    s1 = course.Student(1, 'Misha')
    students = [s1]
    question1 = survey.NumericQuestion(1, 'Do you like food?', 0, 10)
    answer1 = survey.Answer(5)
    survey1 = survey.Survey([question1])
    criteria = criterion.HomogeneousCriterion()
    weight1 = 1
    s1.set_answer(question1, answer1)
    survey1.set_weight(weight1, question1)
    survey1.set_criterion(criteria, question1)
    assert survey1.score_students(students) == 1.0


def test_survey_class_survey_score_students_two_students() -> None:
    s1 = course.Student(1, 'Misha')
    s2 = course.Student(2, 'Jennifer')
    students = [s1, s2]
    question1 = survey.NumericQuestion(1, 'Do you like food?', 0, 10)
    answer1 = survey.Answer(5)
    answer2 = survey.Answer(10)
    survey1 = survey.Survey([question1])
    criteria = criterion.HeterogeneousCriterion()
    weight1 = 3
    s1.set_answer(question1, answer1)
    s2.set_answer(question1, answer2)
    survey1.set_weight(weight1, question1)
    survey1.set_criterion(criteria, question1)
    assert survey1.score_students(students) == 1.5


def test_survey_class_survey_score_students_raise_invalidanswererror() -> None:
    s1 = course.Student(1, 'Misha')
    students = [s1]
    question1 = survey.NumericQuestion(1, 'Do you like food?', 0, 10)
    answer1 = survey.Answer(True)
    survey1 = survey.Survey([question1])
    criteria = criterion.HomogeneousCriterion()
    weight1 = 1
    s1.set_answer(question1, answer1)
    survey1.set_weight(weight1, question1)
    survey1.set_criterion(criteria, question1)
    assert survey1.score_students(students) == 0.0


def test_survey_class_survey_score_grouping() -> None:
    q1 = survey.NumericQuestion(1, "How many?", 0, 5)
    q2 = survey.YesNoQuestion(2, 'Are you okay?')
    survey1 = survey.Survey([q1, q2])
    ted = course.Student(1, "Ted")
    fred = course.Student(2, "Fred")
    jack = course.Student(3, "Jack")
    bob = course.Student(4, "Bob")
    ted.set_answer(q1, survey.Answer(2))
    fred.set_answer(q1, survey.Answer(3))
    jack.set_answer(q1, survey.Answer(4))
    bob.set_answer(q1, survey.Answer(1))
    ted.set_answer(q2, survey.Answer(True))
    fred.set_answer(q2, survey.Answer(True))
    jack.set_answer(q2, survey.Answer(False))
    bob.set_answer(q2, survey.Answer(False))
    grouping1 = grouper.Grouping()
    grouping1.add_group(grouper.Group([ted, fred]))
    grouping1.add_group(grouper.Group([jack, bob]))
    assert survey1.score_grouping(grouping1) == 0.8


def test_criterion_homogeneous_score_answers() -> None:
    question = survey.YesNoQuestion(1, 'Do you like food?')
    answers = [survey.Answer(True), survey.Answer(True), survey.Answer(False)]
    criterions = criterion.HomogeneousCriterion()
    assert criterions.score_answers(question, answers) == 1/3


def test_criterion_homogeneous_raise_invalidanswererror():
    question = survey.NumericQuestion(1, 'Do you like food?', 0, 10)
    answer1 = [survey.Answer(11)]
    answer2 = [survey.Answer(False)]
    answer3 = [survey.Answer(5), survey.Answer(False)]
    with pytest.raises(InvalidAnswerError):
        criterion.HomogeneousCriterion().score_answers(question, answer1)
        criterion.HomogeneousCriterion().score_answers(question, answer2)
        criterion.HomogeneousCriterion().score_answers(question, answer3)


def test_criterion_heterogeneous_score_answers() -> None:
    question = survey.YesNoQuestion(1, 'Do you like food?')
    answers = [survey.Answer(True), survey.Answer(True), survey.Answer(False)]
    criterions = criterion.HeterogeneousCriterion()
    assert pytest.approx(criterions.score_answers(question, answers), 5) == 2/3


def test_criterion_heterogeneous_raise_invalidanswererror():
    question = survey.NumericQuestion(1, 'Do you like food?', 0, 10)
    answer = [survey.Answer(11)]
    with pytest.raises(InvalidAnswerError):
        criterion.HeterogeneousCriterion().score_answers(question, answer)


def test_criterion_lonelymember_criterion_score_answers() -> None:
    question1 = survey.YesNoQuestion(1, 'Do you like food?')
    answer1 = [survey.Answer(True), survey.Answer(True), survey.Answer(False)]
    assert criterion.LonelyMemberCriterion().score_answers(question1, answer1) == 0.0


def test_criterion_lonelymember_raise_invalidanswererror():
    question = survey.NumericQuestion(1, 'Do you like food?', 0, 10)
    answer = [survey.Answer(11)]
    with pytest.raises(InvalidAnswerError):
        criterion.LonelyMemberCriterion().score_answers(question, answer)


def test_grouper_slice_list() -> None:
    lst = [1, [1, 2, 4], 'Jennifer', False, [True, False], 3, 4]
    assert grouper.slice_list(lst, 1) == [[1], [[1, 2, 4]], ['Jennifer'], [False], [[True, False]], [3], [4]]
    assert grouper.slice_list(lst, 3) == [[1, [1, 2, 4], 'Jennifer'], [False, [True, False], 3], [4]]


def test_grouper_windows() -> None:
    lst = [['a']]
    lst1 = [['a', 'b', True], 1.0, 'Jennifer', True]
    assert grouper.windows(lst, 1) == [[['a']]]
    assert grouper.windows(lst1, 3) == [[['a', 'b', True], 1.0, 'Jennifer'], [1.0, 'Jennifer', True]]


def test_grouper_alphagrouper() -> None:
    c1 = course.Course('CSC148')
    s1 = course.Student(1, 'Ali')
    s2 = course.Student(2, 'Kat')
    s3 = course.Student(3, 'Dorsa')
    s4 = course.Student(4, 'Sophia')
    s5 = course.Student(5, 'Momo')
    s6 = course.Student(6, 'Joseph')
    c1.enroll_students([s1, s2, s3, s4, s5, s6])
    a1 = grouper.AlphaGrouper(2)
    q1 = survey.MultipleChoiceQuestion(1, 'What is your choice?', ['A', 'B', 'C'])
    sur1 = survey.Survey([q1])
    assert a1.make_grouping(c1, sur1).get_groups()[0].get_members()[0] == s1
    assert a1.make_grouping(c1, sur1).get_groups()[2].get_members()[0] == s5


def test_grouper_randomgrouper() -> None:
    c1 = course.Course('CSC148')
    s1 = course.Student(1, 'Ali')
    s2 = course.Student(2, 'Kat')
    s3 = course.Student(3, 'Dorsa')
    s4 = course.Student(4, 'Sophia')
    s5 = course.Student(5, 'Momo')
    s6 = course.Student(6, 'Joseph')
    c1.enroll_students([s1, s2, s3, s4, s5, s6])
    a1 = grouper.RandomGrouper(2)
    q1 = survey.MultipleChoiceQuestion(1, 'What is your choice?', ['A', 'B', 'C'])
    sur1 = survey.Survey([q1])
    assert len(a1.make_grouping(c1, sur1).get_groups()) == 3
    assert len(a1.make_grouping(c1, sur1).get_groups()[2].get_members()) == 2


def test_grouper_greedygrouper() -> None:
    c1 = course.Course('CSC148')
    s1 = course.Student(1, 'Ali')
    s2 = course.Student(2, 'Kat')
    s3 = course.Student(3, 'Dorsa')
    s4 = course.Student(4, 'Sophia')
    s5 = course.Student(5, 'Momo')
    s6 = course.Student(6, 'Joseph')
    c1.enroll_students([s1, s2, s3, s4, s5, s6])
    a1 = grouper.GreedyGrouper(2)
    q1 = survey.MultipleChoiceQuestion(1, 'What is your choice?', ['A', 'B', 'C'])
    a = survey.Answer('A')
    b = survey.Answer('B')
    c = survey.Answer('C')
    s1.set_answer(q1, a)
    s2.set_answer(q1, b)
    s3.set_answer(q1, c)
    s4.set_answer(q1, a)
    s5.set_answer(q1, b)
    s6.set_answer(q1, c)
    sur1 = survey.Survey([q1])
    assert a1.make_grouping(c1, sur1).get_groups()[0].get_members()[0] == s1
    assert a1.make_grouping(c1, sur1).get_groups()[2].get_members()[1] == s6


def test_windowgrouping() -> None:
    ted = course.Student(1, "Ted")
    fred = course.Student(2, "Fred")
    jack = course.Student(3, "Jack")
    bob = course.Student(4, "Bob")
    course1 = course.Course("CSC148")
    course1.enroll_students([ted, fred, jack, bob])
    question1 = survey.YesNoQuestion(1, "Really?")
    survey1 = survey.Survey([question1])
    ted.set_answer(question1, survey.Answer(True))
    fred.set_answer(question1, survey.Answer(False))
    jack.set_answer(question1, survey.Answer(False))
    bob.set_answer(question1, survey.Answer(True))
    grouper1 = grouper.WindowGrouper(2)
    grouping1 = grouper1.make_grouping(course1, survey1)
    assert fred in grouping1.get_groups()[0]
    assert jack in grouping1.get_groups()[0]
    assert ted in grouping1.get_groups()[1]
    assert bob in grouping1.get_groups()[1]


def test_grouper_class_group__len__() -> None:
    c1 = course.Course('CSC148')
    s1 = course.Student(1, 'Ali')
    s2 = course.Student(2, 'Kat')
    s3 = course.Student(3, 'Dorsa')
    s4 = course.Student(4, 'Sophia')
    s5 = course.Student(5, 'Momo')
    s6 = course.Student(6, 'Joseph')
    c1.enroll_students([s1, s2, s3, s4, s5, s6])
    a1 = grouper.AlphaGrouper(2)
    q1 = survey.MultipleChoiceQuestion(1, 'What is your choice?', ['A', 'B', 'C'])
    sur1 = survey.Survey([q1])
    a1.make_grouping(c1, sur1)
    assert a1.make_grouping(c1, sur1).get_groups()[0].__len__() == 2


def test_grouper_class_group__contains__() -> None:
    c1 = course.Course('CSC148')
    s1 = course.Student(1, 'Ali')
    s2 = course.Student(2, 'Kat')
    s3 = course.Student(3, 'Dorsa')
    s4 = course.Student(4, 'Sophia')
    s5 = course.Student(5, 'Momo')
    s6 = course.Student(6, 'Joseph')
    c1.enroll_students([s1, s2, s3, s4, s5, s6])
    a1 = grouper.AlphaGrouper(2)
    q1 = survey.MultipleChoiceQuestion(1, 'What is your choice?', ['A', 'B', 'C'])
    sur1 = survey.Survey([q1])
    a1.make_grouping(c1, sur1)
    assert a1.make_grouping(c1, sur1).get_groups()[1].__contains__(s6)
    assert a1.make_grouping(c1, sur1).get_groups()[1].__contains__(s2)
    assert not a1.make_grouping(c1, sur1).get_groups()[0].__contains__(s5)


def test_grouper_class_group__str__() -> None:
    c1 = course.Course('CSC148')
    s1 = course.Student(1, 'Ali')
    s2 = course.Student(2, 'Kat')
    s3 = course.Student(3, 'Dorsa')
    s4 = course.Student(4, 'Sophia')
    s5 = course.Student(5, 'Momo')
    s6 = course.Student(6, 'Joseph')
    c1.enroll_students([s1, s2, s3, s4, s5, s6])
    a1 = grouper.AlphaGrouper(2)
    q1 = survey.MultipleChoiceQuestion(1, 'What is your choice?', ['A', 'B', 'C'])
    sur1 = survey.Survey([q1])
    a1.make_grouping(c1, sur1)
    assert 'Ali' and 'Dorsa' in a1.make_grouping(c1, sur1).get_groups()[0].__str__()
    assert not 'Momo' in a1.make_grouping(c1, sur1).get_groups()[0].__str__()


def test_grouper_class_group_get_members_() -> None:
    c1 = course.Course('CSC148')
    s1 = course.Student(1, 'Ali')
    s2 = course.Student(2, 'Kat')
    s3 = course.Student(3, 'Dorsa')
    s4 = course.Student(4, 'Sophia')
    s5 = course.Student(5, 'Momo')
    s6 = course.Student(6, 'Joseph')
    c1.enroll_students([s1, s2, s3, s4, s5, s6])
    a1 = grouper.AlphaGrouper(2)
    q1 = survey.MultipleChoiceQuestion(1, 'What is your choice?', ['A', 'B', 'C'])
    sur1 = survey.Survey([q1])
    a1.make_grouping(c1, sur1)
    assert a1.make_grouping(c1, sur1).get_groups()[0].get_members() == [s1, s3]
    assert not a1.make_grouping(c1, sur1).get_groups()[0].get_members() == [s1]


def test_grouper_class_grouping__len__() -> None:
    c1 = course.Course('CSC148')
    s1 = course.Student(1, 'Ali')
    s2 = course.Student(2, 'Kat')
    s3 = course.Student(3, 'Dorsa')
    s4 = course.Student(4, 'Sophia')
    s5 = course.Student(5, 'Momo')
    s6 = course.Student(6, 'Joseph')
    c1.enroll_students([s1, s2, s3, s4, s5, s6])
    a1 = grouper.AlphaGrouper(2)
    q1 = survey.MultipleChoiceQuestion(1, 'What is your choice?', ['A', 'B', 'C'])
    sur1 = survey.Survey([q1])
    a1.make_grouping(c1, sur1)
    assert a1.make_grouping(c1, sur1).get_groups().__len__() == 3


def test_grouper_class_grouping__str__() -> None:
    c1 = course.Course('CSC148')
    s1 = course.Student(1, 'Ali')
    s2 = course.Student(2, 'Kat')
    s3 = course.Student(3, 'Dorsa')
    s4 = course.Student(4, 'Sophia')
    s5 = course.Student(5, 'Momo')
    s6 = course.Student(6, 'Joseph')
    c1.enroll_students([s1, s2, s3, s4, s5, s6])
    a1 = grouper.AlphaGrouper(2)
    q1 = survey.MultipleChoiceQuestion(1, 'What is your choice?', ['A', 'B', 'C'])
    sur1 = survey.Survey([q1])
    a1.make_grouping(c1, sur1)
    assert a1.make_grouping(c1, sur1).__str__() == 'Ali Dorsa\nJoseph Kat\nMomo Sophia\n'


def test_grouper_class_grouping_add_group_() -> None:
    grouping1 = grouper.Grouping()
    ted = course.Student(1, "Ted")
    fred = course.Student(2, "Fred")
    jack = course.Student(3, "Jack")
    assert not grouping1.add_group(grouper.Group([]))
    assert grouping1.add_group(grouper.Group([ted, fred]))
    assert not grouping1.add_group(grouper.Group([ted, jack]))


def test_grouper_class_grouping_get_groups_() -> None:
    c1 = course.Course('CSC148')
    s1 = course.Student(1, 'Ali')
    s2 = course.Student(2, 'Kat')
    s3 = course.Student(3, 'Dorsa')
    s4 = course.Student(4, 'Sophia')
    s5 = course.Student(5, 'Momo')
    s6 = course.Student(6, 'Joseph')
    c1.enroll_students([s1, s2, s3, s4, s5, s6])
    a1 = grouper.AlphaGrouper(2)
    q1 = survey.MultipleChoiceQuestion(1, 'What is your choice?', ['A', 'B', 'C'])
    sur1 = survey.Survey([q1])
    a1.make_grouping(c1, sur1)
    assert len(a1.make_grouping(c1, sur1).get_groups()) == 3


class TestStudent(unittest.TestCase):
    def test__str__(self) -> None:
        student = Student(1, "Ted")
        self.assertEqual(str(student), "Ted")

    def test_has_answer(self) -> None:
        student = Student(1, "Ted")
        q = YesNoQuestion(1, "Is it right?")
        self.assertFalse(student.has_answer(q))
        student.set_answer(q, Answer("a"))
        self.assertFalse(student.has_answer(q))
        student.set_answer(q, Answer(True))
        self.assertTrue(student.has_answer(q))

    def test_set_answer(self) -> None:
        student = Student(1, "Ted")
        q = YesNoQuestion(1, "Is it right?")
        answer = Answer(True)
        student.set_answer(q, answer)
        self.assertEqual(student._answers[0], answer)

    def test_get_answer(self) -> None:
        student = Student(1, "Ted")
        q = YesNoQuestion(1, "Is it right?")
        answer = Answer(True)
        student.set_answer(q, answer)
        self.assertEqual(student.get_answer(q), answer)


class TestCourse(unittest.TestCase):
    def test_enroll_students(self) -> None:
        course1 = Course("CSC148")
        ted = Student(1, "Ted")
        fred = Student(2, "Fred")
        students = [ted, fred]
        course1.enroll_students(students)
        self.assertEqual(course1.students, [ted, fred])

        course1.enroll_students(students)
        self.assertEqual(course1.students, [ted, fred])

        course1.enroll_students([Student(3, '')])
        self.assertEqual(course1.students, [ted, fred])

    def test_all_answered(self) -> None:
        course1 = Course("CSC148")
        ted = Student(1, "Ted")
        fred = Student(2, "Fred")
        students = [ted, fred]
        course1.enroll_students(students)

        q = YesNoQuestion(1, "Is it right?")
        survey1 = Survey([q])
        ted.set_answer(q, Answer(True))
        fred.set_answer(q, Answer(False))

        self.assertTrue(course1.all_answered(survey1))

    def test_get_students(self) -> None:
        course1 = Course("CSC148")
        ted = Student(1, "Ted")
        fred = Student(2, "Fred")
        students = [ted, fred]
        course1.enroll_students(students)

        self.assertTrue(isinstance(course1.get_students(), tuple))
        self.assertIn(ted, course1.get_students())
        self.assertIn(fred, course1.get_students())
        self.assertEqual(len(course1.get_students()), 2)

    def test__has_student(self) -> None:
        course1 = Course("CSC148")
        ted = Student(1, "Ted")
        fred = Student(2, "Fred")
        students = [ted, fred]
        course1.enroll_students(students)

        self.assertTrue(course1._Course__has_student(fred))
        self.assertFalse(course1._Course__has_student(Student(4, "Bobo")))


class TestCheckboxQuestion(unittest.TestCase):
    def test__str__(self) -> None:
        q = CheckboxQuestion(1, "What?", ['a', 'b', 'c'])
        self.assertEqual(str(q), "1: What?\na\nb\nc\n")

    def test_validate_answer(self) -> None:
        q = CheckboxQuestion(1, "What?", ['a', 'b', 'c'])

        self.assertFalse(q.validate_answer(Answer('a')))
        self.assertFalse(q.validate_answer(Answer([])))
        self.assertFalse(q.validate_answer(Answer(['a', 'a'])))
        self.assertFalse(q.validate_answer(Answer(['a', 'd'])))
        self.assertTrue(q.validate_answer(Answer(['a', 'b'])))

    def test_get_similarity(self) -> None:
        q = CheckboxQuestion(1, "What?", ['a', 'b', 'c'])
        self.assertEqual(round(q.get_similarity(Answer(['a', 'b']), Answer(['b', 'c'])), 2), 0.33)


class TestMultipleChoiceQuestion(unittest.TestCase):
    def test__str__(self) -> None:
        q = MultipleChoiceQuestion(2, "Which?", ['a', 'b', 'c', 'd'])
        self.assertEqual(str(q), "2: Which?\na\nb\nc\nd\n")

    def test_valiedate_answer(self) -> None:
        q = MultipleChoiceQuestion(2, "Which?", ['a', 'b', 'c', 'd'])
        self.assertFalse(q.validate_answer(Answer(True)))
        self.assertFalse(q.validate_answer(Answer('e')))
        self.assertTrue(q.validate_answer(Answer('c')))

    def test_get_similarity(self) -> None:
        q = MultipleChoiceQuestion(2, "Which?", ['a', 'b', 'c', 'd'])
        self.assertEqual(q.get_similarity(Answer('a'), Answer('b')), 0.0)
        self.assertEqual(q.get_similarity(Answer('a'), Answer('a')), 1.0)


class TestNumericQuestion(unittest.TestCase):
    def test__str__(self) -> None:
        q = NumericQuestion(3, "How many?", 1, 5)
        self.assertEqual(str(q), "3: How many? (1 - 5)\n")

    def test_validate_answer(self) -> None:
        q = NumericQuestion(3, "How many?", 1, 5)
        self.assertFalse(q.validate_answer(Answer(True)))
        self.assertFalse(q.validate_answer(Answer(0)))
        self.assertTrue(q.validate_answer(Answer(5)))

    def test_get_similarity(self) -> None:
        q = NumericQuestion(3, "How many?", 1, 5)
        self.assertEqual(q.get_similarity(Answer(2), Answer(4)), 0.5)


class TestYesNoQuestion(unittest.TestCase):
    def test__str__(self) -> None:
        q = YesNoQuestion(4, "Really?")
        self.assertEqual(str(q), "4: Really? (Yes / No)\n")

    def test_validate_answer(self) -> None:
        q = YesNoQuestion(4, "Really?")
        self.assertTrue(q.validate_answer(Answer(True)))
        self.assertFalse(q.validate_answer(Answer(4)))

    def test_get_similarity(self) -> None:
        q = YesNoQuestion(4, "Really?")
        self.assertEqual(q.get_similarity(Answer(True), Answer(True)), 1.0)
        self.assertEqual(q.get_similarity(Answer(False), Answer(True)), 0.0)


class TestAnswer(unittest.TestCase):
    def test_is_valid(self) -> None:
        q = YesNoQuestion(4, "Really?")
        self.assertFalse(Answer(4).is_valid(q))
        self.assertTrue(Answer(True).is_valid(q))


class TestSurvey(unittest.TestCase):
    _survey: Survey
    _q1: Question
    _q2: Question

    def setUp(self) -> None:
        self._q1 = NumericQuestion(1, "How many?", 0, 5)
        self._q2 = YesNoQuestion(2, "Really?")
        self._survey = Survey([self._q1, self._q2])

    def test__len__(self) -> None:
        self.assertEqual(len(self._survey), 2)

    def test__contains__(self) -> None:
        self.assertIn(self._q1, self._survey)
        self.assertIn(self._q2, self._survey)

    def test__str__(self) -> None:
        self.assertEqual(str(self._survey), "1: How many? (0 - 5)\n\n2: Really? (Yes / No)\n\n")

    def test_get_questions(self) -> None:
        self.assertEqual(self._survey.get_questions(), [self._q1, self._q2])

    def test_get_criterion(self) -> None:
        self.assertTrue(isinstance(self._survey._get_criterion(self._q1), HomogeneousCriterion))

    def test_get_weight(self) -> None:
        self.assertEqual(self._survey._get_weight(self._q1), 1)

    def test_set_weight(self) -> None:
        self._survey.set_weight(2, self._q1)
        self.assertEqual(self._survey._get_weight(self._q1), 2)

    def test_set_criterion(self) -> None:
        self._survey.set_criterion(HeterogeneousCriterion(), self._q2)
        self.assertTrue(isinstance(self._survey._get_criterion(self._q2), HeterogeneousCriterion))

    def test_score_students(self) -> None:
        ted = Student(1, "Ted")
        fred = Student(2, "Fred")
        ted.set_answer(self._q1, Answer(2))
        fred.set_answer(self._q1, Answer(3))
        ted.set_answer(self._q2, Answer(True))
        fred.set_answer(self._q2, Answer(True))
        self.assertEqual(self._survey.score_students([ted, fred]), 0.9)


class TestGroup(unittest.TestCase):
    _ted: Student
    _fred: Student
    _jack: Student
    _bob: Student

    def setUp(self) -> None:
        self._ted = Student(1, "Ted")
        self._fred = Student(2, "Fred")
        self._jack = Student(3, "Jack")
        self._bob = Student(4, "Bob")

    def test__len__(self) -> None:
        group = Group([self._ted, self._fred, self._jack, self._bob])
        self.assertEqual(len(group), 4)

    def test__contains__(self) -> None:
        group = Group([self._ted, self._fred, self._jack, self._bob])
        self.assertIn(self._ted, group)
        self.assertNotIn(Student(5, "Amy"), group)

    def test__str__(self) -> None:
        group = Group([self._ted, self._fred, self._jack, self._bob])
        self.assertEqual(str(group), "Ted Fred Jack Bob")

    def test_get_members(self) -> None:
        group = Group([self._ted, self._fred, self._jack, self._bob])
        self.assertEqual(group.get_members(), [self._ted, self._fred, self._jack, self._bob])


class TestGrouping(unittest.TestCase):
    _ted: Student
    _fred: Student
    _jack: Student
    _bob: Student

    def setUp(self) -> None:
        self._ted = Student(1, "Ted")
        self._fred = Student(2, "Fred")
        self._jack = Student(3, "Jack")
        self._bob = Student(4, "Bob")

    def test__len__(self) -> None:
        grouping = Grouping()
        grouping.add_group(Group([self._ted, self._fred]))
        self.assertEqual(len(grouping), 1)

    def test__str__(self) -> None:
        grouping = Grouping()
        grouping.add_group(Group([self._ted, self._fred]))
        grouping.add_group(Group([self._jack, self._bob]))
        self.assertEqual(str(grouping), "Ted Fred\nJack Bob\n")

    def test_add_group(self) -> None:
        grouping = Grouping()
        self.assertTrue(grouping.add_group(Group([self._ted, self._fred])))
        self.assertFalse(grouping.add_group(Group([self._fred, self._jack])))

    def test_get_groups(self) -> None:
        grouping = Grouping()
        group1 = Group([self._ted, self._fred])
        group2 = Group([self._jack, self._bob])
        grouping.add_group(group1)
        grouping.add_group(group2)

        self.assertEqual(grouping.get_groups(), [group1, group2])


class TestHomogeneousCriterion(unittest.TestCase):
    def test_score_answers(self) -> None:
        q = YesNoQuestion(1, "Really?")
        criterion1 = HomogeneousCriterion()
        self.assertEqual(round(criterion1.score_answers(q, [Answer(True), Answer(True), Answer(False)]), 2), 0.33)


class TestHeterogeneousCriterion(unittest.TestCase):
    def test_score_answers(self) -> None:
        q = YesNoQuestion(1, "Really?")
        criterion1 = HeterogeneousCriterion()
        self.assertEqual(round(criterion1.score_answers(q, [Answer(True), Answer(True), Answer(False)]), 2), 0.67)


class TestLonelyMemberCriterion(unittest.TestCase):
    def test_score_answers(self) -> None:
        q = YesNoQuestion(1, "Really?")
        criterion1 = LonelyMemberCriterion()
        self.assertEqual(round(criterion1.score_answers(q, [Answer(True), Answer(True), Answer(False)]), 2), 0.0)


class TestAlphaGrouper(unittest.TestCase):
    def test_make_grouping(self) -> None:
        ted = Student(1, "Ted")
        fred = Student(2, "Fred")
        jack = Student(3, "Jack")
        bob = Student(4, "Bob")

        course1 = Course("CSC148")
        course1.enroll_students([ted, fred, jack, bob])

        q = YesNoQuestion(1, "Really?")
        survey1 = Survey([q])

        grouper1 = AlphaGrouper(2)
        grouping = grouper1.make_grouping(course1, survey1)

        self.assertIn(bob, grouping.get_groups()[0])
        self.assertIn(fred, grouping.get_groups()[0])
        self.assertIn(jack, grouping.get_groups()[1])
        self.assertIn(ted, grouping.get_groups()[1])


class TestSliceAndWindows(unittest.TestCase):
    def test_slice_list(self) -> None:
        lst = [3, 4, 6, 2, 3]
        self.assertEqual(slice_list(lst, 2), [[3, 4], [6, 2], [3]])

    def test_windows(self) -> None:
        lst = [3, 4, 6, 2, 3]
        self.assertEqual(windows(lst, 2), [[3, 4], [4, 6], [6, 2], [2, 3]])


class TestRandomGrouper(unittest.TestCase):
    def test_make_grouping(self) -> None:
        ted = Student(1, "Ted")
        fred = Student(2, "Fred")
        jack = Student(3, "Jack")
        bob = Student(4, "Bob")

        course1 = Course("CSC148")
        course1.enroll_students([ted, fred, jack, bob])

        q = YesNoQuestion(1, "Really?")
        survey1 = Survey([q])

        grouper1 = RandomGrouper(2)
        grouping = grouper1.make_grouping(course1, survey1)

        self.assertEqual(len(grouping.get_groups()[0]), 2)
        self.assertEqual(len(grouping.get_groups()[1]), 2)

        for student in grouping.get_groups()[0].get_members():
            self.assertNotIn(student, grouping.get_groups()[1])
        for student in grouping.get_groups()[1].get_members():
            self.assertNotIn(student, grouping.get_groups()[0])


class TestGreedyGrouper(unittest.TestCase):
    def test_make_grouping(self) -> None:
        ted = Student(1, "Ted")
        fred = Student(2, "Fred")
        jack = Student(3, "Jack")
        bob = Student(4, "Bob")

        course1 = Course("CSC148")
        course1.enroll_students([ted, fred, jack, bob])

        q = YesNoQuestion(1, "Really?")
        survey1 = Survey([q])

        ted.set_answer(q, Answer(True))
        fred.set_answer(q, Answer(False))
        jack.set_answer(q, Answer(True))
        bob.set_answer(q, Answer(False))

        grouper1 = GreedyGrouper(2)
        grouping = grouper1.make_grouping(course1, survey1)

        self.assertIn(ted, grouping.get_groups()[0])
        self.assertIn(jack, grouping.get_groups()[0])
        self.assertIn(fred, grouping.get_groups()[1])
        self.assertIn(bob, grouping.get_groups()[1])


class TestWindowGrouper(unittest.TestCase):
    def test_make_grouping(self) -> None:
        ted = Student(1, "Ted")
        fred = Student(2, "Fred")
        jack = Student(3, "Jack")
        bob = Student(4, "Bob")

        course1 = Course("CSC148")
        course1.enroll_students([ted, fred, jack, bob])

        q = YesNoQuestion(1, "Really?")
        survey1 = Survey([q])

        ted.set_answer(q, Answer(True))
        fred.set_answer(q, Answer(False))
        jack.set_answer(q, Answer(False))
        bob.set_answer(q, Answer(True))

        grouper1 = WindowGrouper(2)
        grouping = grouper1.make_grouping(course1, survey1)

        self.assertIn(fred, grouping.get_groups()[0])
        self.assertIn(jack, grouping.get_groups()[0])
        self.assertIn(ted, grouping.get_groups()[1])
        self.assertIn(bob, grouping.get_groups()[1])


if __name__ == '__main__':
    pytest.main(['tests.py'])
