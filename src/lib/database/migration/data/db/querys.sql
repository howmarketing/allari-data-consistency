


SELECT 'PERSON:';
SELECT * FROM person;

SELECT 'EXPERIENCE:';
SELECT * FROM experience;

SELECT 'CONTACT:';
SELECT * FROM contact;

SELECT 'PHONE:';
SELECT * FROM phone;


SELECT 'CONTACTs: Retrieves information about phone numbers associated with a specific person (with ID 1) and their contacts. The query joins the `person`, `contact`, and `phone` tables, and also performs a left join with the `person` table to find any other persons whose phone numbers match the phone numbers in the `phone` table.' as TABLE_NAME;

SELECT
    phone.id,
    person.first_name || ' ' || person.last_name AS 'contact_owner_name',
    contact.nickname,
    phone.type,
    phone.number,
    phone.contact_id,
    phone_number_person.id,
    phone_number_person.first_name || ' ' || phone_number_person.last_name AS 'contact_person_name'
FROM
    person
JOIN
    contact ON person.id = contact.owner_id AND contact.owner_id = 1
JOIN
    phone ON phone.contact_id = contact.id
LEFT JOIN
    person as phone_number_person ON phone_number_person.phone LIKE phone.number
WHERE
    person.id = 1
ORDER BY
    person.id, phone.contact_id ASC;


SELECT 
    e.id,
    e.person_id,
    e.company,
    e.title,
    (JULIANDAY(COALESCE(end_date, CURRENT_DATE)) - JULIANDAY(start_date)) as 'permanence_days',
    e.start_date,
    e.end_date
FROM 
    experience as e
WHERE
    permanence_days >= 2000;




SELECT * FROM experience WHERE person_id != 0 ORDER BY company ASC;
SELECT * FROM experience WHERE person_id = 1;
SELECT * FROM contact WHERE owner_id = 1;

SELECT * FROM phone;

-- SQLite
SELECT
    phone.id,
    person.first_name || ' ' || person.last_name AS 'name',
    contact.nickname,
    phone.type,
    phone.number,
    phone.contact_id
FROM
    person
JOIN
    contact ON person.id = contact.owner_id AND contact.owner_id = 1
JOIN
    phone ON phone.contact_id = contact.id
WHERE
    person.id = 1
ORDER BY
    person.id, phone.contact_id ASC;



SELECT 
    * 
FROM 
    person
WHERE
    person.phone LIKE '%4151234567' OR
    person.phone LIKE '%2123458974' OR
    person.phone LIKE '%9173454768' OR
    person.phone LIKE '%2993223016';





-- id	      name	    nickname	        type	        number	        contact_id
-- 01	    John Doe	    Dad	            landline      4151234567              01
-- 02	    John Doe	    Mom	            landline      2123458974              02
-- 03	    John Doe	    Mom	            cell          +19173454768            02
-- 18	    John Doe	    Samanta	        cell	      +5562993223016          17

