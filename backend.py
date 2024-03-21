import pandas as pd
import random,pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,classification_report,mean_squared_error,r2_score,mean_absolute_error

#read data
data = pd.read_excel('final_dataset.xlsx', usecols=[
    'SCORE_BTECH', 
    'SCORE_SSC', 
    'SCORE_HSC', 
    'GAP_YEARS',
    'INDUSTRY_PROJECT_OR_INTERNSHIP_COUNT',
    'SELF_ASSESMENT_ENGLISH_SPOKEN',
    'SELF_ASSESMENT_APTITUDE_LOGIC',
    'SELF_ASSESMENT_TIME_MANAGEMENET',
    'SELF_ASSESMENT_PUBLIC_SPEAKING',
    'SELF_ASSESMENT_GROUP_DISCUSSION',
    'SELF_ASSESEMENT_PRESENTATIONS_SKILLS',
    'SELF_ASSESMENT_INDUSTRY_ASSESMENT',
    'SELF_ASSESMSENT_LEARNING_NEW_SKILL',
    'SELF_ASSMENT_PREPARATION_WORKING_LONG_HOURS',
    'PRIORITY_FOR_JOB_IN_CAREER',
    'PRIORITY_FOR_CONVINIENCE_AT_WORK',
    'PLACEMENT_CTC',
])


#data attributes for encoding
attr = [
    'SELF_ASSESMENT_ENGLISH_SPOKEN',
    'SELF_ASSESMENT_APTITUDE_LOGIC',
    'SELF_ASSESMENT_TIME_MANAGEMENET',
    'SELF_ASSESMENT_PUBLIC_SPEAKING',
    'SELF_ASSESMENT_GROUP_DISCUSSION',
    'SELF_ASSESEMENT_PRESENTATIONS_SKILLS',
    'SELF_ASSESMENT_INDUSTRY_ASSESMENT',
    'SELF_ASSESMSENT_LEARNING_NEW_SKILL',
    'SELF_ASSMENT_PREPARATION_WORKING_LONG_HOURS',
    'PRIORITY_FOR_JOB_IN_CAREER',
    'PRIORITY_FOR_CONVINIENCE_AT_WORK',
]

#data encodings
encodings = {
    'Very Poor': 0,
    'Poor': 1, 
    'Good': 2, 
    'Average': 3, 
    'Excelant': 4, 
    'Medium' : 3, 'Highest' : 5, 'High' : 4 , 'Job is not my priority' : 0, 'Lowest' : 1,
       'Low' : 2
}

for a in attr:
    data[a] = data[a].replace(encodings)



data['GAP_YEARS'] = data['GAP_YEARS'].replace(
{
    '3 Years - Due to Medical Emergency ': 3,
    'direct second year dipolma after 12th' : 0,
    'No Gap in College Academics or any Semester, 1 Year Gap after my 12th Class and before joining an undergraduate degree.' : 1,
    '1 year gap after 12 for preparation': 1,
    "no.. but I took admission in one engineering college in 2018 through MHT-CET, but I couldn't attend second semester due to my health issues at that time.. so I removed my admission from that college and took admission as fresh student through MTH-CET of 2019 in VIIT, Pune.. so from 2019 I'm a regular student of VIIT.." : 1
}
)


data['INDUSTRY_PROJECT_OR_INTERNSHIP_COUNT'] = data['INDUSTRY_PROJECT_OR_INTERNSHIP_COUNT'].replace(
    {
        'nan' : 0,
        '-' : 0,
        'no' : 0,
        '.' : 0,
        '3 months' : 3,
        'Aws eduskills internship in cloud computing' : 1,
        'Na' : 0, 'NO' : 0, 'One' : 1
    }
)


#filling null values of column
for index,value in data['INDUSTRY_PROJECT_OR_INTERNSHIP_COUNT'].items():
  if pd.isnull(value):
    if data.loc[index,'PLACEMENT_CTC']>10:
      data.loc[index,'INDUSTRY_PROJECT_OR_INTERNSHIP_COUNT']=3
    elif data.loc[index,'PLACEMENT_CTC']>8:
      data.loc[index,'INDUSTRY_PROJECT_OR_INTERNSHIP_COUNT']=2
    elif data.loc[index,'PLACEMENT_CTC']>5:
      data.loc[index,'INDUSTRY_PROJECT_OR_INTERNSHIP_COUNT']=1
    else:
      data.loc[index,'INDUSTRY_PROJECT_OR_INTERNSHIP_COUNT']=0


#data cleaning
data['SCORE_SSC'] = data['SCORE_SSC'].replace('%', '')
data['SCORE_SSC'] = data['SCORE_SSC'].replace('95 percent', '95.0')
data['SCORE_SSC'] = data['SCORE_SSC'].replace('9.2 CGPA ', '91.0')
data['SCORE_SSC'] = data['SCORE_SSC'].replace('79.54 %', '79.54')
data['SCORE_SSC'] = data['SCORE_SSC'].replace('90.60 %', '90.60')
data['SCORE_SSC'] = data['SCORE_SSC'].replace('96 %', '96.00')
data['SCORE_SSC'] = data['SCORE_SSC'].replace('93.4 %', '93.40')
data['SCORE_SSC'] = data['SCORE_SSC'].replace('10 CGPA', '97.00')
data['SCORE_SSC'] = data['SCORE_SSC'].replace('9.6cgpa', '92.00')
data['SCORE_SSC'] = data['SCORE_SSC'].replace('91.8 (10 CGPA)', '91.80')
data['SCORE_SSC'] = data['SCORE_SSC'].replace('7.0 CGPA', '70.00')
data['SCORE_SSC'] = data['SCORE_SSC'].replace('92.40 %', '92.40')

#filling null values for hsc_score column
mapping = data.set_index('SCORE_SSC')['SCORE_HSC'].to_dict()
data['SCORE_HSC'] = data.apply(lambda row: mapping.get(row['SCORE_SSC']) if pd.isnull(row['SCORE_HSC']) else row['SCORE_HSC'], axis=1)
data['SCORE_HSC'].isnull().sum()

for index,value in data['SCORE_HSC'].items():
  if pd.isnull(value):
    ssc=data.loc[index,'SCORE_SSC']
    data.loc[index,'SCORE_HSC']=float(ssc)-10

data['SCORE_HSC']=data['SCORE_HSC'].replace("79.54 %","79.54")
for index,value in data['SCORE_HSC'].items():
  if value=='. ' or value=='No' or value=='-' or value=='Na' or value=='.' or value=='na' or value=='N A':
    ssc=data.loc[index,'SCORE_SSC']
    data.loc[index,'SCORE_HSC']=float(ssc)-10


data['SCORE_HSC']=data['SCORE_HSC'].astype(float)
data['SCORE_SSC']=data['SCORE_SSC'].astype(float)

#filling null values for placement_ctc column
for index,value in data['PLACEMENT_CTC'].items():
  if pd.isnull(value):
    if data.loc[index,'SCORE_SSC']>95 and data.loc[index,'SCORE_HSC']>85 and data.loc[index,'SCORE_BTECH']>9.2:
      data.loc[index,'PLACEMENT_CTC']=random.randint(10,15)
    elif data.loc[index,'SCORE_SSC']>88 and data.loc[index,'SCORE_HSC']>70 and data.loc[index,'SCORE_BTECH']>8.0:
      data.loc[index,'PLACEMENT_CTC']=random.randint(6,9)
    elif data.loc[index,'SCORE_SSC']>70 and data.loc[index,'SCORE_HSC']>60 and data.loc[index,'SCORE_BTECH']>7.0:
      data.loc[index,'PLACEMENT_CTC']=random.randint(4,6)
    elif data.loc[index,'SCORE_SSC']>60 and data.loc[index,'SCORE_HSC']>50 and data.loc[index,'SCORE_BTECH']>5.0:
      data.loc[index,'PLACEMENT_CTC']=random.randint(3,4)

data = data[data['PLACEMENT_CTC'].notnull()]

#Making the dataset more balanced 
data_above_8=data[data['PLACEMENT_CTC']>8.0]
data_above_10=data[data['PLACEMENT_CTC']>10.0]
data=pd.concat([data,data_above_8,data_above_8,data_above_10,data_above_10,data_above_10])

#Model training and prediction
X=data[['SCORE_BTECH',
    'SCORE_SSC',
    'SCORE_HSC',
    'GAP_YEARS',
    'INDUSTRY_PROJECT_OR_INTERNSHIP_COUNT',
    'SELF_ASSESMENT_ENGLISH_SPOKEN',
    'SELF_ASSESMENT_APTITUDE_LOGIC',
    'SELF_ASSESMENT_TIME_MANAGEMENET',
    'SELF_ASSESMENT_PUBLIC_SPEAKING',
    'SELF_ASSESMENT_GROUP_DISCUSSION',
    'SELF_ASSESEMENT_PRESENTATIONS_SKILLS',
    'SELF_ASSESMENT_INDUSTRY_ASSESMENT',
    'SELF_ASSESMSENT_LEARNING_NEW_SKILL',
    'SELF_ASSMENT_PREPARATION_WORKING_LONG_HOURS',
    'PRIORITY_FOR_JOB_IN_CAREER',
    'PRIORITY_FOR_CONVINIENCE_AT_WORK']]
y=data['PLACEMENT_CTC']
print(data.iloc[:,:-1])
X_train,X_test,y_train,y_test=train_test_split(data.iloc[:,:-1], data.PLACEMENT_CTC, test_size=0.2, random_state=42)

svm=SVR()
svm.fit(X_train,y_train)
y_pred=svm.predict(X_test)

#Saving the model
with open('deployment_model.pkl', 'wb') as file:
    pickle.dump(svm, file)

