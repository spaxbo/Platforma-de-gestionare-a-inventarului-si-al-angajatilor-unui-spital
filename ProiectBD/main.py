import datetime
import re

import oracledb
from flask import Flask, render_template, request

app = Flask(__name__)

connection = oracledb.connect(user="bd006", password="ms006", host="81.180.214.85", port=1539, service_name="orcl")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/departments/afisare_departament')
def afisare_departament():
    cursor = connection.cursor()
    date: list[tuple[...]]
    date = cursor.execute("SELECT * FROM DEPARTMENTS ORDER BY DEPARTMENT_ID").fetchall()
    return render_template('/departments/afisare_departament.html', date=date)


@app.route('/departments/modify_dept/<int:dept_id>', methods=["GET", "POST"])
def modify_dept(dept_id: int):
    if request.method == 'POST':
        try:
            cursor = connection.cursor()
            dname = request.form['department_name']
            manager_first = request.form['manager_first_name']
            manager_last = request.form['manager_last_name']

            if re.search(r'\d', dname):
                raise ValueError("Eroare: Numele nu poate contine cifre")
            if re.search(r'\d', manager_first):
                raise ValueError("Eroare: Numele nu poate contine cifre")
            if re.search(r'\d', manager_last):
                raise ValueError("Eroare: Numele nu poate contine cifre")

            cursor.execute("""
            UPDATE DEPARTMENTS 
            SET department_name = :department_name, 
                manager_first_name= :manager_first_name,
                manager_last_name=:manager_last_name
            WHERE department_id = :id
            """, {
                'department_name': dname,
                'manager_first_name': manager_first,
                'manager_last_name': manager_last,
                'id': dept_id
            })
            connection.commit()
            return render_template('/departments/succes_modificare.html')
        except oracledb.DatabaseError as e:
            print(f"Eroare la inserare in baza de date:{str(e)}")
    return render_template('/departments/modify_dept.html')


@app.route('/departments/delete_dept/<int:dept_id>')
def delete_dept(dept_id: int):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM DEPARTMENTS WHERE DEPARTMENT_ID = :dept_id", {'dept_id': dept_id})
    connection.commit()
    return render_template('/departments/succes_stergere.html')


@app.route("/departments/index_dept", methods=['GET', 'POST'])
def department():
    if request.method == 'POST':
        try:
            cursor = connection.cursor()
            dname = request.form['dname']
            manager_last = request.form['manager_last']
            manager_first = request.form['manager_first']

            if re.search(r'\d', dname):
                raise ValueError("Eroare: Numele nu poate contine cifre")
            if re.search(r'\d', manager_first):
                raise ValueError("Eroare: Numele nu poate contine cifre")
            if re.search(r'\d', manager_last):
                raise ValueError("Eroare: Numele nu poate contine cifre")

            cursor.execute("INSERT INTO DEPARTMENTS (department_name,manager_first_name,manager_last_name) "
                           "VALUES (:department_name,:manager_first_name,:manager_last_name)",
                           {'department_name': dname, 'manager_first_name': manager_first,
                            'manager_last_name': manager_last})
            connection.commit()
            return render_template('/departments/succes_inserare.html')
        except oracledb.DatabaseError as e:
            print(f"Eroare la inserare in baza de date:{str(e)}")
    return render_template('/departments/index_dept.html')


@app.route('/doctors/afisare_doctori')
def afisare_doctori():
    cursor = connection.cursor()
    date: list[tuple[...]]
    date = cursor.execute(
        """SELECT D.*,DP.DEPARTMENT_NAME 
    FROM DOCTORS D
    JOIN DEPARTMENTS DP ON D.DEPARTMENT_ID = DP.DEPARTMENT_ID
    ORDER BY D.DOCTOR_ID""").fetchall()
    return render_template('/doctors/afisare_doctori.html', date=date)


@app.route("/doctors/doctors_insert/", methods=['GET', 'POST'])
def doctor():
    cursor = connection.cursor()
    departments = cursor.execute("SELECT * FROM DEPARTMENTS")
    if request.method == 'POST':
        try:
            id_dept = request.form['dept']
            doctor_last = request.form['doctor_last']
            doctor_first = request.form['doctor_first']
            hire_date = request.form['hire_date']
            salary = int(request.form['salary'])

            if re.search(r'\d', doctor_last):
                raise ValueError("Eroare: Numele nu poate contine cifre")
            if re.search(r'\d', doctor_first):
                raise ValueError("Eroare: Numele nu poate contine cifre")
            var = datetime.datetime.now()
            date = datetime.datetime.strptime(hire_date, "%Y.%m.%d")
            if var < date:
                raise ValueError
            if salary < 0:
                raise ValueError("Eroare:Salariul nu poate fi negativ")

            cursor = connection.cursor()

            cursor.execute("""
                           INSERT INTO DOCTORS (doctor_last_name, doctor_first_name, hire_date, salary,department_id)
                           VALUES (:doctor_last_name, :doctor_first_name, TO_DATE(:hire_date, 'YYYY-MM-DD'), :salary,:department_id)
                       """, {'doctor_last_name': doctor_last,
                             'doctor_first_name': doctor_first, 'hire_date': hire_date, 'salary': salary,
                             'department_id': id_dept})

            connection.commit()

        except oracledb.DatabaseError as e:
            print(f"Eroare la inserare in baza de date: {str(e)}")

    return render_template('/doctors/doctors_insert.html', departments=departments)


@app.route('/doctors/delete_doc/<int:doctor_id>')
def delete_doc(doctor_id: int):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM doctors WHERE doctor_id = :doctor_id", {'doctor_id': doctor_id})
    connection.commit()
    return render_template('/doctors/succes_stergere_doc.html')


@app.route('/doctors/modify_doc/<int:doctor_id>', methods=["GET", "POST"])
def modify_doc(doctor_id: int):
    cursor = connection.cursor()
    departments = cursor.execute("SELECT * FROM DEPARTMENTS")
    if request.method == 'POST':
        try:
            cursor = connection.cursor()
            doctor_last = request.form['doctor_last_name']
            doctor_first = request.form['doctor_first_name']
            hire_date = request.form['hire_date']
            salary = int(request.form['salary'])

            if re.search(r'\d', doctor_last):
                raise ValueError("Eroare: Numele nu poate contine cifre")
            if re.search(r'\d', doctor_first):
                raise ValueError("Eroare: Numele nu poate contine cifre")
            var = datetime.datetime.now()
            date = datetime.datetime.strptime(hire_date, "%Y.%m.%d")
            if var < date:
                raise ValueError
            if salary < 0:
                raise ValueError("Eroare:Salariul nu poate fi negativ")

            query1 = """
                       UPDATE doctors
                       SET doctor_last_name = :doctor_last_name,
                           doctor_first_name = :doctor_first_name,
                           hire_date = TO_DATE(:hire_date, 'YYYY-MM-DD'),
                           salary = :salary
                       WHERE doctor_id = :doctor_id
                       """

            cursor.execute(query1, {
                'doctor_last_name': doctor_last,
                'doctor_first_name': doctor_first,
                'hire_date': hire_date,
                'salary': salary,
                'doctor_id': doctor_id
            })

            connection.commit()

            return render_template('/doctors/succes_modificare_doc.html')
        except oracledb.DatabaseError as e:
            print(f"Eroare la inserare in baza de date:{str(e)}")
    return render_template('/doctors/modify_doc.html', departments=departments)


@app.route('/patients/afisare_patients')
def afisare_patients():
    cursor = connection.cursor()
    date: list[tuple[...]]
    date = cursor.execute(
        """SELECT P.*,D.DOCTOR_LAST_NAME 
    FROM PATIENTS P
    JOIN DOCTORS D ON P.DOCTOR_ID = D.DOCTOR_ID
    ORDER BY P.PATIENT_ID""").fetchall()
    return render_template('/patients/afisare_patients.html', date=date)


@app.route('/patients/delete_pat/<int:patient_id>')
def delete_pat(patient_id: int):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM patients WHERE patient_id = :patient_id", {'patient_id': patient_id})
    connection.commit()
    return render_template('/patients/succes_stergere_pat.html')


@app.route("/patients/patients_insert/", methods=['GET', 'POST'])
def patient():
    cursor = connection.cursor()
    doctors = cursor.execute("SELECT * FROM DOCTORS")
    if request.method == 'POST':
        try:
            doctor_id = request.form['doc']
            patient_first = request.form['patient_first']
            patient_last = request.form['patient_last']
            date_of_birth = request.form['date_of_birth']
            blood_type = request.form['blood_type']
            medical_insurance = request.form['medical_insurance']

            if re.search(r'\d', patient_first):
                raise ValueError("Eroare: Numele nu poate contine cifre")
            if re.search(r'\d', patient_last):
                raise ValueError("Eroare: Numele nu poate contine cifre")
            var = datetime.datetime.now()
            date = datetime.datetime.strptime(date_of_birth, "%Y.%m.%d")
            if var < date:
                raise ValueError

            cursor = connection.cursor()

            query1 = """
                           INSERT INTO PATIENTS (patient_first_name, patient_last_name, date_of_birth, blood_type, medical_insurance, doctor_id)
                           VALUES (:patient_first_name, :patient_last_name, TO_DATE(:date_of_birth, 'YYYY-MM-DD'), :blood_type,:medical_insurance,:doctor_id)
                       """

            cursor.execute(query1, {'patient_first_name': patient_last,
                                    'patient_last_name': patient_first, 'date_of_birth': date_of_birth,
                                    'blood_type': blood_type,
                                    'medical_insurance': medical_insurance, 'doctor_id': doctor_id})

            connection.commit()

        except oracledb.DatabaseError as e:
            print(f"Eroare la inserare in baza de date: {str(e)}")

    return render_template('/patients/patients_insert.html', doctors=doctors)


@app.route('/patients/modify_pat/<int:patient_id>', methods=["GET", "POST"])
def modify_pat(patient_id: int):
    cursor = connection.cursor()
    doctors = cursor.execute("SELECT * FROM DOCTORS")
    if request.method == 'POST':
        try:
            cursor = connection.cursor()
            patient_first = request.form['patient_first_name']
            patient_last = request.form['patient_last_name']
            date_of_birth = request.form['date_of_birth']
            blood_type = request.form['blood_type']
            medical_insurance = request.form['medical_insurance']

            if re.search(r'\d', patient_first):
                raise ValueError("Eroare: Numele nu poate contine cifre")
            if re.search(r'\d', patient_last):
                raise ValueError("Eroare: Numele nu poate contine cifre")

            query1 = """
                       UPDATE PATIENTS
                       SET patient_first_name = :patient_first_name,
                           patient_last_name = :patient_last_name,
                           date_of_birth = TO_DATE(:date_of_birth, 'YYYY-MM-DD'),
                           blood_type = :blood_type,
                           medical_insurance = :medical_insurance
                       WHERE patient_id = :patient_id
                       """
            var = datetime.datetime.now()
            date = datetime.datetime.strptime(date_of_birth, "%d.%m.%Y")
            if var < date:
                raise ValueError
            else:
                cursor.execute(query1, {
                    'patient_first_name': patient_first,
                    'patient_last_name': patient_last,
                    'date_of_birth': date_of_birth,
                    'blood_type': blood_type,
                    'medical_insurance': medical_insurance,
                    'patient_id': patient_id
                })

            connection.commit()

            return render_template('/patients/succes_modificare_pat.html')
        except oracledb.DatabaseError as e:
            print(f"Eroare la inserare in baza de date:{str(e)}")
    return render_template('/patients/modify_pat.html', doctors=doctors)


@app.route('/nurses/delete_nur/<int:nurses_id>')
def delete_nur(nurses_id: int):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM nurses WHERE nurses_id = :nurses_id", {'nurses_id': nurses_id})
    connection.commit()
    return render_template('/nurses/succes_stergere_nur.html')


@app.route("/nurses/nurses_insert/", methods=['GET', 'POST'])
def nurse():
    cursor = connection.cursor()
    departments = cursor.execute("SELECT * FROM DEPARTMENTS")
    if request.method == 'POST':
        try:
            id_dept = request.form['dept']
            first = request.form['nurse_first_name']
            last = request.form['nurse_last_name']
            specialization = request.form['specialization']
            salary = int(request.form['salary'])
            hire_date = request.form['hire_date']

            if re.search(r'\d', first):
                raise ValueError("Eroare: Numele nu poate contine cifre")
            if re.search(r'\d', last):
                raise ValueError("Eroare: Numele nu poate contine cifre")
            if re.search(r'\d', specialization):
                raise ValueError("Eroare: Specializarea nu poate contine cifre")
            var = datetime.datetime.now()
            date = datetime.datetime.strptime(hire_date, "%Y.%m.%d")
            if var < date:
                raise ValueError
            if salary < 0:
                raise ValueError("Eroare:Salariul nu poate fi negativ")

            cursor = connection.cursor()

            cursor.execute("""
                           INSERT INTO nurses (first_name, last_name, specialization, salary,hire_date,department_id)
                           VALUES (:first_name, :last_name,:specialization,:salary, TO_DATE(:hire_date, 'YYYY-MM-DD'),:department_id)
                       """, {'first_name': first,
                             'last_name': last, 'specialization': specialization, 'salary': salary,
                             'hire_date': hire_date,
                             'department_id': id_dept})

            connection.commit()

        except oracledb.DatabaseError as e:
            print(f"Eroare la inserare in baza de date: {str(e)}")

    return render_template('/nurses/nurses_insert.html', departments=departments)


@app.route('/nurses/afisare_nurses')
def afisare_nurses():
    cursor = connection.cursor()
    date: list[tuple[...]]
    date = cursor.execute(
        """SELECT N.*,DP.DEPARTMENT_NAME 
    FROM NURSES N
    JOIN DEPARTMENTS DP ON N.DEPARTMENT_ID = DP.DEPARTMENT_ID
    ORDER BY N.NURSES_ID""").fetchall()
    return render_template('/nurses/afisare_nurses.html', date=date)


@app.route('/nurses/modify_nur/<int:nurses_id>', methods=["GET", "POST"])
def modify_nur(nurses_id: int):
    cursor = connection.cursor()
    departments = cursor.execute("SELECT * FROM DEPARTMENTS")
    if request.method == 'POST':
        try:
            cursor = connection.cursor()
            first = request.form['nurse_first_name']
            last = request.form['nurse_last_name']
            specialization = request.form['specialization']
            salary = int(request.form['salary'])
            hire_date = request.form['hire_date']

            if re.search(r'\d', first):
                raise ValueError("Eroare: Numele nu poate contine cifre")
            if re.search(r'\d', last):
                raise ValueError("Eroare: Numele nu poate contine cifre")
            if re.search(r'\d', specialization):
                raise ValueError("Eroare: Specializarea nu poate contine cifre")
            var = datetime.datetime.now()
            date = datetime.datetime.strptime(hire_date, "%Y.%m.%d")
            if var < date:
                raise ValueError
            if salary < 0:
                raise ValueError("Eroare:Salariul nu poate fi negativ")

            query1 = """
                       UPDATE nurses
                       SET first_name = :first_name,
                           last_name = :last_name,
                           specialization = :specialization,
                           salary = :salary,
                           hire_date = TO_DATE(:hire_date, 'YYYY-MM-DD')
                       WHERE nurses_id = :nurses_id
                       """

            cursor.execute(query1, {
                'first_name': first,
                'last_name': last,
                'specialization': specialization,
                'salary': salary,
                'hire_date': hire_date,
                'nurses_id': nurses_id
            })

            connection.commit()

            return render_template('/nurses/succes_modificare_nur.html')
        except oracledb.DatabaseError as e:
            print(f"Eroare la inserare in baza de date:{str(e)}")
        cursor.close()
    return render_template('/nurses/modify_nur.html', departments=departments)


@app.route('/patient_history/delete_hist/<int:patient_history_id>')
def delete_hist(patient_history_id: int):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM patient_history WHERE patient_history_id = :patient_history_id",
                   {'patient_history_id': patient_history_id})
    connection.commit()
    cursor.close()
    return render_template('/patient_history/succes_stergere_history.html')


@app.route('/patient_history/afisare_history')
def afisare_patient_history():
    cursor = connection.cursor()
    date: list[tuple[...]]
    date = cursor.execute(
        """SELECT PH.*,P.PATIENT_LAST_NAME 
    FROM PATIENT_HISTORY PH
    JOIN PATIENTS P ON PH.PATIENT_ID = P.PATIENT_ID
    ORDER BY PH.PATIENT_HISTORY_ID""").fetchall()
    cursor.close()
    return render_template('/patient_history/afisare_history.html', date=date)


@app.route('/patient_history/modify_hist/<int:patient_history_id>', methods=["GET", "POST"])
def modify_hist(patient_history_id: int):
    cursor = connection.cursor()
    patients = cursor.execute("SELECT * FROM PATIENTS")
    if request.method == 'POST':
        try:
            cursor = connection.cursor()
            mod = request.form['mod']
            mod_date = request.form['mod_date']

            if re.search(r'\d', mod):
                raise ValueError("Eroare: Numele modificarii nu poate contine cifre")
            var = datetime.datetime.now()
            date = datetime.datetime.strptime(mod_date, "%Y.%m.%d")
            if var < date:
                raise ValueError

            query1 = """
                       UPDATE PATIENT_HISTORY
                       SET modification = :modification,
                           modification_date = TO_DATE(:modification_date, 'YYYY-MM-DD')
                       WHERE patient_history_id = :patient_history_id
                       """
            cursor.execute(query1, {
                'modification': mod,
                'modification_date': mod_date,
                'patient_history_id': patient_history_id
            })

            connection.commit()

            return render_template('/patient_history/succes_modificare_history.html')
        except oracledb.DatabaseError as e:
            print(f"Eroare la inserare in baza de date:{str(e)}")
        cursor.close()
    return render_template('/patient_history/modify_hist.html', patients=patients)


@app.route("/patient_history/history_insert/", methods=['GET', 'POST'])
def patient_history():
    cursor = connection.cursor()
    patients = cursor.execute("SELECT * FROM PATIENTS")
    if request.method == 'POST':
        try:
            patient_id = request.form['patient']
            mod = request.form['mod']
            mod_date = request.form['mod_date']

            if re.search(r'\d', mod):
                raise ValueError("Eroare: Numele modificarii nu poate contine cifre")
            var = datetime.datetime.now()
            date = datetime.datetime.strptime(mod_date, "%Y.%m.%d")
            if var < date:
                raise ValueError

            cursor = connection.cursor()

            query1 = """
                           INSERT INTO PATIENT_HISTORY (modification,modification_date,patient_id)
                           VALUES (:modification,TO_DATE(:modification_date, 'YYYY-MM-DD'),:patient_id)
                       """

            cursor.execute(query1, {'modification': mod,
                                    'modification_date': mod_date, 'patient_id': patient_id})

            connection.commit()

        except oracledb.DatabaseError as e:
            print(f"Eroare la inserare in baza de date: {str(e)}")
        cursor.close()
    return render_template('/patient_history/history_insert.html', patients=patients)


@app.route('/drugs/afisare_drugs')
def afisare_drugs():
    cursor = connection.cursor()
    date: list[tuple[...]]
    date = cursor.execute(
        """SELECT D.*,DP.DEPARTMENT_NAME,DI.SIDE_EFFECTS,DI.PRICE 
    FROM DRUGS D
    JOIN DEPARTMENTS DP ON D.DEPARTMENT_ID = DP.DEPARTMENT_ID
    JOIN DRUG_INFO DI ON D.INFO_ID = DI.INFO_ID
    ORDER BY D.DRUG_ID""").fetchall()
    return render_template('/drugs/afisare_drugs.html', date=date)


@app.route('/drugs/modify_drugs/<int:drug_id>', methods=["GET", "POST"])
def modify_drug(drug_id: int):
    cursor = connection.cursor()
    departments = cursor.execute("SELECT * FROM DEPARTMENTS")
    if request.method == 'POST':
        try:
            cursor = connection.cursor()
            name = request.form['name']
            afu = int(request.form['afu'])
            man = request.form['man']
            side_effects = request.form['side_effects']
            price = int(request.form['price'])

            if re.search(r'\d', name):
                raise ValueError("Eroare: Numele nu poate contine cifre")
            if re.search(r'\d', man):
                raise ValueError("Eroare: Numele producatorului nu poate contine cifre")
            if re.search(r'\d', side_effects):
                raise ValueError("Eroare: Efectele secundare nu pot contine cifre")
            if afu < 0:
                raise ValueError("Eroare:Numarul disponibil nu poate fi negativ")
            if price < 0:
                raise ValueError("Eroare:Pretul nu poate fi negativ")

            di_id = cursor.execute("SELECT info_id from drugs where drug_id = :id", [drug_id]).fetchone()[0]

            query1 = """
                       UPDATE drug_info
                       SET side_effects = :side_effects,
                           price = :price
                       WHERE info_id = (select info_id from drugs d where d.info_id = :id)
                       """

            cursor.execute(query1, {
                'side_effects': side_effects,
                'price': price,
                'id': di_id
            })

            query2 = """
                       UPDATE drugs
                       SET DRUG_NAME = :DRUG_NAME,
                           AVAILABLE_FOR_USE = :AVAILABLE_FOR_USE,
                           MANUFACTURER = :MANUFACTURER
                       WHERE drug_id = :drug_id
                       """

            cursor.execute(query2, {
                'DRUG_NAME': name,
                'AVAILABLE_FOR_USE': afu,
                'MANUFACTURER': man,
                'drug_id': drug_id
            })

            connection.commit()

            return render_template('/drugs/succes_modificare_drugs.html')
        except oracledb.DatabaseError as e:
            print(f"Eroare la inserare in baza de date:{str(e)}")
        cursor.close()
    return render_template('/drugs/modify_drugs.html', departments=departments)


@app.route('/drugs/delete_drugs/<int:drug_id>')
def delete_drug(drug_id: int):
    cursor = connection.cursor()
    di_id = cursor.execute("SELECT info_id from drugs where drug_id = :id", [drug_id]).fetchone()[0]
    cursor.execute("DELETE FROM DRUGS WHERE drug_id = :id", {'id': drug_id})
    cursor.execute("""DELETE FROM DRUG_INFO WHERE info_id = :id""", {'id': di_id})
    connection.commit()
    return render_template('/drugs/succes_stergere_drugs.html')


@app.route("/drugs/insert_drugs/", methods=['GET', 'POST'])
def drug():
    cursor = connection.cursor()
    departments = cursor.execute("SELECT * FROM DEPARTMENTS")
    if request.method == 'POST':
        try:
            id_dept = request.form['dept']
            name = request.form['name']
            afu = int(request.form['afu'])
            man = request.form['man']
            side_effects = request.form['side_effects']
            price = int(request.form['price'])

            if re.search(r'\d', name):
                raise ValueError("Eroare: Numele nu poate contine cifre")
            if re.search(r'\d', man):
                raise ValueError("Eroare: Numele producatorului nu poate contine cifre")
            if re.search(r'\d', side_effects):
                raise ValueError("Eroare: Efectele secundare nu pot contine cifre")
            if afu < 0:
                raise ValueError("Eroare:Numarul disponibil nu poate fi negativ")
            if price < 0:
                raise ValueError("Eroare:Pretul nu poate fi negativ")

            cursor = connection.cursor()

            cursor.execute("INSERT INTO DRUG_INFO (SIDE_EFFECTS,PRICE) VALUES (:side_effects,:price)",
                           {'side_effects': side_effects, 'price': price})
            info_id = cursor.execute(
                "SELECT * FROM DRUG_INFO where side_effects = :side_effects and price = :price",
                {'side_effects': side_effects, 'price': price}).fetchone()[0]
            cursor.execute("INSERT INTO DRUGS(DRUG_NAME,AVAILABLE_FOR_USE,DEPARTMENT_ID,MANUFACTURER,INFO_ID)"
                           "VALUES (:DRUG_NAME,:AVAILABLE_FOR_USE,:DEPARTMENT_ID,:MANUFACTURER,:INFO_ID)",
                           {'DRUG_NAME': name, 'AVAILABLE_FOR_USE': afu, 'DEPARTMENT_ID': id_dept,
                            'MANUFACTURER': man, 'INFO_ID': info_id})

            connection.commit()

        except oracledb.DatabaseError as e:
            connection.rollback()
            print(f"Eroare la inserare in baza de date: {str(e)}")

    return render_template('/drugs/insert_drugs.html', departments=departments)


@app.route('/branch/delete_branch/<int:administrative_branch_per_department_id>')
def delete_branch(administrative_branch_per_department_id: int):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM administrative_branch_per_department WHERE administrative_branch_per_department_id = "
                   ":administrative_branch_per_department_id",
                   {'administrative_branch_per_department_id': administrative_branch_per_department_id})
    connection.commit()
    return render_template('/branch/succes_stergere_branch.html')


@app.route("/branch/branch_insert/", methods=['GET', 'POST'])
def branch():
    cursor = connection.cursor()
    departments = cursor.execute("SELECT * FROM DEPARTMENTS")
    if request.method == 'POST':
        try:
            id_dept = request.form['dept']
            fname = request.form['fname']
            lname = request.form['lname']
            pos = request.form['pos']
            salary = int(request.form['salary'])
            hire_date = request.form['hire_date']

            if re.search(r'\d', fname):
                raise ValueError("Eroare: Numele nu poate contine cifre")
            if re.search(r'\d', lname):
                raise ValueError("Eroare: Numele nu poate contine cifre")
            if re.search(r'\d', pos):
                raise ValueError("Eroare: Pozitia nu poate contine cifre")
            var = datetime.datetime.now()
            date = datetime.datetime.strptime(hire_date, "%Y.%m.%d")
            if var < date:
                raise ValueError
            if salary < 0:
                raise ValueError("Eroare:Salariul nu poate fi negativ")

            cursor = connection.cursor()

            cursor.execute("""
                           INSERT INTO administrative_branch_per_department (first_name, last_name, position,salary, hire_date, department_id)
                           VALUES (:first_name, :last_name,:position,:salary,TO_DATE(:hire_date, 'YYYY-MM-DD'), :department_id)
                       """, {'first_name': fname, 'last_name': lname,
                             'position': pos, 'salary': salary, 'hire_date': hire_date,
                             'department_id': id_dept})

            connection.commit()

        except oracledb.DatabaseError as e:
            print(f"Eroare la inserare in baza de date: {str(e)}")

    return render_template('/branch/branch_insert.html', departments=departments)


@app.route('/branch/afisare_branch')
def afisare_branch():
    cursor = connection.cursor()
    date: list[tuple[...]]
    date = cursor.execute(
        """SELECT D.*,DP.DEPARTMENT_NAME 
    FROM administrative_branch_per_department D
    JOIN DEPARTMENTS DP ON D.DEPARTMENT_ID = DP.DEPARTMENT_ID
    ORDER BY D.administrative_branch_per_department_id""").fetchall()
    return render_template('/branch/afisare_branch.html', date=date)


@app.route('/branch/modify_branch/<int:administrative_branch_per_department_id>', methods=["GET", "POST"])
def modify_branch(administrative_branch_per_department_id: int):
    cursor = connection.cursor()
    departments = cursor.execute("SELECT * FROM DEPARTMENTS")
    if request.method == 'POST':
        try:
            cursor = connection.cursor()
            fname = request.form['fname']
            lname = request.form['lname']
            pos = request.form['pos']
            salary = int(request.form['salary'])
            hire_date = request.form['hire_date']

            if re.search(r'\d', fname):
                raise ValueError("Eroare: Numele nu poate contine cifre")
            if re.search(r'\d', lname):
                raise ValueError("Eroare: Numele nu poate contine cifre")
            if re.search(r'\d', pos):
                raise ValueError("Eroare: Pozitia nu poate contine cifre")
            var = datetime.datetime.now()
            date = datetime.datetime.strptime(hire_date, "%Y.%m.%d")
            if var < date:
                raise ValueError
            if salary < 0:
                raise ValueError("Eroare:Salariul nu poate fi negativ")

            query1 = """
                       UPDATE administrative_branch_per_department
                       SET first_name = :first_name,
                           last_name = :last_name,
                           position = :position,
                           salary = :salary,
                           hire_date = TO_DATE(:hire_date, 'YYYY-MM-DD')
                       WHERE administrative_branch_per_department_id = :administrative_branch_per_department_id
                       """

            cursor.execute(query1, {
                'first_name': fname,
                'last_name': lname,
                'position': pos,
                'salary': salary,
                'hire_date': hire_date,
                'administrative_branch_per_department_id': administrative_branch_per_department_id
            })

            connection.commit()

            return render_template('/branch/succes_modificare_branch.html')
        except oracledb.DatabaseError as e:
            print(f"Eroare la inserare in baza de date:{str(e)}")
    return render_template('/branch/modify_branch.html', departments=departments)


@app.route('/medical/afisare_med')
def afisare_med():
    cursor = connection.cursor()
    date: list[tuple[...]]
    date = cursor.execute(
        """SELECT ME.*,DP.DEPARTMENT_NAME 
    FROM medical_equipment ME
    JOIN DEPARTMENTS DP ON ME.DEPARTMENT_ID = DP.DEPARTMENT_ID
    ORDER BY ME.equipment_id""").fetchall()
    return render_template('/medical/afisare_med.html', date=date)


@app.route('/medical/modify_med/<int:equipment_id>', methods=["GET", "POST"])
def modify_med(equipment_id: int):
    cursor = connection.cursor()
    departments = cursor.execute("SELECT * FROM DEPARTMENTS").fetchall()
    if request.method == 'POST':
        try:
            cursor = connection.cursor()
            name = request.form['name']
            afu = int(request.form['afu'])

            if re.search(r'\d', name):
                raise ValueError("Eroare: Numele nu poate contine cifre")
            if afu < 0:
                raise ValueError("Eroare:Numarul disponibil nu poate fi negativ")

            query1 = """
                       UPDATE medical_equipment
                       SET equipment_name = :equipment_name,
                           available_for_use = :available_for_use
                       WHERE equipment_id = :equipment_id
                       """

            cursor.execute(query1, {
                'equipment_name': name,
                'available_for_use': afu,
                'equipment_id': equipment_id
            })

            connection.commit()

            return render_template('/medical/succes_modificare_med.html')
        except oracledb.DatabaseError as e:
            print(f"Eroare la inserare in baza de date:{str(e)}")
    return render_template('/medical/modify_med.html', departments=departments)


@app.route('/medical/delete_med/<int:equipment_id>')
def delete_med(equipment_id: int):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM medical_equipment WHERE equipment_id = :equipment_id", {'equipment_id': equipment_id})
    connection.commit()
    return render_template('/medical/succes_stergere_med.html')


@app.route("/medical/med_insert/", methods=['GET', 'POST'])
def med():
    cursor = connection.cursor()
    departments = cursor.execute("SELECT * FROM DEPARTMENTS")
    if request.method == 'POST':
        try:
            id_dept = request.form['dept']
            name = request.form['name']
            afu = int(request.form['afu'])

            if re.search(r'\d', name):
                raise ValueError("Eroare: Numele nu poate contine cifre")
            if afu < 0:
                raise ValueError("Eroare:Numarul disponibil nu poate fi negativ")

            cursor = connection.cursor()

            cursor.execute("""
                           INSERT INTO medical_equipment (equipment_name, available_for_use,department_id)
                           VALUES (:equipment_name, :available_for_use,:department_id)
                       """, {'equipment_name': name,
                             'available_for_use': afu,
                             'department_id': id_dept})

            connection.commit()

        except oracledb.DatabaseError as e:
            print(f"Eroare la inserare in baza de date: {str(e)}")
    return render_template('/medical/med_insert.html', departments=departments)


@app.route('/trans/afisare_trans')
def afisare_trans():
    cursor = connection.cursor()
    date: list[tuple[...]]
    date = cursor.execute(
        """SELECT DT.*,D.DRUG_NAME 
    FROM drug_transactions DT
    JOIN DRUGS D ON DT.DRUG_ID = D.DRUG_ID
    ORDER BY DT.drug_transactions_id""").fetchall()
    return render_template('/trans/afisare_trans.html', date=date)


@app.route('/trans/modify_trans/<int:drug_transactions_id>', methods=["GET", "POST"])
def modify_trans(drug_transactions_id: int):
    cursor = connection.cursor()
    drugs = cursor.execute("SELECT * FROM DRUGS").fetchall()
    if request.method == 'POST':
        try:
            cursor = connection.cursor()
            quan = int(request.form['quan'])
            a_date = request.form['a_date']
            seller = request.form['seller']

            if re.search(r'\d', seller):
                raise ValueError("Eroare: Vanzatorul nu poate contine cifre")
            var = datetime.datetime.now()
            date = datetime.datetime.strptime(a_date, "%Y.%m.%d")
            if var < date:
                raise ValueError
            if quan < 0:
                raise ValueError("Eroare:Cantitatea nu poate fi negativa")

            query1 = """
                       UPDATE drug_transactions
                       SET quantity_bought = :quantity_bought,
                           acquisition_date = TO_DATE(:acquisition_date, 'YYYY-MM-DD'),
                           seller = :seller
                       WHERE drug_transactions_id = :drug_transactions_id
                       """

            cursor.execute(query1, {
                'quantity_bought': quan,
                'acquisition_date': a_date,
                'seller': seller,
                'drug_transactions_id': drug_transactions_id
            })

            connection.commit()

            return render_template('/trans/succes_modificare_trans.html')
        except oracledb.DatabaseError as e:
            print(f"Eroare la inserare in baza de date:{str(e)}")
    return render_template('/trans/modify_trans.html', drugs=drugs)


@app.route('/inventory/delete_trans/<int:drug_transactions_id>')
def delete_trans(drug_transactions_id: int):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM drug_transactions WHERE drug_transactions_id = :drug_transactions_id",
                   {'drug_transactions_id': drug_transactions_id})
    connection.commit()
    return render_template('/trans/succes_stergere_trans.html')


@app.route("/trans/insert_trans/", methods=['GET', 'POST'])
def trans():
    cursor = connection.cursor()
    drugs = cursor.execute("SELECT * FROM DRUGS")
    if request.method == 'POST':
        try:
            id_drug = request.form['drug']
            quan = int(request.form['quan'])
            a_date = request.form['a_date']
            seller = request.form['seller']

            if re.search(r'\d', seller):
                raise ValueError("Eroare: Vanzatorul nu poate contine cifre")
            var = datetime.datetime.now()
            date = datetime.datetime.strptime(a_date, "%Y.%m.%d")
            if var < date:
                raise ValueError
            if quan < 0:
                raise ValueError("Eroare:Cantitatea nu poate fi negativa")

            cursor = connection.cursor()

            cursor.execute("""
                           INSERT INTO drug_transactions (quantity_bought, acquisition_date,seller,drug_id)
                           VALUES (:quantity_bought, TO_DATE(:acquisition_date, 'YYYY-MM-DD'),:seller,:drug_id)
                       """, {'quantity_bought': quan,
                             'acquisition_date': a_date, 'seller': seller,
                             'drug_id': id_drug})

            connection.commit()

        except oracledb.DatabaseError as e:
            print(f"Eroare la inserare in baza de date: {str(e)}")
    return render_template('/trans/insert_trans.html', drugs=drugs)


@app.route('/inventory/afisare_inv')
def afisare_inv():
    cursor = connection.cursor()
    date: list[tuple[...]]
    date = cursor.execute(
        """SELECT IE.*,ME.EQUIPMENT_NAME 
    FROM inventory_equipment IE
    JOIN medical_equipment ME ON IE.EQUIPMENT_ID = ME.EQUIPMENT_ID
    ORDER BY IE.inventory_equipment_id""").fetchall()
    return render_template('/inventory/afisare_inv.html', date=date)


@app.route('/inventory/modify_inv/<int:inventory_equipment_id>', methods=["GET", "POST"])
def modify_inv(inventory_equipment_id: int):
    cursor = connection.cursor()
    equipments = cursor.execute("SELECT * FROM MEDICAL_EQUIPMENT").fetchall()
    if request.method == 'POST':
        try:
            cursor = connection.cursor()
            quan = int(request.form['quan'])
            cond = request.form['cond']
            buy_date = request.form['buy_date']

            var = datetime.datetime.now()
            date = datetime.datetime.strptime(buy_date, "%Y.%m.%d")
            if var < date:
                raise ValueError
            if quan < 0:
                raise ValueError("Eroare:Cantitatea nu poate fi negativa")

            query1 = """
                       UPDATE inventory_equipment
                       SET quantity = :quantity,
                           condition = :condition,
                           buying_date = TO_DATE(:buying_date, 'YYYY-MM-DD')
                       WHERE inventory_equipment_id = :inventory_equipment_id
                       """

            cursor.execute(query1, {
                'quantity': quan,
                'condition': cond,
                'buying_date': buy_date,
                'inventory_equipment_id': inventory_equipment_id
            })

            connection.commit()

            return render_template('/inventory/succes_modificare_inv.html')
        except oracledb.DatabaseError as e:
            print(f"Eroare la inserare in baza de date:{str(e)}")
    return render_template('/inventory/modify_inv.html', equipments=equipments)


@app.route('/inventory/delete_inv/<int:inventory_equipment_id>')
def delete_inv(inventory_equipment_id: int):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM inventory_equipment WHERE inventory_equipment_id = :inventory_equipment_id",
                   {'inventory_equipment_id': inventory_equipment_id})
    connection.commit()
    return render_template('/inventory/succes_stergere_inv.html')


@app.route("/inventory/insert_inv/", methods=['GET', 'POST'])
def inv():
    cursor = connection.cursor()
    equipments = cursor.execute("SELECT * FROM MEDICAL_EQUIPMENT")
    if request.method == 'POST':
        try:
            id_equipment = request.form['eq']
            quan = int(request.form['quan'])
            cond = request.form['cond']
            buy_date = request.form['buy_date']

            var = datetime.datetime.now()
            date = datetime.datetime.strptime(buy_date, "%Y.%m.%d")
            if var < date:
                raise ValueError
            if quan < 0:
                raise ValueError("Eroare:Cantitatea nu poate fi negativa")

            cursor = connection.cursor()

            cursor.execute("""
                           INSERT INTO inventory_equipment (quantity,condition, buying_date,equipment_id)
                           VALUES (:quantity, :condition, TO_DATE(:buying_date, 'YYYY-MM-DD'),:equipment_id)
                       """, {'quantity': quan,
                             'condition': cond, 'buying_date': buy_date,
                             'equipment_id': id_equipment})

            connection.commit()

        except oracledb.DatabaseError as e:
            print(f"Eroare la inserare in baza de date: {str(e)}")
    return render_template('/inventory/insert_inv.html', equipments=equipments)


if __name__ == "__main__":
    app.run(debug=True)
