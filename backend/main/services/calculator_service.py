from typing import Dict, List
from ortools.linear_solver import pywraplp

from ..models.subcategory import Subcategory
from ..models import Enrollment


class CalculatorService() :
    def __init__(self):
        pass
    
    def __str__(self):
        pass
    
    def GPACalculate(self, stEnrollments: List[Enrollment]) -> List[Enrollment] :
        """calculate final gpa for duplicate subject

        Args:
            stEnrollments (List[Enrollment]): study result for each student (with duplicate course)

        Returns:
            List[Enrollment]: final study result grade (with no duplicate course)
        """
        
        calculatedEnrollments :Dict[str, Enrollment] = {}
        encounter :Dict[str, int] = {}
        
        for enrollment in stEnrollments :
            key = enrollment.course_fk.course_id
            if calculatedEnrollments.get(key) :
                # if duplicate course will add total grade
                calculatedEnrollments[key].grade += enrollment.grade
                
            else :
                # if first encounter add fresh data
                calculatedEnrollments[key] = enrollment
                encounter[key] = 0
                
            encounter[key] += 1
            
        # averaging the gpa for every courses
        for key in list(calculatedEnrollments.keys()) :
            calculatedEnrollments[key].grade /= encounter[key]
            
        return list(calculatedEnrollments.values())
        
    def map(self, subcategories: List[Subcategory], enrollments: List[Enrollment]) :
        """mapping and categorize the studied courses to categories

        Args:
            subcategories (List[Subcategory]): all category from course curriculum
            enrollments (List[Enrollment]): all studied course of user

        Returns:
            map[str, List]: object of {free elective, categorize courses}
        """
        
        result = {'free elective': [], 'categorize course': []}
        
        mappedEnrollments = self.categorizeSubject(subcategories=subcategories, enrollments=enrollments)
            
        for mappedEnrollment in mappedEnrollments.values() :
            if mappedEnrollment['subcategory'].subcateory_min_credit < mappedEnrollment['sumCredit'] :
                # เกลี่ยรายวิชา
                formatedData = {course.course_fk.course_id: self.convertEnrollment(course) for course in mappedEnrollment['matchEnrollment'].values()}
                optimalAns = self.optimization('SAT', formatedData, mappedEnrollment['subcategory'].subcateory_min_credit)
                
                if not optimalAns :
                    optimalAns = self.optimization('GLOP', formatedData, mappedEnrollment['subcategory'].subcateory_min_credit)
                    
                for courseId, selection in optimalAns :
                    if selection == 0 :
                        removedCourse = mappedEnrollment['matchEnrollment'].pop(courseId)
                        result['free elective'].append(removedCourse)

            result['categorize course'].append(mappedEnrollment)
                        
        return result
    
    def categorizeSubject(self, subcategories: List[Subcategory], enrollments: List[Enrollment]) -> map :
        """categorize the studied courses match with subcategories

        Args:
            subcategories (List[Subcategory]): subcategories from course curriculum
            enrollments (List[Enrollment]): studied courses of user

        Raises:
            RuntimeError: user have been studied in course that not in user's curriculum year

        Returns:
            map: group of {subcategory, match courses, total credit}
        """
        
        mappedEnrollments = {
            subcategory.subcategory_name: {'subcategory': subcategory, 'matchEnrollment':{}, 'sumCredit':0} for subcategory in subcategories
        }
        
        for enrollment in enrollments :
            subcategoryName = enrollment.course_fk.subcategory_fk.subcategory_name
            matchSubcategory = mappedEnrollments.get(subcategoryName)
            if matchSubcategory :
                matchSubcategory['matchEnrollment'][enrollment.course_fk.course_id] = enrollment
                matchSubcategory['sumCredit'] += enrollment.course_fk.credit
            else :
                raise RuntimeError('inserted enrollment got unexpexted subject or category')

        return mappedEnrollments
        
    def convertEnrollment(self, enrollment: Enrollment) -> map :
        """grouping data of studied course

        Args:
            enrollment (Enrollment): studied course of user

        Returns:
            map: data mapping object
        """
        
        return {
            'enrollment': enrollment,
            'credit': enrollment.course_fk.credit,
            'courseId': enrollment.course_fk.course_id,
        }
        
    def optimization(self, model: str, convertedEnrollment: map, minCredit: int) -> List[tuple[str, int]]|None :
        """to optimize fitting studied course to the curriculum category

        Args:
            model (str): SAT (integer solver), GLOP (linear solver)
            convertedEnrollment (map): studied course data
            minCredit (int): minimum credit must take in curriculum course

        Returns:
            List[tuple[str, int]]|None: (course, decision) is telling that course will be choose to be in subcategory or None if problem not feasible
        """
        
        print('\nSolver =', model)
        # linear programming solver
        solver: pywraplp.Solver = pywraplp.Solver.CreateSolver(model)
        
        # variable
        variables = [solver.IntVar(0, 1, enrollment['enrollment'].course_fk.course_id) for enrollment in convertedEnrollment.values()]
        
        # constraint
        constraint = sum([v*convertedEnrollment[v.name()]['credit'] for v in variables])
        print('\nConstrain =', constraint)        
        
        solver.Add(constraint == minCredit)
        
        # objective   
        objective = sum([v for v in variables])
        solver.Maximize(objective)
        
        status = solver.Solve()
        
        if status == pywraplp.Solver.OPTIMAL :
            print("\nSolution:")
            print(f"Objective value = {solver.Objective().Value():0.1f}")
            for v in variables :
                print(f"{v.name()} = {v.solution_value():0.1f}")
                
            return [(v.name(), round(v.solution_value())) for v in variables]
                
        else :
            print('this problem does not have an optimal solution.')
            return None