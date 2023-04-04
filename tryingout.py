from bs4 import BeautifulSoup
import requests

#function to fetch the location and information about departments
def parole():
    url = "https://www.pvamu.edu/hb2504"
    headers={
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    result = requests.get(url,headers=headers).text
    doc = BeautifulSoup(result,"html.parser")

    table = doc.find('table')

    print (doc.find_all("option"))
    
    # #extract the table headers
    # header = []
    # for th in table.find_all('th'):
    #     header.append(th.text)

    # # print (header)
    # #extract the rows
    # rows = []
    # for tr in table.find_all('tr'):
    #     cells=[]
    #     for td in tr.find_all('td'):
    #         cells.append(td.text)
    #     if cells:
    #         rows.append(cells)
    # # create a dictionary for each row in the table
    # directory ={}
    # all_depts=[]
    # for row in rows:
    #     row_data = {}
    #     data = []
    #     for i, cell in enumerate(row):
    #         row_data[header[i]] = cell
    #     data.append(row_data)
    #     directory[list(row_data.values())[0]]= data
        
    #     #add all department in a list.
    #     all_depts.append(row_data['Department Name'])
    # return [directory,all_depts]
parole()