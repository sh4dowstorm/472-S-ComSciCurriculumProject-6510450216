# signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.db import transaction
from django.conf import settings
from pathlib import Path
from .models import Curriculum, Category, Subcategory
import json
import re
import os

def clean_title(text): 
    return re.sub(r'^\d+\.|\s*:$', '', text).strip()

def extract_number(text): 
    return int(re.search(r'\d+', text).group()) if re.search(r'\d+', text) else 0

def map_long_subtitle(text): 
    return "และเลือกเรียนรายวิชาใน 5 กลุ่มสาระ" if text.startswith("และเลือกเรียนรายวิชาใน 5 กลุ่มสาระ") else text

def import_curriculum_from_json(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        curriculum_content = data.get("curriculum", {}).get("content", [])
        course_structures = data.get("course_structures", [])

    # Extract curriculum info
    curriculum_name = ""
    total_credits = 0
    curriculum_year = 0

    for content in curriculum_content:
        heading = content['heading']
        if heading == "รหัสและชื่อหลักสูตร":
            curriculum_name = content['description'][1]
        elif heading == "จำนวนหน่วยกิตที่เรียนตลอดหลักสูตร":
            total_credits = extract_number(content['headingDescription'])
        elif heading == "สถานภาพของหลักสูตร":
            curriculum_year = int(content['description'][0].split()[-1])

    # Create Curriculum
    curriculum = Curriculum.objects.create(
        curriculum_name=curriculum_name,
        total_credit=total_credits,
        curriculum_year=curriculum_year
    )

    # Process course structures
    for name in course_structures:
        for content in name['content']:
            if content['heading'] == "โครงสร้างหลักสูตร :":
                for structure in content['structure']:
                    category = Category.objects.create(
                        curriculum_id_id=curriculum.curriculum_id,
                        category_name=clean_title(structure['title']),
                        category_min_credit=extract_number(structure['description'])
                    )
                    
                    for subsection in structure.get('subsections', []):
                        Subcategory.objects.create(
                            category_id_id=category.category_id,
                            subcategory_name=map_long_subtitle(clean_title(subsection['subtitle'])),
                            subcateory_min_credit=extract_number(subsection['details'])
                        )

@receiver(post_migrate)
def initialize_curriculum_data(sender, **kwargs):
    if sender.name == 'main':  # Replace with your app name
        # Check if data already exists
        if Curriculum.objects.exists():
            return

        # Get the path to the data directory
        data_dir = Path(__file__).resolve().parent / 'data'
        
        # Process all JSON files in the data directory
        with transaction.atomic():
            for json_file in data_dir.glob('*.json'):
                try:
                    import_curriculum_from_json(json_file)
                    print(f"Successfully imported data from {json_file.name}")
                except Exception as e:
                    print(f"Error importing {json_file.name}: {str(e)}")