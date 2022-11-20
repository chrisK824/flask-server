import requests
import json
import random
from time import sleep

baseURL = 'http://127.0.0.1:5000'

males = [
    'Chris', 'Christian', 'Jordan', 'Jim', 'Dimitris',
    'Mitsos', 'Filipo', 'Robert', 'Damien', 'Todd',
    'Michael', 'Mike', 'Masum', 'Nikos', 'Menelaos',
    'Menios', 'Mark', 'Marcus', 'Charlie', 'Elias'
]

females = [
    'Marta', 'Nadine', 'Eviliana', 'Amanda', 'Sachin',
]

lastnames = [
    'Red', 'Green', 'Blue', 'White', 'Black', 'Yellow',
    'Orange', 'Purple', 'Brown', 'Hazel', 'Grey', 'Pink'
]

nationalities = [
    'Greek', 'English', 'Irish', 'Italian',
    'Bosnian', 'Spanish', 'Scotish'
]

bookNames = [
    'Chris', 'Christian', 'Jordan', 'Jim', 'Dimitris',
    'Mitsos', 'Filipo', 'Robert', 'Damien', 'Todd',
    'Michael', 'Mike', 'Masum', 'Nikos', 'Menelaos',
    'Menios', 'Mark', 'Marcus', 'Charlie', 'Elias'
]

authors = [
    'Marta', 'Nadine', 'Eviliana', 'Amanda', 'Sachin',
]

categories = [
    'Red', 'Green', 'Blue', 'White', 'Black', 'Yellow',
    'Orange', 'Purple', 'Brown', 'Hazel', 'Grey', 'Pink'
]


def createMembers(count):
    counter = 0
    while counter < count:
        name = random.choice(random.choice([males, females]))
        lastname = random.choice(lastnames)
        username = name.lower() + str(random.randint(0, 9999))
        email = username.lower() + "gmail.com"
        nationality = random.choice(nationalities)
        gender = 'male'
        if name in females:
            gender = 'female'
        password = list(name+lastname)
        random.shuffle(password)
        password = ''.join(password)

        data = {
            "name": name,
            "lastname": lastname,
            "username": username,
            "password": password,
            "email": email,
            "age": random.randint(18, 55),
            "nationality": nationality,
            "gender": gender
        }
        response = requests.post(baseURL + "/members",
                                 headers={'content-type': 'application/json'},
                                 data=json.dumps(data))
        if response.status_code == 200:
            counter = counter + 1
        sleep(0.1)


def getMembers():
    response = requests.get(baseURL + "/members")
    payload = json.loads(response.text)
    print(json.dumps(payload, indent=4))
    return payload['result']


def deleteMembers(count):
    members = getMembers()
    members_ids = [member['id'] for member in members]
    counter = 0
    while counter < count and len(members_ids) >= 1:
        picked_id = random.choice(members_ids)
        response = requests.delete(baseURL + "/members/" + picked_id)
        if response.status_code == 200:
            counter = counter + 1
            members_ids.remove(picked_id)
        sleep(0.1)


def createBooks(count):
    counter = 0
    while counter < count:
        name = random.choice(bookNames)
        author = random.choice(authors)
        category = random.choice(categories)
        pages = random.randint(150, 750)
        publish_date = random.randint(1920, 2019)
        copies = random.randint(10, 100)

        data = {
            "name": name,
            "author": author,
            "category": category,
            "pages": pages,
            "publish_date": publish_date,
            "copies": copies,
            "copies_available": copies
        }
        response = requests.post(
            baseURL + "/books", headers={'content-type': 'application/json'},
            data=json.dumps(data))
        if response.status_code == 200:
            counter = counter + 1
        sleep(0.1)

def getBooks():
    response = requests.get(baseURL + "/books")
    payload = json.loads(response.text)
    print(json.dumps(payload, indent=4))
    return payload['result']


def deleteBooks(count):
    books = getBooks()
    books_ids = [book['id'] for book in books]
    counter = 0
    while counter < count and len(books_ids) >= 1:
        picked_id = random.choice(books_ids)
        response = requests.delete(baseURL + "/books/" + picked_id)
        if response.status_code == 200:
            counter = counter + 1
            books_ids.remove(picked_id)
        sleep(0.1)


createMembers(10)
getMembers()
deleteMembers(5)
getMembers()
createBooks(10)
getBooks()
deleteBooks(5)
getBooks()

