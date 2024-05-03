# allari-data-consistency
In this four-part exercise, you will write Python code to find connections between people based on given rules.
# Project Overview

In this four-part exercise, you will write Python code to find connections between people based on given rules. Key points include:

- The option to use open-source libraries, with dependencies managed via tools like pip or poetry.
- The necessity for thorough unit and integration testing. Instructions for running these tests and the application should be included in the README file.

## Part 1: Loading Person Records

You are tasked to write a function that:

- Loads any number of Person records into memory from a JSON file. This file contains an array of objects formatted as shown below:

    ```json
    // Person: 
    {
      "id": 0,
      "first": "Jane",
      "last": "Doe",
      "phone": "1-2123458974",
      "experience": [
        {
          "company": "OrangeCart",
          "title": "Director of Marketing",
          "start": "2017-01-01",
          "end": null
        }
      ]
    }
    ```

- **Notes:**
  - "id" values are unique across records.
  - The "phone" field may be null; if not, it is a normalized string combining country code and phone number, separated by a dash.
  - The "start" and "end" fields in an "experience" are normalized strings containing dates. A null "end" date represents the present.
  - Each "experience" entry is unique by "company," implying no multiple entries for the same person/company combination are present.
  - The array should be the root level object in the JSON file without needing a root level key.
    - an array is valid JSON so there is no need to have a root level key like: {“persons”: [...]} make the array itself the root level object instead: [{...}]


## Part 2

> Write a function that takes a Person ID and returns a list of all the IDs of the people that are connected to that person. For the purposes of this exercise, two people are considered connected if they have at least one company in common in their experience. The list should include the original Person ID.
> 

### Part 2: Identifying Connected Persons

- Write a function with two parameters:
  1. A list of Person records.
  2. A Person ID that exists within the list.
- The function returns a list of IDs (integers) representing Persons that are "connected" to the person identified by the second parameter.
- Two Persons are deemed "connected" if:
  - They have worked for the same company.
  - Their employment periods at that company overlapped for at least 90 days.
- For the purpose of this exercise, it's acceptable to assume each person has only one entry per company, meaning re-employment at previous companies does not occur.


## Part 3: Loading Contact Records and Determining Connections Via Contacts

- Load any number of Contact records into memory using a function similar to Part 1, from a JSON file formatted as follows:
    ```json
    // Contact: 
    {
      "id": 0,
      "owner_id": 123,
      "contact_nickname": "Mom",
      "phone": [
        {
          "number": "(212) 345-8974",
          "type": "landline"
        },
        {
          "number": "+19173454768",
          "type": "cell"
        }
      ]
    }
    ```
- **Notes**:
  - A Contact is linked to a Person via the "owner_id" (foreign key).
  - The "phone" field is an array of arbitrary length, containing non-normalized phone number strings which may include dashes, parentheses, and whitespace.
  - If a country code ("1") is present in a phone number, it may be preceded by a "+" sign.
  - Phone numbers always consist of ten digits, excluding the optional country code.
  - The array itself is the root level object of the JSON file.

- Implement a new rule for determining connectedness:
  - Two Persons are connected if at least one has the other’s phone number in their contacts list.


## Part 4: Running Your Program

- Your program should take a Person ID as a command-line argument.
- It prints out a list of connected persons in the format `ID: First Last`, each on a new line, ordered by ID.
- Assume the existence of two text files in the same directory: `persons.json` and `contacts.json`.
- The program combines rules from Parts 2 and 3, indicating two persons can be connected through either or both rules.


**Note**: You have the option to utilize AI in completing the exercise. We are open to evaluating code created with or without AI assistance. However, it is **mandatory** to declare if AI was used at any stage of your solution in your submission. Be advised, solutions crafted with AI support are subject to more rigorous criteria concerning their completeness, readability, and overall performance.

## Submission Guidelines

Candidates are expected to submit their project via a version control system (e.g., Git) repository. The repository should include the source code, tests, documentation, and any additional instructions necessary for running the project.

