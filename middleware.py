import pickle 


#function to access ml model and predict package based on user input
def package_predictor(user_input):
    with open('deployment_model.pkl','rb') as file:
        model=pickle.load(file)
    
    predicted_package=model.predict([user_input])
    return predicted_package
