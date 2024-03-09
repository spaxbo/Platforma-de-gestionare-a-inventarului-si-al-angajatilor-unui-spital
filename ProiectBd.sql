create table BD006.DEPARTMENTS
(
    DEPARTMENT_ID      NUMBER generated as identity
        constraint DEPARTMENT_ID_PK
            primary key,
    DEPARTMENT_NAME    VARCHAR2(50) not null
        constraint DEPARTMENTS_PK
            unique
        constraint DEPT_NAME
            check (REGEXP_LIKE(LOWER(DEPARTMENT_NAME), '^[a-z -]+$')),
    MANAGER_FIRST_NAME VARCHAR2(50) not null
        constraint MANAGER_FIRST_NAME_CK
            check (REGEXP_LIKE(LOWER(MANAGER_FIRST_NAME), '^[a-z -]+$')),
    MANAGER_LAST_NAME  VARCHAR2(50) not null
        constraint MANAGER_LAST_NAME_CK
            check (REGEXP_LIKE(LOWER(MANAGER_LAST_NAME), '^[a-z -]+$'))
)
/

create table BD006.DOCTORS
(
    DOCTOR_ID         NUMBER generated as identity
        constraint DOCTOR_ID_PK
            primary key,
    DOCTOR_FIRST_NAME VARCHAR2(50) not null
        constraint DOCTOR_FIRST_NAME_CK
            check (REGEXP_LIKE(LOWER(DOCTOR_FIRST_NAME), '^[a-z -]+$')),
    DOCTOR_LAST_NAME  VARCHAR2(50) not null
        constraint DOCTOR_LAST_NAME_CK
            check (REGEXP_LIKE(LOWER(DOCTOR_LAST_NAME), '^[a-z -]+$')),
    HIRE_DATE         DATE         not null,
    SALARY            NUMBER       not null
        constraint SALARY_CK
            check (salary >= 0),
    DEPARTMENT_ID     NUMBER
        constraint DEPARTMENT_DOCTOR_FK
            references BD006.DEPARTMENTS
)
/

create table BD006.PATIENTS
(
    PATIENT_ID         NUMBER generated as identity
        constraint PATIENT_ID_PK
            primary key,
    PATIENT_FIRST_NAME VARCHAR2(50) not null
        constraint FIRST_NAME_P_CK
            check (REGEXP_LIKE(LOWER(PATIENT_FIRST_NAME), '^[a-z -]+$')),
    PATIENT_LAST_NAME  VARCHAR2(50) not null
        constraint LAST_NAME_CK
            check (REGEXP_LIKE(LOWER(PATIENT_LAST_NAME), '^[a-z -]+$')),
    DATE_OF_BIRTH      DATE         not null,
    BLOOD_TYPE         VARCHAR2(5)  not null
        constraint BLOOD_TYPE_CK
            check (BLOOD_TYPE in ('A', 'B', 'AB', '0')),
    MEDICAL_INSURANCE  VARCHAR2(10) not null
        constraint MEDICAL_INSURANCE_CK
            check (medical_insurance in ('cass', 'private')),
    DOCTOR_ID          NUMBER
        constraint DOCTOR_ID_FK
            references BD006.DOCTORS
)
/

create table BD006.MEDICAL_EQUIPMENT
(
    EQUIPMENT_ID      NUMBER generated as identity
        constraint EQUIPMENT_ID_PK
            primary key,
    EQUIPMENT_NAME    VARCHAR2(50) not null
        constraint EQ_CK
            check (REGEXP_LIKE(LOWER(EQUIPMENT_NAME), '^[a-z -]+$')),
    DEPARTMENT_ID     NUMBER
        constraint DEPARTMENT_ID_ME_FK
            references BD006.DEPARTMENTS,
    AVAILABLE_FOR_USE NUMBER       not null
        constraint AFU_CK
            check (AVAILABLE_FOR_USE >= 0)
)
/

create table BD006.INVENTORY_EQUIPMENT
(
    INVENTORY_EQUIPMENT_ID NUMBER generated as identity
        constraint INVENTORY_EQUIPMENT_ID_PK
            primary key,
    QUANTITY               NUMBER       not null
        constraint QUANTITY_CK
            check (quantity >= 0),
    CONDITION              VARCHAR2(15) not null
        constraint CONDITION_CK
            check (condition in ('New', 'Used', 'Broken', 'Fixed')),
    BUYING_DATE            DATE         not null,
    EQUIPMENT_ID           NUMBER
        constraint EQUIPMENT_ID_FK
            references BD006.MEDICAL_EQUIPMENT
)
/

create table BD006.ADMINISTRATIVE_BRANCH_PER_DEPARTMENT
(
    ADMINISTRATIVE_BRANCH_PER_DEPARTMENT_ID NUMBER generated as identity
        constraint ADMINISTRATIVE_BRANCH_PER_DEPARTMENT_PK
            primary key,
    FIRST_NAME                              VARCHAR2(50) not null
        constraint FIRST_NAME_A_CK
            check (REGEXP_LIKE(LOWER(FIRST_NAME), '^[a-z -]+$')),
    LAST_NAME                               VARCHAR2(50) not null
        constraint LAST_NAME_A_CK
            check (REGEXP_LIKE(LOWER(LAST_NAME), '^[a-z -]+$')),
    POSITION                                VARCHAR2(50) not null
        constraint POSITION_CK
            check (REGEXP_LIKE(LOWER(POSITION), '^[a-z -]+$')),
    SALARY                                  NUMBER       not null
        constraint SALARY_P_CK
            check (SALARY >= 0),
    HIRE_DATE                               DATE         not null,
    DEPARTMENT_ID                           NUMBER
        constraint ADMINISTRATIVE_BRANCH_PER_DEPARTMENT_DEPARTMENTS__FK
            references BD006.DEPARTMENTS
)
/

create table BD006.NURSES
(
    NURSES_ID      NUMBER generated as identity
        constraint NURSES_PK
            primary key,
    FIRST_NAME     VARCHAR2(50) not null
        constraint FIRST_NAME_N_CK
            check (REGEXP_LIKE(LOWER(FIRST_NAME), '^[a-z -]+$')),
    LAST_NAME      VARCHAR2(50) not null
        constraint LAST_NAME_N_CK
            check (REGEXP_LIKE(LOWER(LAST_NAME), '^[a-z -]+$')),
    SPECIALIZATION VARCHAR2(50) not null
        constraint SPECIALIZATION
            check (REGEXP_LIKE(LOWER(SPECIALIZATION), '^[a-z -]+$')),
    SALARY         NUMBER       not null
        constraint SALARY_N_CK
            check (SALARY >= 0),
    HIRE_DATE      DATE         not null,
    DEPARTMENT_ID  NUMBER
        constraint NURSES_DEPARTMENTS__FK
            references BD006.DEPARTMENTS
)
/

create table BD006.PATIENT_HISTORY
(
    PATIENT_HISTORY_ID NUMBER generated as identity
        constraint PATIENT_HISTORY_PK
            primary key,
    MODIFICATION_DATE  DATE          not null,
    MODIFICATION       VARCHAR2(255) not null
        constraint MOD_CK
            check (REGEXP_LIKE(LOWER(MODIFICATION), '^[a-z -]+$')),
    PATIENT_ID         NUMBER
        constraint PATIENT_HISTORY_PATIENTS__FK
            references BD006.PATIENTS
)
/

create table BD006.DRUG_INFO
(
    INFO_ID      NUMBER generated as identity
        constraint DRUG_INFO_PK
            primary key,
    SIDE_EFFECTS VARCHAR2(50) not null
        constraint SIDE_EFFECTS_CK
            check (REGEXP_LIKE(LOWER(SIDE_EFFECTS), '^[a-z -]+$')),
    PRICE        NUMBER       not null
        constraint PRICE_CK
            check (PRICE >= 0),
    constraint DRUG_UK
        unique (SIDE_EFFECTS, PRICE)
)
/

create table BD006.DRUGS
(
    DRUG_ID           NUMBER generated as identity
        constraint DRUG_ID_PK
            primary key,
    DRUG_NAME         VARCHAR2(50) not null
        constraint DRUG_NAME_UK
            unique
        constraint DRUG_NAME_CK
            check (REGEXP_LIKE(LOWER(DRUG_NAME), '^[a-z -]+$')),
    AVAILABLE_FOR_USE NUMBER       not null
        constraint AVAILABLE_FOR_USE_CK
            check (available_for_use >= 0),
    DEPARTMENT_ID     NUMBER
        constraint DEPARTMENT_ID_DRUGS_FK
            references BD006.DEPARTMENTS,
    MANUFACTURER      VARCHAR2(50) not null
        constraint MAN_CK
            check (REGEXP_LIKE(LOWER(MANUFACTURER), '^[a-z -]+$')),
    INFO_ID           NUMBER       not null
        constraint INFO_ID_UK
            unique
        constraint INFO_FK
            references BD006.DRUG_INFO
)
/

create table BD006.DRUG_TRANSACTIONS
(
    DRUG_TRANSACTIONS_ID NUMBER generated as identity
        constraint DRUG_TRANSACTIONS_PK
            primary key,
    QUANTITY_BOUGHT      NUMBER       not null
        constraint QUANTITY_BOUGHT_CK
            check (QUANTITY_BOUGHT >= 0),
    ACQUISITION_DATE     DATE         not null,
    SELLER               VARCHAR2(50) not null
        constraint SELLER_CK
            check (REGEXP_LIKE(LOWER(SELLER), '^[a-z -]+$')),
    DRUG_ID              NUMBER
        constraint DRUG_TRANSACTIONS_DRUGS__FK
            references BD006.DRUGS
)
/

