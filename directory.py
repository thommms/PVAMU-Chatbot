from bs4 import BeautifulSoup
import requests
import pdfplumber
import requests
import PyPDF2
import re

#function to fetch the location and information about departments
def get_full_dept_directory():
    url = "https://www.pvamu.edu/directory"
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

    # print (header)
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

#=======================================================================================================
#get all professors details and their classes

import re
def fetch_link(inp):
    soup = BeautifulSoup(inp,"html.parser")
    a_tag = soup.find('a')
    if a_tag:
        link = a_tag.get('href')
        return link
def fetch_text(inp):
    soup = BeautifulSoup(inp,"html.parser")
    text = soup.text
    return text

inp = '<a href="https://www.bkstr.com/webApp/discoverView?bookstore_id-1=215&amp;div-1=&amp;term_id-1=202320&amp;dept-1=BIOL&amp;course-1=2416§ion-1=P01" target="_blank"> Book </a>'

def get_all_professors():
    url = "https://www.pvamu.edu/hb2504"
    headers={
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    result = requests.get(url,headers=headers).text
    doc = BeautifulSoup(result,"html.parser")
    header =[]

    table = doc.find_all("table")[1]
    allPack = []

    for row in table.find_all('tr'):
        cells = row.find_all("td")
        pack = []
        for cell in cells:
            pack.append(str(cell).replace("\t","").replace("\n",""))
        allPack.append(pack)

    prof_dict = {}
    for i in range(1,len(allPack)):
        info =[]
        courseCode =allPack[i][0]
        course_link = fetch_link(courseCode)
        temp_link = str(course_link).replace(" ","%20")
        # print ("=======================>",
        link = "https://www.pvamu.edu"+temp_link
        courseName = fetch_text(allPack[i][1])
        instructor = fetch_text(allPack[i][2])
        book = fetch_link(allPack[i][3])

        info.append([fetch_text(courseCode),fetch_link(courseCode)])
        info.append(courseName)
        info.append(link)
        if instructor not in prof_dict:
            prof_dict[instructor] =[info]
        else:
            prof_dict[instructor].append(info)
    
    # print (prof_dict['Limin Zhu'])
    return prof_dict

def get_class_details(name):
    result = get_all_professors()
    instructor = name
    all_list = []
    courseCodes = ""
    courseNames = ""
    books =""
    course_details =""
    for i in range(len(result[name])):
        list_class = []
        courseCodes = result[name][i][0][0]
        # print ("+++++",result[name][i][0][0])
        courseNames = result[name][i][1]
        books = result[name][i][2]
        list_class.extend((courseCodes,courseNames,books))
        all_list.append(list_class)
        course_details+= courseCodes+": "+courseNames+" \nRecommended book:"+books +"\n\n"

    response= f"\nHere are the class details for {instructor} for the classes this semester:\n\n\
Instructor: {instructor}\n\
=============================\n\
{course_details}"
    
    # print (all_list)
    return [response,all_list]

def get_office_hours(key,url):
    # Download the PDF file from the URL
    response = requests.get(url)

    # Write the PDF data to a file
    with open("office_hour_files/{}.pdf".format(key), "wb") as file:
        file.write(response.content)
    line_with_next_line = search_pdf("Office Hours", "office_hour_files/{}.pdf".format(key))
    
    file.close()
    return line_with_next_line[0]+"\n"+line_with_next_line[1]

def search_pdf(keyword, filename):
    with pdfplumber.open(filename) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if keyword in line:
                return line, lines[i+1] if i+1 < len(lines) else ""
    return None, None


# url = "https://www.pvamu.edu/sites/hb2504/courses/Spring%202023/ACCT%202301-P03.pdf"
# url = "https://www.pvamu.edu/sites/hb2504/courses/Spring%202023/ACCT%202302-P02.pdf"
url = "https://www.pvamu.edu/sites/hb2504/courses/Spring%202023/BIOL%202402-P08.pdf"
# line_with_next_line = search_pdf("Office Hours", "temp.pdf")
# if line_with_next_line[0]:
#     print("Line containing keyword:", line_with_next_line[0])
#     print("Next line:", line_with_next_line[1])
# else:
#     print("Keyword not found in PDF file.")
# print (get_office_hours("halass sdfs",url))
    # response = get_all_professors
# print (get_all_dept_names())
# print (get_class_details("Limin Zhu"))
# print (get_class_details("Limin Zhu"))
# print (get_class_details("Bu-Ryung Lee")[0])

# get_all_professors()
# fetch_link(inp)

# get_full_dept_directory()


