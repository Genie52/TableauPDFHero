# TableauPDFHero
Tableau PDF Hero for your Paginating Needs!

testPDF.py is a great start - sample code that uses Tableau REST API to prove the concepts. However to make it work couple of things needs to be done

a) you need to have running Tableau Server
b) publish included Print Page Break - Example Superstore v2.twbx workbook on server
c) you need to find out ID of the view - you can do that with rest apis - I have that code in testPDF.py file

hint:

```python
 # get all the views - so we can also find out what are their IDs - we need that to reference the view for PDFs
    print('\nGET ALL THE VIEWS ACROSS ALL THE WORKBOOKS >>>')
    print('All the Views (Pager): ')
    for view in TSC.Pager(server.views):
        print("View name: ", view.name, " and View ID: ", view.id) 
```
        
I would reccomend revciewing TCS documentation - https://tableau.github.io/server-client-python/docs/ - how to work with Tableau REST APIs


    

