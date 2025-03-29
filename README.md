# ComSciCurriculumProject

## This repository creates for senior project Integrated Agile Process and Devops_01418472-65.

This project is about checking the criteria of students to confirm graduation. The check will include 
1. academic transcripts
2. academic debt payment forms 
3. graduation applications
4. activity sheets (optional).

# How to activate frontend
To activate frontend run the following command
> suggest using git bash
1. `cd frontend/`
2. `npm install`
3. `npm run dev`

# How to activate backend

To activate backend run the following command 
> suggest using git bash

### run server database using docker
1. `docker-compose up -d`
> suggest using seperate terminal

### inspect direct to the database
1. `docker exec -it cs_curriculum bin/bash`
2. `mysql -uroot -p1234`
3. `use cs_curriculum`
4. now you can access directly to the database

### access database via phpmyadmin
1. Go to `http://127.0.0.1:8080/`
    - username : root
    - password : 1234

> [!IMPORTANT]
> Python version should be (or more than) 3.10.x

### setup environment
1. `python -m venv .venv`
2. __activate virtual environment__ -> `source .venv/Scripts/activate`
3. `cd ./backend`
4. `pip install -r requirement.txt`
5. `cp ../.env.example .env`
6. `python backend/manage.py makemigrations`
7. `python backend/manage.py migrate`

### run server
1. `python backend/manage.py runserver`

### deactivate backend program
1. `docker compose down`
2. `deactivate` in terminal using virtual environment

### email for sending OTP code
1. `EMAIL_HOST_USER = 'xxxxxxxxxx@gmail.com'` change the email
2. `EMAIL_HOST_PASSWORD = 'xxxxxxxxxxxxxxxx'` change the app password (get the app password from google account)

### how to do unit testing
1. `cd backend`
2. `pytest -sv`

> `-s` flag is to show console printing </br>
> `-v` flag is to show detail

---

# Agile & DevOps 01418472

## ชื่อเว็บไซต์: ComSci Curriculum Project 
## วัตถุประสงค์
ต้องการจะยื่นเอกสารต่างๆในการขอจบการศึกษาทำให้เจ้าหน้าที่ภาคต้องใช้เวลามากในการตรวจสอบเอกสารของนิสิตทุกคนจึงเกิดมาเป็น Project นี้ที่จะทำให้ใช้เวลาในการตรวจสอบเอกสารต่างๆที่ใช้ในการยื่นจบการศึกษาได้รวดเร็วมากยิ่งขึ้น
## ชื่อกลุ่ม: Sad-Boi
### ชื่อสมาชิก

| ชื่อ-นามสกุล | รหัสนิสิต | หมู่เรียน | ชั้นปี
| --- | --- | --- | --- |
| คณิศร ศรีสว่าง | 6510450216 | 200 | 3 | 
| ไชยภัทร ศรีอำไพ | 6510450305 | 200 | 3 |
| ปณิธาน จำปาหอม | 6510450569 | 200 | 3 |
| มรฑป เฮงประเสริฐ | 6510450861 | 200 | 3 |

<br></br>
| ชื่อ-นามสกุล | Feature ที่รับผิดชอบ 
| --- | --- |
| คณิศร ศรีสว่าง | @sh4dowstorm Feat: [Upload File](https://github.com/Bi-Ma-GOoOD/ComSciCurriculumProject/tree/feature/upload-file-devops)
| ไชยภัทร ศรีอำไพ | @MoreINV8 Feat: [Curriculum Calculate](https://github.com/Bi-Ma-GOoOD/ComSciCurriculumProject/tree/feature/calculate_credit-devops), [Curriculum Calculate Display](https://github.com/Bi-Ma-GOoOD/ComSciCurriculumProject/tree/feature/curriculum_progress-devops)
| ปณิธาน จำปาหอม | @panithan-doe ${\color{red}(Product Owner)}$
| มรฑป เฮงประเสริฐ | @moradoph Feat: [OCR File](https://github.com/Bi-Ma-GOoOD/ComSciCurriculumProject/tree/feature/ocr-devops), [Extracted Text Processing](https://github.com/Bi-Ma-GOoOD/ComSciCurriculumProject/tree/feature/extracted-text-processing-devops)



<br></br>
---

## ชื่อกลุ่ม: OIIAIIOIIIAI
### ชื่อสมาชิก

| ชื่อ-นามสกุล | รหัสนิสิต | หมู่เรียน | ชั้นปี
| --- | --- | --- | --- |
| กิตติธัช เข่งพิมล | 6510450208 | 200 | 3 | 
| พิชญ์ชนก คงสมปรีดิ์ | 6510450739 | 200 | 3 |
| ภาณุวิชญ์ สังข์ธูป | 6510450798 | 200 | 3 |

<br></br>
| ชื่อ-นามสกุล | Feature ที่รับผิดชอบ 
| --- | --- |
| กิตติธัช เข่งพิมล | @kktopkk  ${\color{red}(Product Owner)}$
| พิชญ์ชนก คงสมปรีดิ์ | @Pichanokk Feat: [ชื่อฟีเจอร์](url-link)
| ภาณุวิชญ์ สังข์ธูป | @panuwit89 Feat: [ชื่อฟีเจอร์](url-link)
