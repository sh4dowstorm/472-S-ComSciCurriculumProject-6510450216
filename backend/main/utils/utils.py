import uuid

from ..models import Form, VerificationResult, CreditDetail, SubcategoryDetails, NotPassCourse, Enrollment
from ..minio_client import delete_from_minio

UNIVERSITY_SUBCATEGORY = [
    'กลุ่มสาระอยู่ดีมีสุข',
    'กลุ่มสาระศาสตร์แห่งผู้ประกอบการ',
    'กลุ่มสาระภาษากับการสื่อสาร',
    'กลุ่มสาระสุนทรียศาสตร์',
    'กลุ่มสาระพลเมืองไทยและพลเมืองโลก',
]

FIVE_UNIVERSITY_SUBCATEGORY = 'และเลือกเรียนรายวิชาใน 5 กลุ่มสาระ'

def getGrade(charGrade: str) -> tuple[float|None, str|None] :
    charGrade = charGrade.upper()
    
    if charGrade == 'A' :
        return 4.0, None
    elif charGrade == 'B+' :
        return 3.5, None
    elif charGrade == 'B' :
        return 3.0, None
    elif charGrade == 'C+' :
        return 2.5, None
    elif charGrade == 'C' :
        return 2.0, None
    elif charGrade == 'D+' :
        return 1.5, None
    elif charGrade == 'D' :
        return 1.0, None
    elif charGrade == 'F' :
        return 0.0, None
    
    return None, charGrade

def resetForm(uid: uuid.UUID) :
    # get form
    form = Form.objects.get(user_fk=uuid.UUID(uid))
    
    # get verification result
    vr = VerificationResult.objects.get(form_fk=form.form_id)
    
    # get credit detail
    cd = CreditDetail.objects.get(verification_result_fk=vr.verification_result_id)
    
    SubcategoryDetails.objects.filter(credit_detail_fk=cd.credit_details_id).delete()
    NotPassCourse.objects.filter(credit_detail_fk=cd.credit_details_id).delete()
    Enrollment.objects.filter(user_fk=uid).delete()
    
    cd.delete()
    vr.delete()
    
    form.form_status = Form.FormStatus.DRAFT
    form.form_type = Form.FormType.GRADUATION_CHECK
    form.save()
    
    # TODO: delete files
    try :
        delete_from_minio(str(form.form_id))
    except Exception as e :
        print(e)
        
    return 'Delete success'