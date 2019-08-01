import tableauserverclient as TSC


tableau_auth = TSC.TableauAuth('admin', 'admin', user_id_to_impersonate='223510e8-3bf5-4971-bf00-b2146092b957')
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
    stateFilter = ['Alabama', 'Arizona','Arkansas','California','Colorado','Iowa','Kansas','Texas']
    subCategory = ['Chairs', 'Art', 'Machines', 'Phones']

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
    


    





