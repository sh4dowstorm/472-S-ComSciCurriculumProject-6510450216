import fitz, re
from ..models import Enrollment, User, Course
from django.core.exceptions import ObjectDoesNotExist

class OCRService():
    def __init__(self):
        self.courses = {course.course_id: course for course in Course.objects.all()}
        self.semester_mapping = {"Summer":0, "First":1, "Second":2}
        
    def extract_text_from_pdf(self, file_path):
        with open(file_path, 'rb') as file:
            doc = fitz.open(file)
            text = ""
            for page in doc:
                text += page.get_text("text") + "\n"
            return text.split("\n")
        
    def get_student_info(self, text):
        student_info = {}
        recent_year = None
        recent_semester = None
        
        for i, item in enumerate(text):
            match = re.match(r"\s*STUDENT ID\s+(\d{10})", item)
            if match:
                student_info["id"] = match.group(1)
            
            match = re.match(r"\s*NAME\s+(.+)", item)
            if match:
                student_info["name"] = match.group(1)
                
            match = re.match(r"\s*FACULTY OF\s+(.+)", item)
            if match:
                student_info["faculty"] = match.group(1)
            
            match = re.match(r"\s*FIELD OF STUDY\s+(.+)", item)
            if match:
                student_info["field"] = match.group(1)
                
            match = re.match(r"\s*DATE OF ADMISSION\s+(.+)", item)
            if match:
                student_info["start_year"] = int(match.group(1).split()[2]) + 543
            
            semester_match = re.match(r"\s*(First|Second)( Semester| Summer Session) (\d{4})", item)
            if semester_match:
                semester = self.semester_mapping.get(semester_match.group(1), None)
                year = int(semester_match.group(3)) + 543
                
                if not recent_year or (year > recent_year) or (semester > recent_semester):
                    recent_year = year
                    recent_semester = semester
                    
        if recent_year and recent_semester:
            student_info["recent_year"] = recent_year
            student_info["recent_semester"] = recent_semester
                
        return student_info
    
    def extract_receipt_info(self, text):
        receipt_info = {}
        text_str = " ".join(text)
        
        student_id_match = re.search(r"\b(\d{10})\b", " ".join(text))
        receipt_info["id"] = student_id_match.group(1) 

        name_index = text.index("STUDENT NAME") + 2 # +2 for ENG name
        receipt_info["name"] = text[name_index]
        
        academic_year_match = re.search(r"(\d{4}),\s*ภาค(?:ปลาย|ต้น)", " ".join(text))
        receipt_info["year"] = academic_year_match.group(1) 

        semester_match = re.search(r"(First|Second)( Semester| Summer Session)", " ".join(text))
        receipt_info["semester"] = self.semester_mapping.get(semester_match.group(1), None) 

        total_fee_match = re.search(r"รวม\s*/\s*TOTAL\s+([\d,]+.\d{2})", " ".join(text))
        receipt_info["total_fee"] = total_fee_match.group(1) 

        payment_keywords = {
            "Bank": "ธนาคาร",
            "Student Loan": "เงินกู้",
            "Cashier": "แคชเชียร์เช็ค",
            "Credit": "บัตรเครดิต",
            "Cash": "เงินสด",
            "Scholarship": "ทุนการศึกษา",
            "Org. Project": "ผ่านโครงการ"
        }

        found_payment_method = None
        for eng, thai in payment_keywords.items():
            if thai in text_str or eng in text_str:
                found_payment_method = eng
                break

        receipt_info["payment_method"] = found_payment_method

        return receipt_info
        
    def extract_semester(self, item):
        semester_match = re.match(r"(First|Second) Semester (\d{4})", item)
        summer_match = re.match(r"(First|Second)* Summer Session (\d{4})", item)
        
        if semester_match:
            term, year = semester_match.groups()
            return f"{1 if term == 'First' else 2}/{int(year) + 543}"
        elif summer_match:
            _, year = summer_match.groups()
            return f"0/{int(year) - 1 + 543}"
        return None
            
    def extract_course_info(self, text, user):
        count = 0
        course_data = {}
        current_semester = None

        i = 0
        while i < len(text):
            item = text[i].strip()
            
            semester = self.extract_semester(item)
            if semester:
                current_semester = semester
                course_data.setdefault(current_semester, {})

            # match course id and course name
            course_match = re.match(r"(\d{8})\s+(.+)", item) 
            if course_match and current_semester:
                course_id = course_match.group(1)

                # ถ้าไม่มีเกรดข้ามเรื่อยๆจนกว่าจะเจอเกรด
                grading = None
                j = i + 1
                while j < len(text):
                    next_item = text[j].strip()
                    if next_item in ['A', 'B', 'B+', 'C', 'C+', 'D', 'D+', 'F', 'P', 'NP', 'N']:
                        grading = next_item
                        break
                    j += 1  

                if grading:
                    course = self.courses.get(course_id)
                    course_data[current_semester][course_id] = grading # for debug
                    count += 1
                    if course:
                        s, y = current_semester.split('/')
                        try:
                            Enrollment.objects.create(
                                semester=s, 
                                year=y, grade=grading, 
                                user_fk=user, 
                                course_fk=self.courses[course_id]
                            )
                        except ObjectDoesNotExist:
                            print(f"course with course_id {course_id} not found.")
            i += 1  

        print("Total courses:", count)
        return course_data
    
    def get_activiy_status(self, text, uid):
        id_match = re.match(r".+\s+(\d{10})", text[1])
        
        if id_match:
            matched_uid = id_match.group(1)
            
            if matched_uid == uid:
                try:
                    User.objects.get(student_code=uid)
                
                    if "PASS" in text:
                        return True
                    else:
                        return False
                except ObjectDoesNotExist:
                    print(f"User with student_code {uid} not found.")
                    return False
            else:
                return False
        return False
    
        

        
