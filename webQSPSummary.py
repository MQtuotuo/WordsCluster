import json
from summary import * 

# find question id, answers, keyword, relations given by a question
def findElements(question):
    answers =[]
    relations = []
    for item in questions:
        if item["RawQuestion"] == question:
            parses = item["Parses"]   
            question_id = item['QuestionId']
            for j in range(0, len(parses)):
                # keywords extraction
                keyword = parses[j]["TopicEntityName"]
                # answers extraction
                answers_set = parses[j]["Answers"]
                #answers.append(answers_set)
                
                for k in range(0, len(answers_set)):
                    answer = answers_set[k]['EntityName']
                    answers.append(answer)
                
                # relations extraction
                relations_set = parses[j]["InferentialChain"]
                relations.append(relations_set)
                break          
    return question_id, answers, keyword, relations


# write to JSON file
def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp, indent = 4, ensure_ascii = False)



# get all questions
WebQSP = json.load(open('data/WebQSP.train.json'))
numberOfQuestions = len(WebQSP["Questions"])
questions = WebQSP["Questions"]
rawQuestions = []
for i in range(0, numberOfQuestions):
    rawQuestion = questions[i]["RawQuestion"]
    rawQuestions.append(rawQuestion)


# write into a json file with summary
data = {}
data['Questions'] = []  
for i in range(0, len(rawQuestions)):
    question_id, answers, keyword, relations = findElements(rawQuestions[i])
    if relations[0]==None:
        relation=None
    else:
        relation = relations[0][-1].rsplit('.')[-1]
    data['Questions'].append({  
    'QuestionId': question_id,
    'RawQuestion': rawQuestion,
    'TopEntityName': keyword, 
    'Relation':relation,
    'InferentialChain': relations[0]
    #'Answers': answers[0]
    })

    data['Questions'][i]["Answers"]=[]
    for answer in answers: 
        print(answer)
        if answer==None:
            summary=None
        else:
            summary=getSummary(answer, keyword, relation)
        
        #print(summary)
        data['Questions'][i]["Answers"].append({
            "EntityName": answer,
            "EntitySummary":summary
        })

writeToJSONFile('./data','WebQSPSummary',data)









