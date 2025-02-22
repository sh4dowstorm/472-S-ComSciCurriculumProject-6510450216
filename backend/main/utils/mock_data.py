from typing import List
from ..models import User, Curriculum, Category, Subcategory, Course, Enrollment


def mockUser() -> User :
    return User.objects.create(
        email='abc@gmail.com',
        password='1234',
        name='doe',
        student_code='6510450000',
        role=User.Role.STUDENT,
    )
    
def mockCurriculum() -> Curriculum :
    return Curriculum.objects.create(
        curriculum_name='หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาวิทยาการคอมพิวเตอร์',
        total_credit=124,
        curriculum_year=2565,
    )
    
def mockCategories(curriculum: Curriculum) -> List[Category] :
    return [
        Category.objects.create(
            category_name='หมวดวิชาศึกษาทั่วไป',
            category_min_credit=4,
            curriculum_fk=curriculum,
        ),
        Category.objects.create(
            category_name='หมวดวิชาเสรี',
            category_min_credit=3,
            curriculum_fk=curriculum,
        ),   
    ]
    
def mockSubcategories(category: Category, name_and_credit: List[tuple]) -> List[Subcategory] :
    return [
        Subcategory.objects.create(
            subcategory_name=name,
            subcateory_min_credit=credit,
            category_fk=category,
        )
        for name, credit in name_and_credit
    ]
    
def mockCourses(subcategory: Subcategory, credits: List[int]) -> List[Course] :
    return [
        Course.objects.create(
            course_id=str(i),
            credit=credits[i],
            course_name_th=f'วิชา {ord("A") + i}',
            course_name_en=f'subject {ord("A") + i}',
            subcategory_fk=subcategory,
        )
        for i in range(len(credits))
    ]
    
def mockEnrollments(user: User, course_and_grade_and_year: List[tuple[Course, float, int]]) :
    return [
        Enrollment.objects.create(
            semester=Enrollment.Semester.FIRST,
            year=year,
            user_fk=user,
            course_fk=course,
            grade=grade,
        )
        for course, grade, year in course_and_grade_and_year
    ]