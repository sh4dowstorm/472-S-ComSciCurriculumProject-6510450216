import fitz
import re

from ..models import Enrollment, User, Course

class OCRService(): 
    # def extract_course_info(self, text, user_id):
    #     count = 0
    #     course_data = {}
    #     current_semester = None

    #     user = User.objects.get(pk=user_id)

    #     i = 0
    #     while i < len(text):
    #         item = text[i].strip()
            
    #         semester_match = re.match(r"(First|Second) Semester (\d{4})", item)
    #         summer_match = re.match(r"(First|Second)* Summer Session (\d{4})", item)

    #         if semester_match:
    #             term, year = semester_match.groups()
    #             current_semester = (1 if term == 'First' else 2, int(year)+543)
    #             course_data.setdefault(current_semester, {})

    #         elif summer_match:
    #             term, year = summer_match.groups()
    #             current_semester = (0, int(year)-1+543) # -1 จากปีที่แสดงใน pdf ภาษาอังกฤษที่จะแสดงว่าเรียนในปีไหนแทนที่จะเป็นปีการศึกษา
    #             course_data.setdefault(current_semester, {})

    #         # match course id and course name
    #         course_match = re.match(r"(\d{8})\s+(.+)", item) 
    #         if course_match and current_semester:
    #             course_id = course_match.group(1)

    #             # ถ้าไม่มีเกรดข้ามเรื่อยๆจนกว่าจะเจอเกรด
    #             grade = None
    #             j = i + 1
    #             while j < len(text):
    #                 next_item = text[j].strip()
    #                 if next_item in ['A', 'B', 'B+', 'C', 'C+', 'D', 'D+', 'F', 'P', 'NP', 'N']:
    #                     grade = next_item
    #                     break
    #                 j += 1  

    #             if grade:
    #                 course_data[current_semester][course_id] = grade
    #                 count += 1

    #                 course = Course.objects.get(course_id=course_id)
    #                 enrollment = Enrollment(
    #                     semester=current_semester[0],
    #                     year=current_semester[1],
    #                     grade=grade if grade not in ['P', 'NP', 'N'] else None,
    #                     user_fk=user,
    #                     course_fk=course
    #                 )
    #                 # enrollment.save()
    #         i += 1  
            
    #     print("Total courses:", count)
    #     print(enrollment)
    #     return course_data
    
    def extract_course_info(self, text):
        count = 0
        course_data = {}
        current_semester = None

        i = 0
        while i < len(text):
            item = text[i].strip()
            
            semester_match = re.match(r"(First|Second) Semester (\d{4})", item)
            summer_match = re.match(r"(First|Second)* Summer Session (\d{4})", item)

            if semester_match:
                term, year = semester_match.groups()
                current_semester = f"{1 if term == 'First' else 2}/{int(year)+543}"
                course_data.setdefault(current_semester, {})

            elif summer_match:
                term, year = summer_match.groups()
                current_semester = f"S/{int(year)-1+543}"
                course_data.setdefault(current_semester, {})

            # match course id and course name
            course_match = re.match(r"(\d{8})\s+(.+)", item) 
            if course_match and current_semester:
                course_id = course_match.group(1)

                # ถ้าไม่มีเกรดข้ามเรื่อยๆจนกว่าจะเจอเกรด
                grade = None
                j = i + 1
                while j < len(text):
                    next_item = text[j].strip()
                    if next_item in ['A', 'B', 'B+', 'C', 'C+', 'D', 'D+', 'F', 'P', 'NP', 'N']:
                        grade = next_item
                        break
                    j += 1  

                if grade:
                    course_data[current_semester][course_id] = grade
                    count += 1
            i += 1  
        print("Total courses:", count)
        return course_data

    def get_student_info(self, text):
        student_info = {}
        for i, item in enumerate(text):
            match = re.match(r"\s*STUDENT ID\s+(\d{10})", item)
            if match:
                student_info["ID"] = match.group(1)
            
            match = re.match(r"\s*NAME\s+(.+)", item)
            if match:
                student_info["Name"] = match.group(1)
                
            match = re.match(r"\s*FACULTY OF\s+(.+)", item)
            if match:
                student_info["Faculty"] = match.group(1)
            
            match = re.match(r"\s*FIELD OF STUDY\s+(.+)", item)
            if match:
                student_info["Field"] = match.group(1)
                
            match = re.match(r"\s*DATE OF ADMISSION\s+(.+)", item)
            if match:
                student_info["Start_year"] = int(match.group(1).split()[2]) + 543
                
        return student_info

    def extract_text_from_pdf(self, file_path):
        with open(file_path, 'rb') as file:
            doc = fitz.open(file)
            text = ""
            for page in doc:
                text += page.get_text("text") + "\n"
            return text.split("\n")
        
