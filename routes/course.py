"""Routes for the course resource.
"""

from run import app
from flask import request
from http import HTTPStatus
import data
import json
import datetime

@app.route("/course/<int:id>", methods=['GET'])
def get_course(id):
    """Get a course by id.

    :param int id: The record id.
    :return: A single course (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------   
    1. Bonus points for not using a linear scan on your data structure.
    """
    # YOUR CODE HERE
    course = data.courses.get(id)
    if(not course):
        message = "Course {} does not exist".format(id)
        return {"message": message}, 404
    ret_course = course.copy()
    ret_course.pop('id')
    return {'data' : ret_course}



@app.route("/course", methods=['GET'])
def get_courses():
    """Get a page of courses, optionally filtered by title words (a list of
    words separated by commas".

    Query parameters: page-number, page-size, title-words
    If not present, we use defaults of page-number=1, page-size=10

    :return: A page of courses (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    ------------------------------------------------------------------------- 
    1. Bonus points for not using a linear scan, on your data structure, if
       title-words is supplied
    2. Bonus points for returning resulted sorted by the number of words which
       matched, if title-words is supplied.
    3. Bonus points for including performance data on the API, in terms of
       requests/second.
    """
    # YOUR CODE HERE
    args=request.args
    pagenumber=int(args.get('page-number',1))
    pagesize=int(args.get('page-size',10))
    titlewords = args.get('title-words',None)
    
    data1=[]
    if titlewords:
        for i in data.courses.values():
            c=0
            for j in titlewords:
                if j in i['title']:
                    c+=1
            if c:
                data1.insert(c, i)
        data1=data1[::-1]
        data1=data1[(pagenumber-1)*pagesize+1: pagesize*pagenumber]
        metadata={"page_count":-(-len(data1)//pagesize),
                "page_number":pagenumber,
                "page_size":pagesize,
                'record_count':len(data1)}
    else:
        for i in range((pagenumber-1)*pagesize+1, pagesize*pagenumber):
            data1.append(data.courses[i])
        metadata={"page_count":-(-len(data.courses)//pagesize),
                "page_number":pagenumber,
                "page_size":pagesize,
                'record_count':len(data.courses)}
    
    return json.dumps({'data':data1, 'metadata':metadata}), 200, {'ContentType':'application/json'} 
    
def validate_post_data(post_data):

    if "id" in post_data and "date_created" in post_data and "date_updated" in post_data and "on_discount" in post_data \
        and "price" in post_data and "title" in post_data:
        return True
    else:
        return False

@app.route("/course", methods=['POST'])
def create_course():
    """Create a course.
    :return: The course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the POST body fields
    """
    # YOUR CODE HERE
    title = request.json.get('title')
    price = request.json.get('price')
    description = request.json.get('description')
    discount_price = request.json.get('discount_price')
    on_discount = request.json.get('on_discount')
    image_path = request.json.get('image_path')

    date_created = datetime.datetime.now().isoformat()
    date_updated = date_created

    data.last_id = data.last_id +1
    _id = data.last_id


    course = {
            'title': title,
            'price': price,
            'description': description,
            'discount_price': discount_price,
            'on_discount': on_discount,
            'image_path': image_path,
            'date_created': date_created,
            'date_updated': date_updated,
            'id': _id
            }
    data.courses[_id] = course
    return {"data": course}, 201



@app.route("/course/<int:id>", methods=['PUT'])
def update_course(id):
    """Update a a course.
    :param int id: The record id.
    :return: The updated course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the PUT body fields, including checking
       against the id in the URL

    """
    # YOUR CODE HERE
    _id = request.json.get('id')
    title = request.json.get('title')
    price = request.json.get('price')
    description = request.json.get('description')
    discount_price = request.json.get('discount_price')
    on_discount = request.json.get('on_discount')
    image_path = request.json.get('image_path')

    if id != _id :
        message =  "the id does not match the payload"
        return {"message": message}, 400

    course = data.courses.get(id)
    if not course :
        message = "Course {} does not exist".format(id)
        return {"message": message}, 404
    
    course['title'] = title
    course['price'] = price
    course['description'] = description
    course['discount_price'] = discount_price
    course['image_path'] = image_path
    course['on_discount'] = on_discount

    ret_course = course.copy()
    ret_course.pop('date_created')
    return {"data": ret_course}


@app.route("/course/<int:id>", methods=['DELETE'])
def delete_course(id):
    """Delete a course
    :return: A confirmation message (see the challenge notes for examples)
    """
    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    None
    """
    # YOUR CODE HERE
    try:
        del data.courses[id]
        return json.dumps({'message':"The specified key has been deleted"}), 200, {'ContentType':'application/json'} 
    except KeyError:
        return json.dumps({'message':f'Course {id} does not exist in file'}), 404, {'ContentType':'application/json'} 