# import TSC library - wrapper for Tableau REST API
# https://tableau.github.io/server-client-python/docs/
import tableauserverclient as TSC

# login as admin
tableau_auth = TSC.TableauAuth('admin', 'admin')

# if you want to impersonate user you need to know user ID
# tableau_auth = TSC.TableauAuth('admin', 'admin', user_id_to_impersonate='223510e8-3bf5-4971-bf00-b2146092b957')

# connect to your tableau server
server = TSC.Server('http://192.168.0.11', use_server_version = True) #use_server_version = True gives us the latest REST API version to work with
    
#sign in to Tableau Server and do the things below
with server.auth.sign_in(tableau_auth): 

    #show REST API sevrer version
    tableau_server_version =  server.version
    print('\nTableau Server Version:', server.version,'\n') #3.4 is 2019.2
    
    # with this we can find out users on server and their IDs!
    print('\nGET USERS NAMES AND LUIDs >>>')
    all_users, pagination_item = server.users.get()
    print('All the Users: ',[user.name for user in all_users])
    print('IDs of the Users: ',[user.id for user in all_users])

    # get all the views - so we can also find out what are their IDs - we need that to reference the view for PDFs
    print('\nGET ALL THE VIEWS ACROSS ALL THE WORKBOOKS >>>')
    print('All the Views (Pager): ')
    for view in TSC.Pager(server.views):
        print("View name: ", view.name, " and View ID: ", view.id)  #this line repeats for every View available - thats why they are printed one after another
    
    # set the PDF request options
    # https://tableau.github.io/server-client-python/docs/api-ref#pdfrequestoptions-class
    pdf_req_option = TSC.PDFRequestOptions(page_type=TSC.PDFRequestOptions.PageType.A4, orientation=TSC.PDFRequestOptions.Orientation.Landscape)

    # (optional) set a view filter (you can setup like this multiple filters)
    pdf_req_option.vf('State', 'Alabama')

    # print PDF - here is simple one time go example - no filters 
    # https://tableau.github.io/server-client-python/docs/api-ref#views
    for view in TSC.Pager(server.views):
        # this is ID of view we want to export to PDF
        if view.id == '88aa3d1f-f294-4af4-be1a-bc70b0242526':
            server.views.populate_pdf(view, pdf_req_option)
            with open('./view_pdf.pdf', 'wb') as f:
                f.write(view.pdf)

    # now we gonna print PDFs in paginated way using the following filters 
    # of course you can get this infromation (about data in filters) in multiple ways - database, manually, file 
    # or as will show later from HTML page with embedded Tableau view
    stateFilter = ['Alabama', 'Arizona','Arkansas','California','Colorado','Iowa','Kansas','Texas'] # just example
    subCategory = ['Chairs', 'Art', 'Machines', 'Phones']

    # lets filter only for the State
    for state in stateFilter:
        pdf_req_option = TSC.PDFRequestOptions(page_type=TSC.PDFRequestOptions.PageType.A4, orientation=TSC.PDFRequestOptions.Orientation.Landscape)
        pdf_req_option.vf('State', state) # name of the filter (State) is the same as in Tableau workbook 
        print("Printing PDF -->", "view_pdf - " + state + " -.pdf")

        for view in TSC.Pager(server.views):
            # this is ID of view we want to export to PDF
            if view.id == '88aa3d1f-f294-4af4-be1a-bc70b0242526':
                server.views.populate_pdf(view, pdf_req_option)
                with open('./view_pdf - ' + state + ' -.pdf', 'wb') as f:
                    f.write(view.pdf)

    #now lets filter for each State and Sub-Category
    for state in stateFilter:
        for subC in subCategory:
            pdf_req_option = TSC.PDFRequestOptions(page_type=TSC.PDFRequestOptions.PageType.A4, orientation=TSC.PDFRequestOptions.Orientation.Landscape)
            pdf_req_option.vf('State', state)
            pdf_req_option.vf('Sub-Category', subC) # name of the filter (Sub-Category) is the same as in Tableau workbook 
            print("Printing PDF -->", "view_pdf - " + state + " and subCat " + subC + " -.pdf")

            for view in TSC.Pager(server.views):
                if view.id == '88aa3d1f-f294-4af4-be1a-bc70b0242526':
                    server.views.populate_pdf(view, pdf_req_option)
                    with open('./view_pdf - ' + state + ' - ' + subC + ' -.pdf', 'wb') as f:
                        f.write(view.pdf)
    


    





