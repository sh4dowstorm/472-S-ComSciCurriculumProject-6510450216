from typing import List

from ..models import Curriculum, Enrollment
from ..serializers import CreditVerifySerializer
from .calculator_service import CalculatorService


class EducationEvaluationService() :
    def __init__(self):
        self.caculator = CalculatorService()
        
    def getCurriculumData(self, curriculum: Curriculum, mappingResult, **param) :
        # TODO freeElectiveDetail use only test before query
        # TODO nonElectiveCategoryDetail use only test before query (1. query category)
        # TODO subCategoryDetail use only test before query (2. query subcategory)
        if not (param and param.get('freeElectiveDetail')) : return
        if not (param and param.get('nonElectiveCategoryDetail')) : return # want [ categories, ... ]
        if not (param and param.get('subCategoryDetail')) : return # want { category: [subcategories, ...] }
        
        isComplete = True
        categories = []
        
        subcategoryDetailParam = dict(param.get('subCategoryDetail'))
        # no elective category course
        for category in param.get('nonElectiveCategoryDetail') :
            checked = self.getCategorizeCategoryDetail(
                categorizeCourses=mappingResult['categorize course'],
                categoryDetail=category,
                subcategoriesDetail=subcategoryDetailParam.get(category.category_name),
            )
            isComplete &= checked['isComplete']
            categories.append(checked)
            
        # elective category course
        freeElectiveCheck = self.getFreeElectionCategoryDetal(
            freeElectiveDetail=param.get('freeElectiveDetail'), 
            freeElectiveEnrollment=mappingResult['free elective'],
        )
        isComplete &= freeElectiveCheck['isComplete']
        categories.append(freeElectiveCheck)
        
        return {
            'curriculum': curriculum,
            'isComplete': isComplete,
            'categories': categories,
        }
        
    def getFreeElectionCategoryDetal(self, freeElectiveEnrollment, freeElectiveDetail) :
        studied = []
        totalCredit = 0
        for enrollment in freeElectiveEnrollment :
            totalCredit += enrollment.course_fk.credit
            studied.append({
                'course': enrollment.course_fk,
                'studyResult': enrollment,
            })
        
        return {
            'category': freeElectiveDetail,
            'isComplete': totalCredit >= freeElectiveDetail.category_min_credit,
            'isFreeElective': True,
            'courses_or_subcategories': studied,
        }
        
    def getCategorizeCategoryDetail(self, categorizeCourses, categoryDetail, subcategoriesDetail) :
        categorizeCoursesReformat = {}
        for categorizeCourse in categorizeCourses :
            categorizeCoursesReformat[categorizeCourse['subcategory'].subcategory_name] = list(categorizeCourse['matchEnrollment'].values())
            
        isComplete = True
        subcategories = []
        for subcategory in subcategoriesDetail :
            checked = self.getSubcategoryDetail(subcategory, categorizeCoursesReformat)
            subcategories.append(checked)
            isComplete &= checked['isComplete']
        
        return {
            'category': categoryDetail,
            'isComplete': isComplete,
            'isFreeElective': False,
            'courses_or_subcategories': [
                self.getSubcategoryDetail(subcategory, categorizeCoursesReformat) for subcategory in subcategoriesDetail
            ]
        }
        
    def getSubcategoryDetail(self, subcategory, categorizeCourses) :
        studied = []
        totalCredit = 0
        for enrollment in categorizeCourses[subcategory.subcategory_name] :
            totalCredit += enrollment.course_fk.credit
            studied.append({
                'course': enrollment.course_fk,
                'studyResult': enrollment,
            })
            
        return {
            'subcategory': subcategory,
            'isComplete': totalCredit >= subcategory.subcateory_min_credit,
            'courses': studied,
        }
    
    def verify(self, curriculum: Curriculum, enrollments: List[Enrollment], *args) :
        # TODO: use only in testing
        if not len(args) == 3 :
            return None
        categories, subcategories, courses = args
        
        subcategoriesReformate = {}
        for subcategory in subcategories :
            categoryId = subcategory.category_fk.category_name
            if subcategoriesReformate.get(categoryId) :
                subcategoriesReformate[categoryId].append(subcategory)
            else :
                subcategoriesReformate[categoryId] = [subcategory] 
        
        cleanEnrollment = self.caculator.GPACalculate(enrollments)
        mappingResult = self.caculator.map(subcategories, cleanEnrollment)

        studyResult = self.getCurriculumData(
            curriculum=curriculum,
            mappingResult=mappingResult,
            freeElectiveDetail = categories[1],
            nonElectiveCategoryDetail = [categories[0]],
            subCategoryDetail = subcategoriesReformate,
        )
        
        return CreditVerifySerializer(studyResult)