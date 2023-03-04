import writeToJson
import directory
import json

def updateIntentDept():
        dept_list = directory.get_all_dept_names()
        for dept in dept_list:
                response = directory.get_deptInfo_by_name(dept)
                new_data = {
                "tag": dept,
                "patterns": [
                        "How do I get to the department of "+ dept,
                        "where is the building of "+dept,
                        "have any idea where the location of "+dept+" is?",
                        "where do i find the "+dept+" building"
                ],
                "responses": [
                        response
                ],
                "context_set": ""
                }
                # data = json.loads(new_data)
                # data['responses'] = data['responses'].replace("\\n","\n")
                # new_data = json.dumps(data)
                print (new_data)
                writeToJson.write_json(new_data)
# updateIntentDept()