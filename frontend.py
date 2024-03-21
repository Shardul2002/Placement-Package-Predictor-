import streamlit as st
from middleware import package_predictor 
st.set_page_config(page_title="Placement Package Predictor")


#Project title
st.title("Placement Package Predictor",anchor="Placement Package Predictor")

#User input details
st.write('<span style="font-size:24px">Academic Details:</span>',unsafe_allow_html=True)
variable_names=['btech_cgpa','hsc_score','ssc_score','gap_years','industry_internship_count','english_speaking','aptitude_skill','time_management','public_speaking','group_discussion','presentation_skills','industry_performance','skill_ability','productivity','job_priority','work_environment']
attributes=['BTech Score','HSC Score','SSC Score','Gap Years','Industry Project or Internship Count','English Fluency','Aptitude Skills','Time Management Skills','Public Speaking Skills','Group Discussion Skills','Presentation Skills','Industry Performance','New Skills Acquiring Ability','Productivity','Job Priority','Work Environment Priority',]
j=0
for i in range(8):
    col1,col2=st.columns(2)
    with col1:
        if j==0 or j==2:
            variable_names[j]=st.number_input(attributes[j],min_value=0.0,key=variable_names[j])
            
        else:
            variable_names[j]=st.number_input(attributes[j],min_value=0,key=variable_names[j])
        j=j+1
    with col2:
        if j==1:
            variable_names[j]=st.number_input(attributes[j],min_value=0.0,key=variable_names[j])
        else:
            variable_names[j]=st.number_input(attributes[j],min_value=0,key=variable_names[j])
        j=j+1
    if i==1:
        st.write("")
        st.write('<span style="font-size:24px">Personal Assesments:  </span>(Please rate yourself between 0-5)',unsafe_allow_html=True)
        st.write("")

st.write("")    
submit=st.button('Submit')

#Result Display
index_to_exclude=3
if submit and (any((i!=3 and (user_input_value==0 or user_input_value==0.00)) for i,user_input_value in enumerate(variable_names))):
    st.error("Please fill all the input fields!!")
else:
    if submit:
        user_input=[]
        for i in range(16):
         user_input.append(variable_names[i])
        package_range=package_predictor(user_input)
        lower_package_limit=round(package_range[0]-1,2)
        upper_package_limit=round(package_range[0]+1,2)
        st.write("")
        st.write(f'<span style="font-size:18px;border: 2px solid #000000; padding: 10px; border-radius: 5px;"><b>Predicted Package Range:</b> {lower_package_limit} LPA - {upper_package_limit} LPA</span>',unsafe_allow_html=True)

     

