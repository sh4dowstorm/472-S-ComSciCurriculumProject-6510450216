# ComSciCurriculumProject

## This repository creates for senior project Integrated Agile Process and Devops_01418472-65.

This project is about checking the criteria of students to confirm graduation. The check will include 
1. academic transcripts
2. academic debt payment forms 
3. graduation applications
4. activity sheets (optional).

# How to activate backend

1. `python -m venv .venv`
2. __activate virtual environment__ -> `source .venv/Scripts/activate`
3. `pip install -r requirement.txt`
4. `python backend/cs_curriculum/manage.py migrate`
5. __run server__ -> `python backend/cs_curriculum/manage.py runserver`
6. __deactivate virtual environment__ -> `deactivate`