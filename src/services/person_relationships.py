"""Module providing a person relationships"""
import json
import datetime
from src.lib.database.conn import db
from src.lib.database.migration.models.person_model import Person
from src.lib.database.migration.models.experience_model import Experience
from src.lib.database.migration.migration import Migration


class FindContactsByPersonId:
    """
    Retrieves a list of contact information for a given person ID.
    
    This class provides a way to fetch contact information for a specific person, including their phone numbers and associated contact information. The `get_query_result` method can be used to retrieve the contact data, with an optional parameter to only show contacts that match the person's phone number.
    
    Args:
        person_id (int): The ID of the person to retrieve contacts for.
    
    Returns:
        list[dict]: A list of dictionaries containing the contact information, with keys for the contact ID, owner name, nickname, phone type, phone number, and associated person name.
    """

    __query = ""
    __query_result = []
    __person_id = 0
    
    def __init__(self, person_id):
        """
        Initializes a new instance of the `PersonRelationships` class with the specified `person_id`.
        
        The `__person_id` attribute stores the ID of the person whose relationships are being managed.
        The `__query` attribute stores the SQL query that will be used to retrieve the person's contact information.
        The `__query_result` attribute stores the results of the executed SQL query.
        """
        self.__person_id            = person_id
        self.__query                =       ""
        self.__query_result         =       []
    
    def set_query(self, show_only_contacts_matching_person = False):
        """
        Sets the SQL query to retrieve phone contact information for a person, optionally filtering to only include contacts that match the person.
        
        The query retrieves the following fields:
        - phone.id
        - person.first_name || ' ' || person.last_name AS 'contact_owner_name'
        - contact.nickname
        - phone.type
        - phone.number
        - phone.contact_id
        - phone_number_person.id
        - phone_number_person.first_name || ' ' || phone_number_person.last_name AS 'contact_person_name'
        
        The query joins the person, contact, and phone tables, and optionally joins the person table again to filter to only include contacts that match the person.
        
        Args:
            show_only_contacts_matching_person (bool): If True, the query will only include contacts that match the person. If False, the query will include all contacts associated with the person.
        """
        self.__query = ""
        self.__query +=  "SELECT "
        self.__query +=      "phone.id, "
        self.__query +=      "person.first_name || ' ' || person.last_name AS 'contact_owner_name', "
        self.__query +=      "contact.nickname, "
        self.__query +=      "phone.type, "
        self.__query +=      "phone.number, "
        self.__query +=      "phone.contact_id, "
        self.__query +=      "phone_number_person.id, "
        self.__query +=      "phone_number_person.first_name || ' ' || phone_number_person.last_name AS 'contact_person_name' "
        self.__query +=  "FROM "
        self.__query +=      "person "
        self.__query +=  "JOIN "
        self.__query +=      "contact ON person.id = contact.owner_id AND contact.owner_id = ? "
        self.__query +=  "JOIN "
        self.__query +=      "phone ON phone.contact_id = contact.id "
        if(show_only_contacts_matching_person):
            self.__query +=  "JOIN "
        else:
            self.__query +=  "LEFT JOIN "
        
        self.__query +=      "person as phone_number_person ON phone_number_person.phone LIKE phone.number "
        self.__query +=  "WHERE "
        self.__query +=      "person.id = ? "
        self.__query +=  "ORDER BY "
        self.__query +=      "person.id, phone.contact_id ASC"
    
    def execute_query(self):
        """
        Executes the SQL query stored in the `__query` attribute and populates the `__query_result` attribute with the results.
        
        The method iterates over the cursor returned by the `execute_sql` function and creates a dictionary for each row, storing the relevant data in the dictionary. The dictionary is then appended to the `__query_result` list.
        
        Returns:
            list: The query result stored in the `__query_result` attribute.
        """
        self.__query_result = []
        cursor = db.execute_sql('{}'.format(self.__query), (self.__person_id, self.__person_id))
        for value in cursor:
            id, contact_owner_name, nickname, type, number, contact_id, id, contact_person_name = value
            data = {
                'id'                    :       id,
                'contact_owner_name'    :       contact_owner_name,
                'nickname'              :       nickname,
                'type'                  :       type,
                'number'                :       number,
                'contact_id'            :       contact_id,
                'id'                    :       id,
                'contact_person_name'   :       contact_person_name
            }
            self.__query_result.append(data)
        return self.__query_result
    
    def get_query_result(self, show_only_contacts_matching_person = False):
        """
        Retrieves the query result stored in the `__query_result` attribute.
        
        Args:
            show_only_contacts_matching_person (bool, optional): If True, the query will only return experiences that match the person ID specified in the class. Defaults to False.
        
        Returns:
            list: The query result stored in the `__query_result` attribute.
        """
        self.set_query(show_only_contacts_matching_person)
        self.execute_query()
        return self.__query_result
    

class FindExperiencesWithPermanenceDays:
    """
    A class that provides methods to retrieve related experiences from a person's experiences.
    
    The `FindExperiencesWithPermanenceDays` class is responsible for fetching a person's experiences and finding related experiences based on certain criteria, such as minimum permanence days.
    
    The main methods provided by this class are:
    - `set_query`: Constructs and executes a SQL query to retrieve experience data for a given person, filtering by company name, minimum permanence days, and excluding the person's own experience.
    - `get_query_binds`: Constructs the query binds for the SQL query executed in the `execute_query` method.
    - `execute_query`: Executes the query and populates the `__query_result` attribute with the results.
    - `get_query_result`: Retrieves the query result stored in the `__query_result` attribute.
    """
    
    __query = ""
    __query_result = []
    
    company_name           =      ''
    min_permanence_days    =      90
    person_id              =      00
    start_date             =      None
    end_date               =      None
    
    def __init__(self, company_name='', start_date = None, end_date = None, min_permanence_days = 90, person_id = 0):
        """
        Initializes a PersonRelationships object with the provided parameters.
        
        Args:
            company_name (str, optional): The name of the company to filter experiences by. Defaults to an empty string.
            start_date (datetime.date, optional): The start date to filter experiences by. Defaults to today's date minus the minimum permanence days plus one day.
            end_date (datetime.date, optional): The end date to filter experiences by. Defaults to today's date.
            min_permanence_days (int, optional): The minimum number of days a person must have been employed at a company to be included in the results. Defaults to 90 days.
            person_id (int, optional): The ID of the person whose experiences should be excluded from the results. Defaults to 0.
        """
        
        self.company_name           =       company_name
        self.min_permanence_days    =       min_permanence_days
        self.person_id              =       person_id
        self.start_date             =       datetime.date.today() - datetime.timedelta(days=min_permanence_days+1) if start_date is None else datetime.date.fromisoformat(str(start_date))
        self.end_date               =       datetime.date.today() if end_date is None else datetime.date.fromisoformat(str(end_date))
        self.start_date             =       str(self.start_date)
        self.end_date               =       str(self.end_date)
        self.__query                =       ""
        self.__query_result         =       []

    def date_range_gte_min_perm(self, start_date, end_date):
        """
        Checks if the date range between the provided `start_date` and `end_date` is greater than or equal to the minimum permanence days specified in the class.
        
        Args:
            start_date (str): The start date in ISO format.
            end_date (str): The end date in ISO format.
        
        Returns:
            bool: True if the date range is greater than or equal to the minimum permanence days, False otherwise.
        """
        return (datetime.date.fromisoformat(str(end_date)) - datetime.date.fromisoformat(str(start_date))).days >= self.min_permanence_days

    def set_query(self):
        """
        Constructs and executes a SQL query to retrieve experience data for a given person, filtering by company name, minimum permanence days, and excluding the person's own experience.
        
        The query selects the following fields:
        - `e.id`: The unique identifier for the experience record.
        - `e.person_id`: The person ID associated with the experience record.
        - `e.company`: The company name for the experience record.
        - `e.title`: The job title for the experience record.
        - `(JULIANDAY(COALESCE(end_date, CURRENT_DATE)) - JULIANDAY(start_date)) as 'permanence_days'`: The number of days the person was employed at the company.
        - `e.start_date`: The start date for the experience record.
        - `e.end_date`: The end date for the experience record.
        
        The query filters the results to only include experiences where:
        - The company name matches the provided `company_name` (using a LIKE query with wildcards).
        - The permanence days are greater than or equal to the provided `min_permanence_days`.
        - The person ID is not equal to the provided `person_id`.
        - The start date is less than or equal to the provided `end_date` minus the `min_permanence_days`.
        
        The results are ordered by `e.id` and `e.person_id` in ascending order.
        """
        self.__query = ""
        self.__query +=    "SELECT  "
        self.__query +=        "e.id, "
        self.__query +=        "e.person_id, "
        self.__query +=        "e.company, "
        self.__query +=        "e.title, "
        self.__query +=        "(JULIANDAY(COALESCE(end_date, CURRENT_DATE)) - JULIANDAY(start_date)) as 'permanence_days', "
        self.__query +=        "e.start_date, "
        self.__query +=        "e.end_date "
        self.__query +=    "FROM  "
        self.__query +=        "experience as e "
        self.__query +=    "WHERE "
        self.__query +=        "e.company like ? "
        self.__query +=    "AND "
        self.__query +=        "permanence_days >= ? "
        self.__query +=    "AND "
        self.__query +=        "person_id <> ? "
        self.__query +=    "AND "
        self.__query +=        "start_date <= ? " # start_date lte (self.end_date - self.min_permanence_days)
        self.__query +=     "ORDER BY "
        self.__query +=         "e.id, e.person_id ASC"
    
    def get_query_binds(self):
        """
        Constructs the query binds for the SQL query executed in the `execute_query` method.
        
        The binds include:
        - `company`: A wildcard-enclosed version of the `company_name` attribute, used for a LIKE query.
        - `permanence_days`: The `min_permanence_days` attribute, converted to an integer.
        - `person_id`: The `person_id` attribute, converted to an integer.
        - `start_date`: The `end_date` attribute minus `permanence_days` days, converted to a string.
        
        These binds are used to parameterize the SQL query and provide the necessary values for the query execution.
        """
        company = "%{}%".format(self.company_name)
        permanence_days = int(self.min_permanence_days)
        person_id = int(self.person_id)
        start_date = datetime.date.fromisoformat(str(self.end_date)) - datetime.timedelta(days=permanence_days)
        start_date = str(start_date)
        return (company, permanence_days, person_id, start_date)
    
    def execute_query(self):
        """
        Executes the query and populates the `__query_result` attribute with the results.
        
        If the date range is not valid (i.e. the `end_date` is less than `min_permanence_days` days after the `start_date`), a warning message is printed and an empty list is returned.
        
        The method uses the `get_query_binds()` method to get the parameter bindings for the query, and then executes the query using the `db.execute_sql()` method. The results are then iterated over and added to the `__query_result` list as dictionaries, with keys for the various fields (id, person_id, company, title, permanence_days, start_date, end_date).
        
        Finally, the `__query_result` list is returned.
        """
        date_range_is_valid = self.date_range_gte_min_perm(self.start_date, self.end_date)
        if not date_range_is_valid:
            print('Invalid date range of {}, {} is not gte {} days'. format(self.start_date, self.end_date, self.min_permanence_days))
            return []
        binds = self.get_query_binds()
        query = '{}'.format(self.__query)

        cursor = db.execute_sql(query, binds)
        
        for value in cursor:
            id, person_id, company, title, permanence_days, start_date, end_date = value
            data = {
                'id'                    :       id,
                'person_id'             :       person_id,
                'company'               :       company,
                'title'                 :       title,
                'permanence_days'       :       permanence_days,
                'start_date'            :       start_date,
                'end_date'              :       end_date
            }
            self.__query_result.append(data)
        return self.__query_result
    
    def get_query_result(self):
        """
        Retrieves the query result stored in the `__query_result` attribute.
        
        This method first sets the query by calling the `set_query()` method, then executes the query by calling the `execute_query()` method, and finally returns the stored query result.
        """
        self.set_query()
        self.execute_query()
        return self.__query_result
    
    def __repr__(self):
        """
        Provides a string representation of the `FindExperiencesWithPermanenceDays` object, displaying its key attributes such as company name, minimum permanence days, person ID, start date, end date, and query results.
        
        This method is primarily used for debugging and logging purposes, as it allows for a concise and readable display of the object's state.
        """
        l = [7, 0, 10, 9, 11]
        print('company_name'         ,  ': ', ' '*l[0]      ,    self.company_name)
        print('min_permanence_days'  ,  ': ', ' '*l[1]      ,    self.min_permanence_days)
        print('person_id'            ,  ': ', ' '*l[2]      ,    self.person_id)
        print('start_date'           ,  ': ', ' '*l[3]      ,    self.start_date)
        print('end_date'             ,  ': ', ' '*l[4]      ,    self.end_date)
        print('query_results'        ,  ': ', ' '*l[4]      ,    self.__query_result)
                
        return list((self.company_name, self.min_permanence_days, self.person_id, self.start_date, self.end_date, self.__query_result))



class RelatedExperiencesFromExperience():
    """
    A class that provides methods to retrieve related experiences from a person's experiences.
    
    The `RelatedExperiencesFromExperience` class is responsible for fetching a person's experiences and finding related experiences based on certain criteria, such as minimum permanence days.
    
    The main methods provided by this class are:
    - `set_person_by_id`: Sets the person object based on the provided person ID.
    - `get_person_by_id`: Returns the person object based on the provided person ID.
    - `get_person_experiences_by_person_id`: Returns the list of experiences for the given person ID.
    - `set_related_experiences_from_person_experiences`: Sets the list of related experiences based on the person's experiences and the minimum permanence days.
    - `get_related_experiences_from_person_experiences`: Returns the list of related experiences based on the person's experiences and the minimum permanence days.
    """
    
    _related_from_experiences:list[Experience] = []
    _person_id = 0
    _person:Person = None
    
    def __init__(self, person_id = 0):
        """
        Initializes a new instance of the class with the given person_id.
        
        Args:
            person_id (int): The ID of the person. Defaults to 0 if not provided.
        
        Attributes:
            _related_from_experiences (list[Experience]): A list of related experiences for the person.
            _person_id (int): The ID of the person.
        """
        self._related_from_experiences = []
        self._person_id = person_id        

    def set_person_by_id(self, person_id=None):
        """
        Sets the Person object associated with this instance based on the provided person_id.
        
        If person_id is None, it will use the _person_id attribute of the current instance.
        
        If the _person attribute is not None and its id matches the provided person_id, this method will simply return the current instance without making any changes.
        
        Otherwise, it will retrieve the Person object with the given person_id and set it as the _person attribute of the current instance. It will then return the current instance.
        """
        if person_id is None:
            person_id = self._person_id
        if self._person is not None and self._person.id == person_id:
            return self
        
        self._person = Person.get_by_id(self._person_id)
        return self
    
    def get_person_by_id(self, person_id=None) -> Person:
        """
        Gets the person object by their ID.
        
        Args:
            person_id (int, optional): The ID of the person to retrieve. If not provided, the `_person_id` attribute will be used.
        
        Returns:
            Person: The person object with the specified ID.
        """
        if person_id is None:
            person_id = self._person_id
        return self.set_person_by_id(person_id=person_id)._person
    
    def get_person_experiences_by_person_id(self, person_id=None) -> list[Experience]:
        """
        Gets the list of experiences for a person by their ID.
        
        Args:
            person_id (int, optional): The ID of the person to get experiences for. If not provided, the `_person_id` attribute will be used.
        
        Returns:
            list[Experience]: A list of experiences for the specified person.
        """
        if person_id is None:
            person_id = self._person_id
        person = self.get_person_by_id(person_id=person_id)
        return person.experiences
    
    
    def set_related_experiences_from_person_experiences(self, person_id=None, min_permanence_days=90) -> list[Experience]:
        """
        Sets the related experiences for a person based on their existing experiences, filtering for a minimum number of permanence days.
        
        Args:
            person_id (int, optional): The ID of the person to get related experiences for. If not provided, the `_person_id` attribute will be used.
            min_permanence_days (int, optional): The minimum number of days a person must have been in an experience for it to be considered related. Defaults to 90 days.
        
        Returns:
            list[Experience]: A list of related experiences for the person.
        """
        if person_id is None:
            person_id = self._person_id

        self._related_from_experiences = []
        
        person_exp = self.get_person_experiences_by_person_id(person_id)
        
        for exp in person_exp:
            find_experiences_with_permanence_days = FindExperiencesWithPermanenceDays(
                company_name=exp.company,
                start_date=exp.start_date,
                end_date=exp.end_date,
                min_permanence_days=min_permanence_days,
                person_id=exp.person.id
            )
            related_by_experience = find_experiences_with_permanence_days.get_query_result()
            for related in related_by_experience:
                self._related_from_experiences.append(Experience(
                    person=related['person_id'],
                    company=related['company'],
                    title=related['title'],
                    start_date=related['start_date'],
                    end_date=related['end_date']
                ))
        
        return self
            
    def get_related_experiences_from_person_experiences(self, person_id=None, min_permanence_days=90):
        """
        Gets the related experiences from the person's experiences, filtered by a minimum permanence days.
        
        Parameters:
        - person_id (Optional[str]): The ID of the person to get related experiences for.
        - min_permanence_days (int): The minimum number of days a person must have an experience to be considered related.
        
        Returns:
        A list of related experiences from the person's experiences.
        """
        self.set_related_experiences_from_person_experiences(person_id=person_id, min_permanence_days=min_permanence_days)
        return self._related_from_experiences


class PersonRepository(RelatedExperiencesFromExperience):
    """
    Provides a repository for managing person relationships, including relationships based on shared experiences and contacts.
    
    The `PersonRepository` class extends the `RelatedExperiencesFromExperience` class and provides methods for retrieving a person's relationships, both based on shared experiences and contacts.
    
    The `get_person_relationships` method returns a dictionary containing two lists: `by_experiences` and `by_contacts`. The `by_experiences` list contains dictionaries representing related people based on shared experiences, and the `by_contacts` list contains dictionaries representing related people based on shared contacts.
    """
    
    _person:Person = None
    _experiences:list[Experience] = []
    
    def __init__(self, person_id=None):
        """
        Initializes a new instance of the PersonRelationshipsService class with the specified person ID.
        
        Parameters:
        - person_id (int, optional): The ID of the person to associate with this instance.
        """
        super().__init__(person_id=person_id)
    
    
    def get_person(self, person_id=None):
        """
        Retrieves a person by their ID.
        
        Parameters:
        - person_id (int, optional): The ID of the person to retrieve.
        
        Returns:
        The person with the specified ID.
        """
        return super().get_person_by_id(person_id=person_id)
    
    def get_person_experiences(self, person_id=None):
        """
        Retrieves the experiences for a person based on their person ID.
        
        Parameters:
        - person_id (int, optional): The ID of the person to retrieve experiences for.
        
        Returns:
        A list of experiences for the specified person.
        """
        return super().get_person_experiences_by_person_id(person_id=person_id)
    
    def get_person_related_people_by_experiences(self, person_id=None, min_permanence_days=90):
        """
        Retrieves the related experiences for a person based on the minimum number of days they have been in an experience.
        
        Parameters:
        - person_id (int, optional): The ID of the person to retrieve related experiences for.
        - min_permanence_days (int, optional): The minimum number of days a person must have been in an experience for it to be considered related. Defaults to 90.
        
        Returns:
        A list of related experiences for the person, based on the specified minimum permanence days.
        """
        return super().get_related_experiences_from_person_experiences(person_id=person_id, min_permanence_days=min_permanence_days)
    
    def get_person_related_people_by_contacts(self, person_id=None, only_contacts_with_related_person=True):
        """
        Retrieves the contacts of a person, optionally only including contacts with related people.
        
        Parameters:
        - person_id (int, optional): The ID of the person to retrieve contacts for.
        - only_contacts_with_related_person (bool, optional): A flag indicating whether to only include contacts with related people. Defaults to True.
        
        Returns:
        A list of contact information for the person, optionally filtered to only include contacts with related people.
        """
        person = self.get_person(person_id=person_id)
        return FindContactsByPersonId(person.id).get_query_result(only_contacts_with_related_person)
    def get_person_relationships(self, person_id=None, min_permanence_days=90, only_contacts_with_related_person=True):
        """
        Retrieves the relationships of a person based on shared experiences and contacts.

        Parameters:
        - person_id (int, optional): The ID of the person to retrieve relationships for. Defaults to None.
        - min_permanence_days (int, optional): The minimum number of days a person must have been in an experience for it to be considered related. Defaults to 90.
        - only_contacts_with_related_person (bool, optional): A flag indicating whether to only include contacts with related people. Defaults to True.

        Returns:
        A dictionary containing two lists: 'by_experiences' and 'by_contacts'. Each list contains dictionaries representing related people based on shared experiences and contacts, respectively.
        """
        person_relationship = {
            'by_experiences': [],
            'by_contacts': [],
        }
        # print('get_person_related_people_by_experiences')
        person_experiences = self.get_person_related_people_by_experiences(person_id=person_id, min_permanence_days=min_permanence_days)
        for related_from_experience in person_experiences:
            related_from_experience.__data__['person'] = related_from_experience.person.__data__
            person_relationship['by_experiences'].append(related_from_experience.__data__)
            # print2(related_from_experience.__data__)
        
        # print('get_person_related_people_by_contacts')
        person_contacts = self.get_person_related_people_by_contacts(person_id=person_id, only_contacts_with_related_person=only_contacts_with_related_person)
        for related_from_contact in person_contacts:
            person_relationship['by_contacts'].append(related_from_contact)
            # print2(related_from_contact)
        
        person = self.get_person(person_id=person_id)
        person.__data__['relationships'] = person_relationship
        return person.__data__;

def print2(data):
    """
    Prints the provided data in a formatted way.
    
    If the data is a list, it will be printed as a JSON-formatted list with indentation. Otherwise, it will be printed as a single-element JSON-formatted list with indentation.
    
    If there is an error during the printing, the raw data will be printed instead.
    """
    # Print the param __name__ and __value__
    print(getattr(data, '__name__', '') or '')
    try:
        if isinstance(data, list):
            print(json.dumps(data, indent=2))
        else:
            print(json.dumps([data], indent=2))
    except:
        print(data)



def execute(person_id):
    """
    Executes a migration and retrieves the person relationships for the given person ID. Prints the person's relationships by experiences and contacts.
    
    Parameters:
    - person_id (int): The ID of the person to retrieve relationships for.
    
    Returns:
    None
    """
    Migration()
    person_relation_ships = PersonRepository(person_id=person_id).get_person_relationships(person_id=person_id)
    print2(person_relation_ships)
    print('-'*64)
    print(person_relation_ships['id'], ' | ', person_relation_ships['first_name'], person_relation_ships['last_name'])
    for relationships_by_experience in person_relation_ships['relationships']['by_experiences']:
        print(relationships_by_experience['person']['id'], ' | ', relationships_by_experience['person']['first_name'], relationships_by_experience['person']['last_name'])
    
    for relationships_by_contacts in person_relation_ships['relationships']['by_contacts']:
        print(relationships_by_contacts['id'], ' | ', relationships_by_contacts['contact_person_name'])
