from typing import Dict, List
from ..models import Enrollment


class CalculatorService() :
    def __init__(self):
        pass
    
    def __str__(self):
        pass
    
    def GPACalculate(self, stEnrollments: List[Enrollment]) -> List[Enrollment] :
        
        calculatedEnrollments :Dict[str, Enrollment] = {}
        encounter :Dict[str, int] = {}
        
        for enrollment in stEnrollments :
            key = enrollment.course_id.course_id
            if calculatedEnrollments.get(key) :
                calculatedEnrollments[key].grade += enrollment.grade
                
            else :
                calculatedEnrollments[key] = enrollment
                encounter[key] = 0
                
            encounter[key] += 1
            
        for key in list(calculatedEnrollments.keys()) :
            calculatedEnrollments[key].grade /= encounter[key]
            
        return list(calculatedEnrollments.values())
        