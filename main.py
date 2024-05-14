from src.services.person_relationships import execute
def main(person_id=0):
    execute(person_id)
    

if __name__ == "__main__":
    import sys
    person_id = int(sys.argv[1])
    main(person_id)