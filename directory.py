from bs4 import BeautifulSoup
import requests

#function to fetch the location and information about departments
def get_full_dept_directory():
    url = "https://www.pvamu.edu/directory"
    # url = "https://coinmarketcap.com"
    headers={
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    result = requests.get(url,headers=headers).text
    doc = BeautifulSoup(result,"html.parser")

    table = doc.find('table')
    
    #extract the table headers
    header = []
    for th in table.find_all('th'):
        header.append(th.text)

    #extract the rows
    rows = []
    for tr in table.find_all('tr'):
        cells=[]
        for td in tr.find_all('td'):
            cells.append(td.text)
        if cells:
            rows.append(cells)
    # create a dictionary for each row in the table
    directory ={}
    all_depts=[]
    for row in rows:
        row_data = {}
        data = []
        for i, cell in enumerate(row):
            row_data[header[i]] = cell
        data.append(row_data)
        directory[list(row_data.values())[0]]= data
        
        #add all department in a list.
        all_depts.append(row_data['Department Name'])
    return [directory,all_depts]

# def get_all_dept():

#     return result

def get_deptInfo_by_name(department):
    result = get_full_dept_directory()
    department_name = result[0][department][0]['Department Name']
    main_number = result[0][department][0]["Main Number"]
    mail_stop = result[0][department][0]["Mail Stop"]
    location = result[0][department][0]["Location"]

    response = f"Here are the details of {department_name} as of today: \n\nDepartment Name : {department_name} \
        \nDepartment Phone Number: {main_number}\
        \nMail box: {mail_stop}\
        \nAddress/Office location: {location}"
    # return result[department][0]
    return response

# print (get_deptInfo_by_name('Academic Affairs'))

def get_all_dept_names():
    result = get_full_dept_directory()
    return result[1]

# print (get_all_dept_names())
