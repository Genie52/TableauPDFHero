# import Flask library (class) that has needed functionality to build Web Server
# import render_template - this is library that works with Flask Jinja (HTML) templates
# import request - to access incoming request data, you can use the global request object.
# Flask parses incoming request data for you and gives you access to it through that global object.
# import flask_wtf and wtfforms are libraries that will help us with the form data

from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from  wtforms import StringField, SubmitField
import requests
import tableauserverclient as TSC

app = Flask(__name__)

# initializin global variables
tableau_ticket_return = ''
username = ''

# this secret key is here a string just so we have forms working - if you want to know more google it ;-)
app.config['SECRET_KEY'] = 'somesecretkey'

# instance the form class - inheritance is from the FlaskForm.
# You can name the calss as you like - we named it "UserForm"
class UserForm(FlaskForm):
    # Below are the form fields we want to be able to capture and send (in our case just the username) to Tableau server.
    # These are used as form attributes in .html file
    # in the quotes is the text user weill see when using the form
    username = StringField("Username:")
    password = StringField("Password:")
    submitForm = SubmitField("Login!")

@app.route('/', methods=['GET','POST']) #make sure you setup GET and POST for our landing page - becaue form will be there ;-)
def index():
    global username
    username = False
    # instance the form! we will send this to our HTML template below in the code
    form = UserForm()

    # check if form is calid on submission (also how to read those form fields)
    if form.validate_on_submit():
        # we are just reading the username! this is because Tableau Server just expects a username as parameter (in this case)
        username = form.username.data
        # in previous line we have already saved the value of username so lets sut reset it to empty string now
        form.username.data = ''
        # now we are referencing the tableau_ticket_return from the top!
        global tableau_ticket_return
        tableau_ticket_return = requests.post("http://192.168.0.11/trusted?username=" + username)

    # sending all the variables and form to HTML template
    return render_template('index-tableau.html', form = form, username = username, tableau_ticket_return = tableau_ticket_return)

@app.route('/loginTableauPage')
def loginTableauPage():
    return render_template('loginTableauPage-Finish.html', tableau_ticket = tableau_ticket_return.text, username = username)
    #return render_template('loginTableauPage-Start.html', tableau_ticket = tableau_ticket_return.text, username = username)

@app.route('/printPDF', methods=['POST','GET'])
def printPDF():
    
    if request.method == 'POST':
        print("Detected POST method!")
        results = request.form
        print("\nResults from HTML form -> ", results)

        stateResult = results['stateFilter']
        print("\nState Filter -> ", stateResult)

        subCResult = results['subCFilter']
        print("\nsub-Category Filter -> ", subCResult)       




    tableau_auth = TSC.TableauAuth('admin', 'admin')
    server = TSC.Server('http://192.168.0.11', use_server_version = True) #use_server_version = True gives us the latest REST API version to work with
    
    #sign in to Tableau Server and do the things below
    with server.auth.sign_in(tableau_auth): 
        #show REST API sevrer version
        tableau_server_version =  server.version
        print('\nTableau Server Version:', server.version,'\n') #3.4 is 2019.2

        print('\nGET ALL THE VIEWS ACROSS ALL THE WORKBOOKS >>>')
        print('All the Views (Pager): ')
        for view in TSC.Pager(server.views):
            print("View name: ", view.name, " and View ID: ", view.id)  #this line repeats for every View available - thats why they are printed one after another
        
        # set the PDF request options
        pdf_req_option = TSC.PDFRequestOptions(page_type=TSC.PDFRequestOptions.PageType.A4, orientation=TSC.PDFRequestOptions.Orientation.Landscape)

        # (optional) set a view filter
        pdf_req_option.vf('State', 'Alabama')

        # print PDF
        for view in TSC.Pager(server.views):
            if view.id == '88aa3d1f-f294-4af4-be1a-bc70b0242526':
                server.views.populate_pdf(view, pdf_req_option)
                with open('./view_pdf.pdf', 'wb') as f:
                    f.write(view.pdf)

        #get this from the database table you are using as filter (dimension) in Tableau 
        # if you need more granular have filters for each level of granularity you need
        #stateFilter = ['Alabama', 'Arizona','Arkansas','California','Colorado','Iowa','Kansas','Texas']
        #subCategory = ['Chairs', 'Art', 'Machines', 'Phones']

        stateFilter = [stateResult]
        subCategory = [subCResult]

        # lets filter only for the State
        for state in stateFilter:
            pdf_req_option = TSC.PDFRequestOptions(page_type=TSC.PDFRequestOptions.PageType.A4, orientation=TSC.PDFRequestOptions.Orientation.Landscape)
            pdf_req_option.vf('State', state)
            print("Printing PDF -->", "view_pdf - " + state + " -.pdf")

            for view in TSC.Pager(server.views):
                if view.id == '88aa3d1f-f294-4af4-be1a-bc70b0242526':
                    server.views.populate_pdf(view, pdf_req_option)
                    with open('./view_pdf - ' + state + ' -.pdf', 'wb') as f:
                        f.write(view.pdf)

        #now lets filter for each State and Sub-Category
        for state in stateFilter:
            for subC in subCategory:
                pdf_req_option = TSC.PDFRequestOptions(page_type=TSC.PDFRequestOptions.PageType.A4, orientation=TSC.PDFRequestOptions.Orientation.Landscape)
                pdf_req_option.vf('State', state)
                pdf_req_option.vf('Sub-Category', subC)
                print("Printing PDF -->", "view_pdf - " + state + " and subCat " + subC + " -.pdf")

                for view in TSC.Pager(server.views):
                    if view.id == '88aa3d1f-f294-4af4-be1a-bc70b0242526':
                        server.views.populate_pdf(view, pdf_req_option)
                        with open('./view_pdf - ' + state + ' - ' + subC + ' -.pdf', 'wb') as f:
                            f.write(view.pdf)
    
    return render_template('printPDF.html')


if __name__ == '__main__':
    app.run()
