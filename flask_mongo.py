import flask
from flask import Flask, render_template
from pymongo import MongoClient
import pymongo

app = Flask(__name__)

client = MongoClient()  # connects to the local host, default port mongo server (which is what we have!)
db = client.db
collection = db['CS301']


@app.route('/')
def index():
    return 'Server Works!'


@app.route('/HW1')
def hw1():
    return str(collection.count())  # Return total count of documents in the database


@app.route('/HW2')
def hw2():
    myList = []
    for doc in collection.find({"milestones.stoneable.name": "Zoho"},
                               {"twitter_username": 1, "category_code": 1,
                                "_id": 0}):  # List the twitter_username and category_code for companies that have "Zoho" as a name of a stoneable of milestones.
        myList.append(doc)  # Append each match to myList[]

    return "<br>".join(
        str(v) for v in myList)  # Join all matches with <br> separating them for cleanly formatted output


@app.route('/HW3')
def hw3():
    myList = []
    for doc in collection.find({}, {"twitter_username": 1, "_id": 0}):  # List the twitter_username for all documents;
        myList.append(doc)

    return "<br>".join(str(v) for v in myList)


@app.route('/HW4')
def hw4():
    myList = []
    for doc in collection.find({"number_of_employees": {"$gte": 5000}, "founded_year": {"$gt": 2000}},
                               {"name": 1, "founded_year": 1, "number_of_employees": 1, "total_money_raised": 1,
                                "_id": 0}):  # List the name, founded_year, number_of_employees and total_money_raised for companies whose founded_year was after 2000 and whose number_of_employees was greater than or equal to 5000.
        myList.append(doc)

    return "<br>".join(str(v) for v in myList)


@app.route('/HW6')
def hw6():
    myList = []
    for doc in collection.find({"founded_month": {"$exists": "false"}},
                               {"_id": 1}):  # List the _id for companies that do not have a founded_month field.
        myList.append(doc)

    return "<br>".join(str(v) for v in myList)


@app.route('/HW7')
def hw7():
    return str(collection.count({"funding_rounds.raised_amount": {
        "$gt": 5000000}}))  # Return a count of the number of documents whose raised_amount of funding_rounds is greater than 5 million.


@app.route('/HW9')
def hw9():
    myList = []
    for doc in collection.find({"$or": [{"founded_year": {"$gt": 2012}}, {"founded_year": {"$lt": 1805}}]},
                               {"_id": 0, "name": 1, "founded_year": 1}).sort(
        [("founded_year", pymongo.DESCENDING), ("name",
                                                pymongo.ASCENDING)]):  # List the name and founded_year for companies whose founded_year was before 1805 or whose founded_year was after 2012. Sort by founded_year in descending order then by name in ascending order.
        myList.append(doc)

    return "<br>".join(str(v) for v in myList)


@app.route('/HW10')  # Is .pretty() required?
def hw10():
    myList = []
    for doc in collection.find({"founded_year": 1800, "products.name": {"$exists": "true"}},
                               {"name": 1, "homepage_url": 1, "number_of_employees": 1, "products.name": 1,
                                "_id": 0}):  # For companies with a founded_year equal to 1800 and that have a name of products, list their name, homepage_url, number_of_employees and name of products.  Write using find().
        myList.append(doc)

    return "<br>".join(str(v) for v in myList)


@app.route('/HW12')
def hw12():
    return str(collection.count_documents({
                                              "screenshots.attribution": None}))  # List a count of the documents whose attribution of screenshots is a null value


@app.route('/HW13')
def hw13():
    myList = []
    for doc in collection.find({}, {"number_of_employees": 1, "_id": 0}).sort(
            [("number_of_employees", pymongo.DESCENDING)]).limit(
        1):  # List the maximum number_of_employees over all companies and do so without using $max.
        myList.append(doc)

    return "<br>".join(str(v) for v in myList)


# Find all companies who's name equals COMPANY_NAME
@app.route('/company/<COMPANY_NAME>')
def show_company(COMPANY_NAME):
    myList = []
    for doc in collection.find({"name": COMPANY_NAME}, {"_id": 0}):  # Find documents whose name matches COMPANY_NAME
        myList.append(doc)

    if not myList:  # If the list is empty, then a document for that company does not exist
        return "No company found"

    return "<br>".join(str(v) for v in myList)


# Find all companies who's founded_year equals the YEAR_FOUNDED parameter
@app.route('/list_companies_by_year/<YEAR_FOUNDED>')
def list_companies_by_year(YEAR_FOUNDED):
    if len(str(YEAR_FOUNDED)) != 4:  # If given year is not 4 digits, return an error
        return '<span style="color: #FF0000;">ERROR: {} is not a 4 digit number!</span>'.format(
            YEAR_FOUNDED)  # Returns error string in red (https://stackoverflow.com/questions/63922114/how-can-you-use-flask-to-make-the-text-of-your-website-blue)

    myList = []
    for doc in collection.find({"founded_year": int(YEAR_FOUNDED)},
                               {"_id": 0}):  # Check if company matches YEAR_FOUNDED
        myList.append(doc)

    if not myList:  # If list is empty, then no companies were found in the given year
        return 'No Companies Founded In The Year {}'.format(YEAR_FOUNDED)

    return "<br>".join(str(v) for v in myList)


# Get count of all companies who's founded_year equals the YEAR_FOUNDED parameter
@app.route('/count_companies_by_year/<YEAR_FOUNDED>')
def count_companies_by_year(YEAR_FOUNDED):
    if len(str(YEAR_FOUNDED)) != 4:  # If given year is not 4 digits, return an error
        return '<span style="color: #FF0000;">ERROR: {} is not a 4 digit number!</span>'.format(
            YEAR_FOUNDED)  # Returns error string in red (https://stackoverflow.com/questions/63922114/how-can-you-use-flask-to-make-the-text-of-your-website-blue)

    myList = []
    for doc in collection.find({"founded_year": int(YEAR_FOUNDED)},
                               {"_id": 0}):  # Check if company matches YEAR_FOUNDED
        myList.append(doc)

    if not myList:  # If list is empty, then no companies were found
        return 'No Companies Founded In The Year {}'.format(YEAR_FOUNDED)

    return str(len(myList))  # Return the number of companies founded in the given year


# Find the company documents with the <COMPANY_NAME> and use a built-in Flask operation to redirect the
# user's web browser to the company's crunchbase URL located in the document. If no company is found,
# return an error message as above. Use the default HTTP status code for the redirect.
@app.route('/crunchbase/redirect/<COMPANY_NAME>')
def get_crunch_base_url(COMPANY_NAME):
    myList = []
    for url in collection.find({"name": COMPANY_NAME}, {"crunchbase_url": 1,
                                                        "_id": 0}):  # Check if the name of the current company matches COMPANY_NAME
        myList.append(url)

    if not myList:
        return "No company found by the name {}".format(COMPANY_NAME)

    return flask.redirect(url["crunchbase_url"])  # Pass the crunchbase_url of the matched company to redirect
