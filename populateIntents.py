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
                # print (new_data)
                writeToJson.write_json(new_data)
# updateIntentDept()

def updateIntentProf():
        prof_classes = directory.get_all_professors()
        for key,value in prof_classes.items():
                response = directory.get_class_details(key)
                # courseCodes[:len(courseCodes)-4]
                # courseCode = value[0][0][0][:len(value[0][0][0])-4]
                # print ("=============>",response[1])
                # courseName = value[0][1]
                # print ("++++++++++++++++++++",value[0][1])
                # print ("--------------->",len(response[1]))
                for i in range(len(response[1])):
                        courseCode = response[1][i][0][:-4]
                        courseName = response[1][i][1]
                        # print ("------------------->",courseCode)
                        new_data = {
                        "tag": key,
                        "patterns": [
                                "what classes is "+key+" taking this semester",
                                "who is the instructor for "+courseCode+"?",
                                "who is the instructor for "+courseName+"?",
                                "who is the professor taking "+courseCode+"?",
                                "what class is Dr. "+key+" taking this semester?",
                                "what books are recommended book for "+courseName+"?",
                                "what books are recommended book for "+courseCode+"?",
                                "who is teaching "+courseCode+"?",
                                "who is taking "+courseCode+"?",
                                "what class does "+key+" teaches",
                                "what classes does "+key+" teach",
                                "what classes is "+key+" teaching"
                        ],
                        "responses": [
                                response[0]
                        ],
                        "context_set": ""
                        }
                        # print (new_data)
                        writeToJson.write_json(new_data)
        # return response
        # print (new_data)
                # data = json.loads(new_data)
                # data['responses'] = data['responses'].replace("\\n","\n")
                # new_data = json.dumps(data)
                # print (new_data)
                # writeToJson.write_json(new_data)

def updateIntentOfficeHours():
        prof_classes = directory.get_all_professors()
        for key,value in prof_classes.items():
                response = directory.get_class_details(key)
                url = value[0][2]
                for i in range(len(response[1])):
                        courseName = response[1][i][1]
                        # print (value[0])
                        # response = directory.get_office_hours(key,url)
                        # print (response)
                        new_data = {
                        "tag": key[:10]+"_hours",
                        "patterns": [
                                "what time is the office hours for "+key+"?",
                                "when is the office hour for "+key+"?",
                                "office hour for "+key,
                                "what time is the office hours for Dr "+key+"?",
                                "when is the office hour for Dr "+key+"?",
                                "office hour for Dr"+key,
                                "Dr "+key+" office hours",
                                key+"'s office hours",
                                "what book is Dr "+key+" using",
                                "recommended textbook for "+courseName,
                                "recommended books for "+courseName,
                                "What are the recommended books for "+courseName

                        ],
                        "responses": [
                                "For more information about "+key+", Please visit "+url+" e.g office hours, books etc"
                        ],
                        "context_set": ""
                        }
                        print (new_data)
                        writeToJson.write_json(new_data)

# updateIntentDept()
updateIntentProf()
updateIntentOfficeHours()