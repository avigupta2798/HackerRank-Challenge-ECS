"""Routines associated with the application data.
"""
import json
courses = []

def load_data():
    """Load the data from the json file.
    """
    data = []
    try :
        with open('./json/course.json') as course_data :
            data = json.loads(course_data.read())
    except Exception as e:
        print(e,"\nError opening course.json file.\n")
        return
    
    global courses
    global last_id
    courses = { dict_data['id'] : dict_data for dict_data in data }
    last_id = max(courses.keys())