# # Import all the necessary libraries
# import matplotlib
# matplotlib.use('Agg')  # Set the backend to 'Agg' to avoid GUI requirements
# import matplotlib.pyplot as plt
# # import seaborn as sns
# # import numpy as np
# import numpy as np
# from numpy.core.numeric import NaN
# import pandas as pd
# import seaborn as sns
# # import matplotlib.pyplot as plt
# # import module .venv
# import json
# import re
# import time
# import cv2
# import spacy
# from sklearn.linear_model import LogisticRegression
# from sklearn.preprocessing import LabelEncoder
# from flask import Flask , render_template , request , url_for , jsonify , Response
# from werkzeug.utils import redirect, secure_filename
# from flask_mail import Mail , Message
# from flask_mysqldb import MySQL
# from pyresparser import ResumeParser
# from fer import Video
# from fer import FER
# from video_analysis import extract_text , analyze_sentiment
# from decouple import config
# nlp = spacy.load('en_core_web_sm')
# # spacy.load('en_core_web_sm')

# # Access the environment variables stored in .env file
# MYSQL_USER = config('mysql_user')
# MYSQL_PASSWORD = config('mysql_password')

# # To send mail (By interviewee)
# MAIL_USERNAME = config('mail_username')
# MAIL_PWD = config('mail_pwd')

# # For logging into the interview portal
# COMPANY_MAIL = config('company_mail')
# COMPANY_PSWD = config('company_pswd')

# # Create a Flask app
# app = Flask(__name__)

# # App configurations
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = MYSQL_USER
# app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
# app.config['MYSQL_DB'] = 'smarthire' 
# user_db = MySQL(app)

# mail = Mail(app)              
# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = MAIL_USERNAME
# app.config['MAIL_PASSWORD'] = MAIL_PWD
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_ASCII_ATTACHMENTS'] = True
# mail = Mail(app)


# # Initial sliding page
# @app.route('/')
# def home():
#     return render_template('index.html')


# # Interviewee signup 
# @app.route('/signup' , methods=['POST' , 'GET'])
# def interviewee():
#     if request.method == 'POST' and 'username' in request.form and 'usermail' in request.form and 'userpassword' in request.form:
#         username = request.form['username']
#         usermail = request.form['usermail']
#         userpassword = request.form['userpassword']

#         cursor = user_db.connection.cursor()

#         cursor.execute("SELECT * FROM candidates WHERE candidatename = % s AND email = %s", (username, usermail))
#         account = cursor.fetchone()
        
#         if account:
#             err = "Account Already Exists"
#             return render_template('index.html' , err = err)
#         elif not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', usermail):
#             err = "Invalid Email Address !!"
#             return render_template('index.html' , err = err)
#         elif not re.fullmatch(r'[A-Za-z0-9\s]+', username):
#             err = "Username must contain only characters and numbers !!"
#             return render_template('index.html' , err = err)
#         elif not username or not userpassword or not usermail:
#             err = "Please fill out all the fields"
#             return render_template('index.html' , err = err)
#         else:
#             cursor.execute("INSERT INTO candidates VALUES (NULL, % s, % s, % s)" , (username, usermail, userpassword,))
#             user_db.connection.commit()
#             reg = "You have successfully registered !!"
#             return render_template('FirstPage.html' , reg = reg)
#     else:
#         return render_template('index.html')


# # Interviewer signin 
# @app.route('/signin' , methods=['POST' , 'GET'])
# def interviewer():
#     if request.method == 'POST' and 'company_mail' in request.form and 'password' in request.form:
#         company_mail = request.form['company_mail']
#         password = request.form['password']

#         if company_mail == COMPANY_MAIL and password == COMPANY_PSWD:
#             return render_template('candidateSelect.html')
#         else:
#             return render_template("index.html" , err = "Incorrect Credentials")
#     else:
#         return render_template("index.html")

# # personality trait prediction using Logistic Regression and parsing resume
# @app.route('/prediction' , methods = ['GET' , 'POST'])
# def predict():
#     # get form data
#     if request.method == 'POST':
#         fname = request.form['firstname'].capitalize()
#         lname = request.form['lastname'].capitalize()
#         age = int(request.form['age'])
#         gender = request.form['gender']
#         email = request.form['email']
#         file = request.files['resume']
#         path = './static/{}'.format(file.filename)
#         file.save(path)
#         # Check if the form inputs are not empty before converting to float
#         if 'openness' in request.form and request.form['openness'].strip():  # Check if 'openness' is not empty
#             val1 = float(request.form['openness'])
#         else:
#             # Handle the case where 'openness' is not provided or empty
#             # For example, you can assign a default value or return an error message.
#             val1 = 0.0  # Assigning a default value of 0.0

#         # Repeat the above steps for other form inputs
#         if 'neuroticism' in request.form and request.form['neuroticism'].strip():  # Check if 'neuroticism' is not empty
#             val2 = float(request.form['neuroticism'])
#         else:
#             val2 = 0.0  # Assigning a default value of 0.0

#         if 'conscientiousness' in request.form and request.form['conscientiousness'].strip():  # Check if 'conscientiousness' is not empty
#             val3 = float(request.form['conscientiousness'])
#         else:
#             val3 = 0.0  # Assigning a default value of 0.0

#         if 'agreeableness' in request.form and request.form['agreeableness'].strip():  # Check if 'agreeableness' is not empty
#             val4 = float(request.form['agreeableness'])
#         else:
#             val4 = 0.0  # Assigning a default value of 0.0

#         if 'extraversion' in request.form and request.form['extraversion'].strip():  # Check if 'extraversion' is not empty
#             val5 = float(request.form['extraversion'])
#         else:
#             val5 = 0.0  # Assigning a default value of 0.0

#         # val1 = float(request.form['openness'])
#         # val2 = float(request.form['neuroticism'])
#         # val3 = float(request.form['conscientiousness'])
#         # val4 = float(request.form['agreeableness'])
#         # val5 = float(request.form['extraversion'])

#         # val1 = request.form['openness']
#         # val2 = request.form['neuroticism']
#         # val3 = request.form['conscientiousness']
#         # val4 = request.form['agreeableness']
#         # val5 = request.form['extraversion']
        
#         # model prediction
#         df = pd.read_csv(r'static\trainDataset.csv')
#         le = LabelEncoder()
#         df['Gender'] = le.fit_transform(df['Gender'])
#         x_train = df.iloc[:, :-1].to_numpy()
#         y_train = df.iloc[:, -1].to_numpy(dtype = str)
#         lreg = LogisticRegression(multi_class='multinomial', solver='newton-cg',max_iter =1000)
#         lreg.fit(x_train, y_train)
#         if gender == 'male':
#             gender = 1
#         elif gender == 'female': 
#             gender = 0
#         input =  [gender, age, val1, val2, val3, val4, val5]
#         # print("Gender after conversion:", gender)

#         # if gender == 'male':
#         #     gender = 1
#         # elif gender == 'female': 
#         #     gender = 0
#         # input =  [gender, age, val1, val2, val3, val4, val5]

#         pred = str(lreg.predict([input])[0]).capitalize()

#         # get data from the resume
#         data = ResumeParser(path).get_extracted_data()
#         result = {'Name': fname + ' ' + lname, 'Age': age, 'Email': email, 'Mobile Number': data.get('mobile_number', None),
#           'Skills': str(data['skills']).replace("[", "").replace("]", "").replace("'", "") if data else None,
#           'Degree': data.get('degree', [None])[0] if data else None,
#           'Designation': data.get('designation', [None])[0] if data and data.get('designation') else None,
#         #   'Designation': data.get('designation', [None])[0] if data else None,
#           'Total Experience': data.get('total_experience', None),
#           'Predicted Personality': pred}

#         # result = {'Name':fname+' '+lname , 'Age':age , 'Email':email , 'Mobile Number':data.get('mobile_number', None) , 
#         # 'Skills':str(data['skills']).replace("[" , "").replace("]" , "").replace("'" , "") , 'Degree':data.get('degree' , None)[0] , 'Designation':data.get('designation', None)[0] ,
#         # 'Total Experience':data.get('total_experience') , 'Predicted Personality':pred}

#         with open('./static/result.json' , 'w') as file:
#             json.dump(result , file)

#     return render_template('questionPage.html')

# # # Record candidate's interview for face emotion and tone analysis
# # @app.route('/analysis', methods=['POST'])
# # def video_analysis():
# #     # get videos using media recorder js and save
# #     quest1 = request.files['question1']
# #     quest2 = request.files['question2']
# #     quest3 = request.files['question3']
# #     path1 = "./static/{}.{}".format("question1", "webm")
# #     path2 = "./static/{}.{}".format("question2", "webm")
# #     path3 = "./static/{}.{}".format("question3", "webm")
# #     quest1.save(path1)
# #     quest2.save(path2)
# #     quest3.save(path3)

# #     # speech to text response for each question - Google Cloud Speech-to-Text
# #     responses = {'Question 1: Tell something about yourself': [], 'Question 2: Why should we hire you?': [],
# #                  'Question 3: Where Do You See Yourself Five Years From Now?': []}
# #     ques = list(responses.keys())

# #     text1, _ = extract_text("question1.webm")
# #     time.sleep(15)
# #     responses[ques[0]].append(text1)

# #     text2, _ = extract_text("question2.webm")
# #     time.sleep(15)
# #     responses[ques[1]].append(text2)

# #     text3, _ = extract_text("question3.webm")
# #     time.sleep(15)
# #     responses[ques[2]].append(text3)

# #     # sentiment analysis for each textual answer - Google Cloud Natural Language API
# #     res1 = analyze_sentiment(text1)
# #     tones_doc1 = [('Sentiment', round(res1['score'], 2))]

# #     res2 = analyze_sentiment(text2)
# #     tones_doc2 = [('Sentiment', round(res2['score'], 2))]

# #     res3 = analyze_sentiment(text3)
# #     tones_doc3 = [('Sentiment', round(res3['score'], 2))]

# #     # plot sentiment analysis
# #     document_sentiments = [res1['score'], res2['score'], res3['score']]
# #     fig = plt.figure(figsize=(12, 6))
# #     sns.set_style("whitegrid")
# #     plt.bar(np.arange(len(document_sentiments)), document_sentiments, color='blue')
# #     plt.xticks(np.arange(len(document_sentiments)), ['Question 1', 'Question 2', 'Question 3'], fontsize=15,
# #                fontweight=60)
# #     plt.yticks(fontsize=12, fontweight=90)
# #     plt.xlabel('Questions', fontsize=15, fontweight=60)
# #     plt.ylabel('Sentiment Score', fontsize=15, fontweight=60)
# #     plt.title('Sentiment Analysis', fontsize=15, fontweight=60)
# #     plt.savefig('./static/sentiment_analysis.jpg', bbox_inches='tight')

# #     # save all responses
# #     with open('./static/answers.json', 'w') as file:
# #         json.dump(responses, file)

# #     # face emotion recognition - plotting the emotions against time in the video
# #     videos = ["question1.webm", "question2.webm", "question3.webm"]
# #     frame_per_sec = 100
# #     size = (1280, 720)

# #     video = cv2.VideoWriter(f"./static/combined.webm", cv2.VideoWriter_fourcc(*"VP90"), int(frame_per_sec), size)

# #     # Write all the frames sequentially to the new video
# #     for v in videos:
# #         curr_v = cv2.VideoCapture(f'./static/{v}')
# #         while curr_v.isOpened():
# #             r, frame = curr_v.read()
# #             if not r:
# #                 break
# #             video.write(frame)
# #     video.release()

# #     face_detector = FER(mtcnn=True)
# #     input_video = Video(r"./static/combined.webm")
# #     processing_data = input_video.analyze(face_detector, display=False, save_frames=False, save_video=False,
# #                                           annotate_frames=False, zip_images=False)
# #     vid_df = input_video.to_pandas(processing_data)
# #     vid_df = input_video.get_first_face(vid_df)
# #     vid_df = input_video.get_emotions(vid_df)
# #     pltfig = vid_df.plot(figsize=(12, 6), fontsize=12).get_figure()
# #     plt.legend(fontsize='large', loc=1)
# #     pltfig.savefig(f'./static/fer_output.png')

# #     return "success"
# # import numpy as np
# # import pandas as pd
# # import json
# # import os
# # import random
# # import time
# # import boto3
# # from google.cloud import language_v1
# # import cv2
# # import matplotlib.pyplot as plt
# # import seaborn as sns
# # from fer import FER
# # from fer import Video
# # from flask import Flask, render_template, request
# # from flask_mail import Mail, Message
# # from decouple import config

# # app = Flask(__name__)
# # mail = Mail(app)

# # Record candidate's interview for face emotion and tone analysis
# @app.route('/analysis', methods=['POST'])
# def video_analysis():
#     # get video using media recorder js and save
#     interview_video = request.files["interview_video"]
#     path = "./static/{}.{}".format("interview_video", "webm")
#     interview_video.save(path)

#     # speech to text response for the combined question
#     responses = {'How would you handle a situation where two project teams, one girls and one boys, are in conflict over language use, and also manage the project if a team member becomes severely ill and hospitalized near the deadline?': []}
#     ques = list(responses.keys())

#     text, _ = extract_text("interview_video.webm")
#     time.sleep(15)
#     responses[ques[0]].append(text)

#     # Sentiment analysis for the textual answer
#     res = analyze_sentiment(text)
#     sentiment = 'Positive' if res['magnitude'] > 0 else 'Negative' if res['magnitude'] < 0 else 'Neutral'

#     # Plot sentiment analysis
#     fig = plt.figure(figsize=(6, 4))
#     sns.set_style("whitegrid")
#     colors = 'green' if sentiment == 'Positive' else 'red' if sentiment == 'Negative' else 'gray'
#     plt.bar(ques[0], 1 if sentiment == 'Positive' else -1 if sentiment == 'Negative' else 0, color=colors)
#     plt.yticks(np.arange(-1, 2), ['Negative', 'Neutral', 'Positive'], fontsize=12, fontweight=90)
#     plt.xlabel('Question', fontsize=15, fontweight=60)
#     plt.ylabel('Sentiment', fontsize=15, fontweight=60)
#     plt.title('Sentiment Analysis', fontsize=15, fontweight=60)
#     plt.savefig('./static/sentiment_analysis.jpg', bbox_inches='tight')
#     plt.close(fig)  # Close the figure to release memory

#     # Save response and sentiment analysis
#     with open('./static/answers.json', 'w') as file:
#         json.dump(responses, file)
#     with open('./static/sentiment.json', 'w') as file:
#         json.dump({"sentiment": sentiment}, file)

# #     return "Video analysis and sentiment analysis completed."

# # if __name__ == "__main__":
# #     app.run(debug=True)

# # @app.route('/analysis', methods=['POST'])
# # def video_analysis():
# #     # get videos using media recorder js and save
# #     quest1 = request.files["question1"]
# #     quest2 = request.files["question2"]
# #     quest3 = request.files["question3"]
# #     path1 = "./static/{}.{}".format("question1", "webm")
# #     path2 = "./static/{}.{}".format("question2", "webm")
# #     path3 = "./static/{}.{}".format("question3", "webm")
# #     quest1.save(path1)
# #     quest2.save(path2)
# #     quest3.save(path3)

# #     # speech to text response for each question - AWS
# #     responses = {'Question 1: Tell something about yourself': [], 'Question 2: Why should we hire you?': [],
# #                  'Question 3: Where Do You See Yourself Five Years From Now?': []}
# #     ques = list(responses.keys())

# #     text1, data1 = extract_text("question1.webm")
# #     time.sleep(15)
# #     responses[ques[0]].append(text1)

# #     text2, data2 = extract_text("question2.webm")
# #     time.sleep(15)
# #     responses[ques[1]].append(text2)

# #     text3, data3 = extract_text("question3.webm")
# #     time.sleep(15)
# #     responses[ques[2]].append(text3)
# # #NEW SENTIMENT
# #     # Sentiment analysis for each textual answer - Google Cloud Natural Language API
# #     res1 = analyze_sentiment(text1)
# #     tones_doc1 = [('Sentiment', 'Positive' if res1['magnitude'] > 0 else 'Negative' if res1['magnitude'] < 0 else 'Neutral')]

# #     res2 = analyze_sentiment(text2)
# #     tones_doc2 = [('Sentiment', 'Positive' if res2['magnitude'] > 0 else 'Negative' if res2['magnitude'] < 0 else 'Neutral')]

# #     res3 = analyze_sentiment(text3)
# #     tones_doc3 = [('Sentiment', 'Positive' if res3['magnitude'] > 0 else 'Negative' if res3['magnitude'] < 0 else 'Neutral')]

# #     # Plot sentiment analysis
# #     document_sentiments = [tones_doc1[0][1], tones_doc2[0][1], tones_doc3[0][1]]
# #     fig = plt.figure(figsize=(12, 6))
# #     sns.set_style("whitegrid")
# #     colors = ['green' if sentiment == 'Positive' else 'red' if sentiment == 'Negative' else 'gray' for sentiment in document_sentiments]
# #     bars = plt.bar(np.arange(len(document_sentiments)), [1 if sentiment == 'Positive' else -1 if sentiment == 'Negative' else 0 for sentiment in document_sentiments], color=colors)
# #     plt.xticks(np.arange(len(document_sentiments)), ['Question 1', 'Question 2', 'Question 3'], fontsize=15, fontweight=60)
# #     plt.yticks(np.arange(-1, 2), ['Negative', 'Neutral', 'Positive'], fontsize=12, fontweight=90)  # Explicitly set ticks and labels
# #     plt.xlabel('Questions', fontsize=15, fontweight=60)
# #     plt.ylabel('Sentiment', fontsize=15, fontweight=60)
# #     plt.title('Sentiment Analysis', fontsize=15, fontweight=60)
# #     # Make sure neutral line is clearly visible
# #     for bar in bars:
# #         if bar.get_height() == 0:  # Neutral sentiment
# #             bar.set_linewidth(2)  # Increase line width for neutral sentiment
# #     # Add legend with explicit labels
# #     legend_labels = {'Positive': 'Positive', 'Negative': 'Negative', 'Neutral': 'Neutral'}
# #     legend_handles = [plt.Rectangle((0,0),1,1, color=color, ec="k", label=legend_labels[sentiment]) for sentiment, color in zip(['Positive', 'Negative', 'Neutral'], ['green', 'red', 'gray'])]
# #     plt.legend(handles=legend_handles, loc='upper right', fontsize=12)
# #     plt.savefig('./static/sentiment_analysis.jpg', bbox_inches='tight')
# #     plt.close(fig)  # Close the figure to release memory

# #     # Save all responses
# #     with open('./static/answers.json', 'w') as file:
# #         json.dump(responses, file)

# # #OLD SENTIMENT
# #     # # sentiment analysis for each textual answer - Google Cloud Natural Language API
# #     # res1 = analyze_sentiment(text1)
# #     # tones_doc1 = [('Sentiment', round(res1['score'], 2))]

# #     # res2 = analyze_sentiment(text2)
# #     # tones_doc2 = [('Sentiment', round(res2['score'], 2))]

# #     # res3 = analyze_sentiment(text3)
# #     # tones_doc3 = [('Sentiment', round(res3['score'], 2))]

# #     # # plot sentiment analysis
# #     # document_sentiments = [res1['score'], res2['score'], res3['score']]
# #     # fig = plt.figure(figsize=(12, 6))
# #     # sns.set_style("whitegrid")
# #     # plt.bar(np.arange(len(document_sentiments)), document_sentiments, color='blue')
# #     # plt.xticks(np.arange(len(document_sentiments)), ['Question 1', 'Question 2', 'Question 3'], fontsize=15, fontweight=60)
# #     # plt.yticks(fontsize=12, fontweight=90)
# #     # plt.xlabel('Questions', fontsize=15, fontweight=60)
# #     # plt.ylabel('Sentiment Score', fontsize=15, fontweight=60)
# #     # plt.title('Sentiment Analysis', fontsize=15, fontweight=60)
# #     # plt.savefig('./static/sentiment_analysis.jpg', bbox_inches='tight')
# #     # plt.close(fig)  # Close the figure to release memory
    
# #     # # save all responses
# #     # with open('./static/answers.json', 'w') as file:
# #     #     json.dump(responses, file)
# # #TILL HERE
# #     # face emotion recognition - plotting the emotions against time in the video
# #     videos = ["question1.webm", "question2.webm", "question3.webm"]
# #     frame_per_sec = 23
# #     size = (1280, 720)

# #     video = cv2.VideoWriter(f"./static/combined.webm", cv2.VideoWriter_fourcc(*"VP90"), int(frame_per_sec), size)

# #     # Write all the frames sequentially to the new video
# #     for v in videos:
# #         curr_v = cv2.VideoCapture(f'./static/{v}')
# #         while curr_v.isOpened():
# #             r, frame = curr_v.read()
# #             if not r:
# #                 break
# #             video.write(frame)
# #     video.release()

# #     face_detector = FER(mtcnn=True)
# #     input_video = Video(r"./static/combined.webm")
# #     processing_data = input_video.analyze(face_detector, display=False, save_frames=False, save_video=False,
# #                                           annotate_frames=False, zip_images=False)
# #     vid_df = input_video.to_pandas(processing_data)
# #     vid_df = input_video.get_first_face(vid_df)
# #     vid_df = input_video.get_emotions(vid_df)
# #     pltfig = vid_df.plot(figsize=(12, 6), fontsize=12).get_figure()
# #     plt.legend(fontsize='large', loc=1)
# #     pltfig.savefig(f'./static/fer_output.png')

#     # return "success"

# # Interview completed response message
# @app.route('/recorded')
# def response():
#     return render_template('recorded.html')


# # Display results to interviewee
# @app.route('/info')
# def info():
#     with open('./static/result.json', 'r') as file:
#         output = json.load(file)

#     with open('./static/answers.json', 'r') as file:
#         answers = json.load(file)

#     return render_template('result.html', output=output, responses=answers)


# # Send job confirmation mail to selected candidate
# @app.route('/accept', methods=['GET'])
# def accept():
#     with open('./static/result.json', 'r') as file:
#         output = json.load(file)

#     name = output['Name']
#     email = output['Email']
#     position = "Software Development Engineer"

#     msg = Message(f'Job Confirmation Letter', sender=MAIL_USERNAME, recipients=[email])
#     msg.body = f"Dear {name},\n\n" + f"Thank you for taking the time to interview for the {position} position. We enjoyed getting to know you. We have completed all of our interviews.\n\n" + f"I am pleased to inform you that we would like to offer you the {position} position. We believe your past experience and strong technical skills will be an asset to our organization. Your starting salary will be $15,000 per year with an anticipated start date of July 1.\n\n" + f"The next step in the process is to set up meetings with our CEO, Steve Carell\n\n." + f"Please respond to this email by June 23 to let us know if you would like to accept the SDE position.\n\n" + f"I look forward to hearing from you.\n\n" + f"Sincerely,\n\n" + f"Ashnuta Upadhyaya\nHuman Resources Director\nPhone: 9087654567\nEmail: feedbackmonitor123@gmail.com"
#     mail.send(msg)

#     return "success"

# # Send mail to rejected candidate
# @app.route('/reject', methods=['GET'])
# def reject():
#     with open('./static/result.json', 'r') as file:
#         output = json.load(file)

#     name = output['Name']
#     email = output['Email']
#     position = "Software Development Engineer"

#     msg = Message(f'Your application to Smart Hire', sender=MAIL_USERNAME, recipients=[email])
#     msg.body = f"Dear {name},\n\n" + f"Thank you for taking the time to consider Smart Hire. We wanted to let you know that we have chosen to move forward with a different candidate for the {position} position.\n\n" + f"Our team was impressed by your skills and accomplishments. We think you could be a good fit for other future openings and will reach out again if we find a good match.\n\n" + f"We wish you all the best in your job search and future professional endeavors.\n\n" + f"Regards,\n\n" + f"Ashnuta Upadhyaya\nHuman Resources Director\nPhone: 9087654567\nEmail: feedbackmonitor123@gmail.com"
#     mail.send(msg)

#     return "success"


# if __name__ == '__main__':
#     app.debug = True
#     app.run()


# # # Record candidate's interview for face emotion and tone analysis
# # @app.route('/analysis', methods = ['POST'])
# # def video_analysis():

# #     # get videos using media recorder js and save
# #     quest1 = request.files['question1']
# #     quest2 = request.files['question2']
# #     quest3 = request.files['question3']
# #     path1 = "./static/{}.{}".format("question1","webm")
# #     path2 = "./static/{}.{}".format("question2","webm")
# #     path3 = "./static/{}.{}".format("question3","webm")
# #     quest1.save(path1)
# #     quest2.save(path2)
# #     quest3.save(path3)

# #     # speech to text response for each question - AWS
# #     responses = {'Question 1: Tell something about yourself': [] , 'Question 2: Why should we hire you?': [] , 'Question 3: Where Do You See Yourself Five Years From Now?': []}
# #     ques = list(responses.keys())

# #     text1 , data1 = extract_text("question1.webm")
# #     time.sleep(15)
# #     responses[ques[0]].append(text1)

# #     text2 , data2 = extract_text("question2.webm")
# #     time.sleep(15)
# #     responses[ques[1]].append(text2)

# #     text3 , data3 = extract_text("question3.webm")
# #     time.sleep(15)
# #     responses[ques[2]].append(text3)

# #     # tone analysis for each textual answer - IBM
# #     res1 = analyze_sentiment(text1)
# #     tones_doc1 = []
    
# #     for tone in res1['document_tone']['tones']:
# #         tones_doc1.append((tone['tone_name'] , round(tone['score']*100, 2)))
    
# #     if 'Tentative' not in [key for key, val in tones_doc1]:
# #         tones_doc1.append(('Tentative', 0.0))
# #     if 'Analytical' not in [key for key, val in tones_doc1]:
# #         tones_doc1.append(('Analytical', 0.0))
# #     if 'Fear' not in [key for key, val in tones_doc1]:
# #         tones_doc1.append(('Fear', 0.0))
# #     if 'Confident' not in [key for key, val in tones_doc1]:
# #         tones_doc1.append(('Confident', 0.0))
# #     if 'Joy' not in [key for key, val in tones_doc1]:
# #         tones_doc1.append(('Joy', 0.0))
        
# #     tones_doc1 = sorted(tones_doc1)

# #     res2 = analyze_sentiment(text2)
# #     tones_doc2 = []

# #     for tone in res2['document_tone']['tones']:
# #         tones_doc2.append((tone['tone_name'] , round(tone['score']*100, 2)))
        
# #     if 'Tentative' not in [key for key, val in tones_doc2]:
# #         tones_doc2.append(('Tentative', 0.0))
# #     if 'Analytical' not in [key for key, val in tones_doc2]:
# #         tones_doc2.append(('Analytical', 0.0))
# #     if 'Fear' not in [key for key, val in tones_doc2]:
# #         tones_doc2.append(('Fear', 0.0))
# #     if 'Confident' not in [key for key, val in tones_doc2]:
# #         tones_doc2.append(('Confident', 0.0))
# #     if 'Joy' not in [key for key, val in tones_doc2]:
# #         tones_doc2.append(('Joy', 0.0))
        
# #     tones_doc2 = sorted(tones_doc2)

# #     res3 = analyze_sentiment(text3)
# #     tones_doc3 = []

# #     for tone in res3['document_tone']['tones']:
# #         tones_doc3.append((tone['tone_name'] , round(tone['score']*100, 2)))
        
# #     if 'Tentative' not in [key for key, val in tones_doc3]:
# #         tones_doc3.append(('Tentative', 0.0))
# #     if 'Analytical' not in [key for key, val in tones_doc3]:
# #         tones_doc3.append(('Analytical', 0.0))
# #     if 'Fear' not in [key for key, val in tones_doc3]:
# #         tones_doc3.append(('Fear', 0.0))
# #     if 'Confident' not in [key for key, val in tones_doc3]:
# #         tones_doc3.append(('Confident', 0.0))
# #     if 'Joy' not in [key for key, val in tones_doc3]:
# #         tones_doc3.append(('Joy', 0.0))
        
# #     tones_doc3 = sorted(tones_doc3)

# #     # plot tone analysis 
# #     document_tones = tones_doc1 + tones_doc2 + tones_doc3

# #     analytical_tone = []
# #     tentative_tone = []
# #     fear_tone = []
# #     joy_tone = []
# #     confident_tone = []

# #     for sentiment, score in document_tones:
# #         if sentiment == "Analytical":
# #             analytical_tone.append(score)
# #         elif sentiment == "Tentative":
# #             tentative_tone.append(score)
# #         elif sentiment == "Fear":
# #             fear_tone.append(score)
# #         elif sentiment == "Joy":
# #             joy_tone.append(score)
# #         elif sentiment == "Confident":
# #             confident_tone.append(score)

# #     values = np.array([0,1,2])*3
# #     fig = plt.figure(figsize=(12, 6))
# #     sns.set_style("whitegrid")
# #     plt.xlim(-1.5, 10)

# #     plt.bar(values , analytical_tone , width = 0.4 , label = 'Analytical')
# #     plt.bar(values+0.4 , confident_tone , width = 0.4 , label = 'Confidence')
# #     plt.bar(values+0.8 , fear_tone , width = 0.4 , label = 'Fear')
# #     plt.bar(values-0.4 , joy_tone , width = 0.4 , label = 'Joy')
# #     plt.bar(values-0.8 , tentative_tone , width = 0.4 , label = 'Tentative')

# #     plt.xticks(ticks = values , labels = ['Question 1','Question 2','Question 3'] , fontsize = 15 , fontweight = 60)
# #     plt.yticks(fontsize = 12 , fontweight = 90)
# #     ax = plt.gca()
# #     ax.xaxis.set_ticks_position('none')
# #     ax.yaxis.set_ticks_position('none')                    
# #     ax.xaxis.set_tick_params(pad = 5)
# #     ax.yaxis.set_tick_params(pad = 5)
# #     plt.legend()
# #     plt.savefig(f'./static/tone_analysis.jpg' , bbox_inches = 'tight')

# #     # save all responses
# #     with open('./static/answers.json' , 'w') as file:
# #         json.dump(responses , file)

# #     # face emotion recognition - plotting the emotions against time in the video
# #     videos = ["question1.webm", "question2.webm", "question3.webm"]
# #     frame_per_sec = 100
# #     size = (1280, 720)

# #     video = cv2.VideoWriter(f"./static/combined.webm", cv2.VideoWriter_fourcc(*"VP90"), int(frame_per_sec), size)

# #     # Write all the frames sequentially to the new video
# #     for v in videos:
# #         curr_v = cv2.VideoCapture(f'./static/{v}')
# #         while curr_v.isOpened():
# #             r, frame = curr_v.read()    
# #             if not r:
# #                 break
# #             video.write(frame)         
# #     video.release()

# #     face_detector = FER(mtcnn=True)
# #     input_video = Video(r"./static/combined.webm")
# #     processing_data = input_video.analyze(face_detector, display = False, save_frames = False, save_video = False, annotate_frames = False, zip_images = False)
# #     vid_df = input_video.to_pandas(processing_data)
# #     vid_df = input_video.get_first_face(vid_df)
# #     vid_df = input_video.get_emotions(vid_df)
# #     pltfig = vid_df.plot(figsize=(12, 6), fontsize=12).get_figure()
# #     plt.legend(fontsize = 'large' , loc = 1)
# #     pltfig.savefig(f'./static/fer_output.png')

# #     return "success"


# # # Interview completed response message
# # @app.route('/recorded')
# # def response():
# #     return render_template('recorded.html')


# # # Display results to interviewee
# # @app.route('/info')
# # def info():
# #     with open('./static/result.json' , 'r') as file:
# #         output = json.load(file)

# #     with open('./static/answers.json' , 'r') as file:
# #         answers = json.load(file)

# #     return render_template('result.html' , output = output , responses = answers)


# # # Send job confirmation mail to selected candidate
# # @app.route('/accept' , methods=['GET'])
# # def accept():

# #     with open('./static/result.json' , 'r') as file:
# #         output = json.load(file)
    
# #     name = output['Name']
# #     email = output['Email']
# #     position = "Software Development Engineer"

# #     msg = Message(f'Job Confirmation Letter', sender = MAIL_USERNAME, recipients = [email])
# #     msg.body = f"Dear {name},\n\n" + f"Thank you for taking the time to interview for the {position} position. We enjoyed getting to know you. We have completed all of our interviews.\n\n"+ f"I am pleased to inform you that we would like to offer you the {position} position. We believe your past experience and strong technical skills will be an asset to our organization. Your starting salary will be $15,000 per year with an anticipated start date of July 1.\n\n"+ f"The next step in the process is to set up meetings with our CEO, Rahul Dravid\n\n."+ f"Please respond to this email by June 23 to let us know if you would like to accept the SDE position.\n\n" + f"I look forward to hearing from you.\n\n"+ f"Sincerely,\n\n"+ f"Harsh Verma\nHuman Resources Director\nPhone: 555-555-1234\nEmail: feedbackmonitor123@gmail.com"
# #     mail.send(msg)

# #     return "success"

# # # Send mail to rejected candidate
# # @app.route('/reject' , methods=['GET'])
# # def reject():

# #         with open('./static/result.json' , 'r') as file:
# #             output = json.load(file)
        
# #         name = output['Name']
# #         email = output['Email']
# #         position = "Software Development Engineer"

# #         msg = Message(f'Your application to Smart Hire', sender = MAIL_USERNAME, recipients = [email])
# #         msg.body = f"Dear {name},\n\n" + f"Thank you for taking the time to consider Smart Hire. We wanted to let you know that we have chosen to move forward with a different candidate for the {position} position.\n\n"+ f"Our team was impressed by your skills and accomplishments. We think you could be a good fit for other future openings and will reach out again if we find a good match.\n\n"+ f"We wish you all the best in your job search and future professional endeavors.\n\n"+ f"Regards,\n\n"+ f"Harsh Verma\nHuman Resources Director\nPhone: 555-555-1234\nEmail: feedbackmonitor123@gmail.com"
# #         mail.send(msg)

# #         return "success"


# # # if __name__ == '__main__':
# # #     app.run(debug = True)
# # if __name__ == '__main__':
# #     app.debug = True
# #     app.run()
# Import all the necessary libraries
import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg' to avoid GUI requirements
import matplotlib.pyplot as plt
# import seaborn as sns
# import numpy as np
import numpy as np
from numpy.core.numeric import NaN
import pandas as pd
import seaborn as sns
# import matplotlib.pyplot as plt
# import module .venv
import json
import re
import time
import cv2
import spacy
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from flask import Flask , render_template , request , url_for , jsonify , Response
from werkzeug.utils import redirect, secure_filename
from flask_mail import Mail , Message
from flask_mysqldb import MySQL
from pyresparser import ResumeParser
from fer import Video
from fer import FER
from video_analysis import extract_text , analyze_sentiment
from decouple import config
nlp = spacy.load('en_core_web_sm')
# spacy.load('en_core_web_sm')

# Access the environment variables stored in .env file
MYSQL_USER = config('mysql_user')
MYSQL_PASSWORD = config('mysql_password')

# To send mail (By interviewee)
MAIL_USERNAME = config('mail_username')
MAIL_PWD = config('mail_pwd')

# For logging into the interview portal
COMPANY_MAIL = config('company_mail')
COMPANY_PSWD = config('company_pswd')

# Create a Flask app
app = Flask(__name__)

# App configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = 'smarthire' 
user_db = MySQL(app)

mail = Mail(app)              
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PWD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_ASCII_ATTACHMENTS'] = True
mail = Mail(app)


# Initial sliding page
@app.route('/')
def home():
    return render_template('index.html')


# Interviewee signup 
@app.route('/signup' , methods=['POST' , 'GET'])
def interviewee():
    if request.method == 'POST' and 'username' in request.form and 'usermail' in request.form and 'userpassword' in request.form:
        username = request.form['username']
        usermail = request.form['usermail']
        userpassword = request.form['userpassword']

        cursor = user_db.connection.cursor()

        cursor.execute("SELECT * FROM candidates WHERE candidatename = % s AND email = %s", (username, usermail))
        account = cursor.fetchone()
        
        if account:
            err = "Account Already Exists"
            return render_template('index.html' , err = err)
        elif not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', usermail):
            err = "Invalid Email Address !!"
            return render_template('index.html' , err = err)
        elif not re.fullmatch(r'[A-Za-z0-9\s]+', username):
            err = "Username must contain only characters and numbers !!"
            return render_template('index.html' , err = err)
        elif not username or not userpassword or not usermail:
            err = "Please fill out all the fields"
            return render_template('index.html' , err = err)
        else:
            cursor.execute("INSERT INTO candidates VALUES (NULL, % s, % s, % s)" , (username, usermail, userpassword,))
            user_db.connection.commit()
            reg = "You have successfully registered !!"
            return render_template('FirstPage.html' , reg = reg)
    else:
        return render_template('index.html')


# Interviewer signin 
@app.route('/signin' , methods=['POST' , 'GET'])
def interviewer():
    if request.method == 'POST' and 'company_mail' in request.form and 'password' in request.form:
        company_mail = request.form['company_mail']
        password = request.form['password']

        if company_mail == COMPANY_MAIL and password == COMPANY_PSWD:
            return render_template('candidateSelect.html')
        else:
            return render_template("index.html" , err = "Incorrect Credentials")
    else:
        return render_template("index.html")

# personality trait prediction using Logistic Regression and parsing resume
@app.route('/prediction' , methods = ['GET' , 'POST'])
def predict():
    # get form data
    if request.method == 'POST':
        fname = request.form['firstname'].capitalize()
        lname = request.form['lastname'].capitalize()
        age = int(request.form['age'])
        gender = request.form['gender']
        email = request.form['email']
        file = request.files['resume']
        path = './static/{}'.format(file.filename)
        file.save(path)
        val1 = float(request.form['openness'])
        val2 = float(request.form['neuroticism'])
        val3 = float(request.form['conscientiousness'])
        val4 = float(request.form['agreeableness'])
        val5 = float(request.form['extraversion'])
        # model prediction
        df = pd.read_csv(r'static\trainDataset.csv')
        le = LabelEncoder()
        df['Gender'] = le.fit_transform(df['Gender'])
        x_train = df.iloc[:, :-1].to_numpy()
        y_train = df.iloc[:, -1].to_numpy(dtype = str)
        lreg = LogisticRegression(multi_class='multinomial', solver='newton-cg',max_iter =1000)
        lreg.fit(x_train, y_train)
        if gender == 'male':
            gender = 1
        elif gender == 'female': 
            gender = 0
        input =  [gender, age, val1, val2, val3, val4, val5]
        # print("Gender after conversion:", gender)

        pred = str(lreg.predict([input])[0]).capitalize()

        # get data from the resume
        data = ResumeParser(path).get_extracted_data()
        result = {'Name': fname + ' ' + lname, 'Age': age, 'Email': email, 'Mobile Number': data.get('mobile_number', None),
          'Skills': str(data['skills']).replace("[", "").replace("]", "").replace("'", "") if data else None,
          'Degree': data.get('degree', [None])[0] if data else None,
          'Designation': data.get('designation', [None])[0] if data and data.get('designation') else None,
        #   'Designation': data.get('designation', [None])[0] if data else None,
          'Total Experience': data.get('total_experience', None),
          'Predicted Personality': pred}

        # result = {'Name':fname+' '+lname , 'Age':age , 'Email':email , 'Mobile Number':data.get('mobile_number', None) , 
        # 'Skills':str(data['skills']).replace("[" , "").replace("]" , "").replace("'" , "") , 'Degree':data.get('degree' , None)[0] , 'Designation':data.get('designation', None)[0] ,
        # 'Total Experience':data.get('total_experience') , 'Predicted Personality':pred}

        with open('./static/result.json' , 'w') as file:
            json.dump(result , file)

    return render_template('questionPage.html')
@app.route('/analysis', methods=['POST'])
def video_analysis():
    # Get the video file for the single question
    question_video = request.files["question1"]
    question_video.save("./static/question1.webm")

    # Speech-to-text response for the single question
    text, newdata = extract_text("question1.webm")
    time.sleep(15)  # Placeholder delay for processing
    
    # Save the response for the single question
    with open('./static/answers.json', 'w') as file:
        json.dump({"How would you handle a situation where two project teams, one girls and one boys, are in conflict over language use, and also manage the project if a team member becomes severely ill and hospitalized near the deadline?": [text]}, file)

    # Perform sentiment analysis on the extracted text using Google Cloud Natural Language API
    sentiment_result = analyze_sentiment(text)

    # Determine sentiment from the analysis
    sentiment = 'Positive' if sentiment_result['magnitude'] > 0 else 'Negative' if sentiment_result['magnitude'] < 0 else 'Neutral'
    
    # Save sentiment analysis result as a plot
    fig = plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    color = 'green' if sentiment == 'Positive' else 'red' if sentiment == 'Negative' else 'gray'
    bars = plt.bar(np.arange(1), [1 if sentiment == 'Positive' else -1 if sentiment == 'Negative' else 0], color=color)
    plt.xticks(np.arange(1), ['Question 1'], fontsize=15, fontweight=60)
    plt.yticks(np.arange(-1, 2), ['Negative', 'Neutral', 'Positive'], fontsize=12, fontweight=90)
    plt.xlabel('Questions', fontsize=15, fontweight=60)
    plt.ylabel('Sentiment', fontsize=15, fontweight=60)
    plt.title('Sentiment Analysis', fontsize=15, fontweight=60)
    plt.savefig('./static/sentiment_analysis.jpg', bbox_inches='tight')
    plt.close(fig)

    # Perform face emotion recognition on the video
    face_detector = FER(mtcnn=True)
    input_video = Video(r"./static/question1.webm")
    processing_data = input_video.analyze(face_detector, display=False, save_frames=False, save_video=False,
                                          annotate_frames=False, zip_images=False)
    vid_df = input_video.to_pandas(processing_data)
    vid_df = input_video.get_first_face(vid_df)
    vid_df = input_video.get_emotions(vid_df)
    pltfig = vid_df.plot(figsize=(12, 6), fontsize=12).get_figure()
    plt.legend(fontsize='large', loc=1)
    pltfig.savefig(f'./static/fer_output.png')

    return "success"
# Interview completed response message
@app.route('/recorded')
def response():
    return render_template('recorded.html')


# Display results to interviewee
@app.route('/info')
def info():
    with open('./static/result.json', 'r') as file:
        output = json.load(file)

    with open('./static/answers.json', 'r') as file:
        answers = json.load(file)

    return render_template('result.html', output=output, responses=answers)


# Send job confirmation mail to selected candidate
@app.route('/accept', methods=['GET'])
def accept():
    with open('./static/result.json', 'r') as file:
        output = json.load(file)

    name = output['Name']
    email = output['Email']
    position = "Software Development Engineer"

    msg = Message(f'Job Confirmation Letter', sender=MAIL_USERNAME, recipients=[email])
    msg.body = f"Dear {name},\n\n" + f"Thank you for taking the time to interview for the {position} position. We enjoyed getting to know you. We have completed all of our interviews.\n\n" + f"I am pleased to inform you that we would like to offer you the {position} position. We believe your past experience and strong technical skills will be an asset to our organization. Your starting salary will be $15,000 per year with an anticipated start date of July 1.\n\n" + f"The next step in the process is to set up meetings with our CEO, Steve Carell\n\n." + f"Please respond to this email by June 23 to let us know if you would like to accept the SDE position.\n\n" + f"I look forward to hearing from you.\n\n" + f"Sincerely,\n\n" + f"Ashnuta Upadhyaya\nHuman Resources Director\nPhone: 9087654567\nEmail: feedbackmonitor123@gmail.com"
    mail.send(msg)

    return "success"

# Send mail to rejected candidate
@app.route('/reject', methods=['GET'])
def reject():
    with open('./static/result.json', 'r') as file:
        output = json.load(file)

    name = output['Name']
    email = output['Email']
    position = "Software Development Engineer"

    msg = Message(f'Your application to Smart Hire', sender=MAIL_USERNAME, recipients=[email])
    msg.body = f"Dear {name},\n\n" + f"Thank you for taking the time to consider Smart Hire. We wanted to let you know that we have chosen to move forward with a different candidate for the {position} position.\n\n" + f"Our team was impressed by your skills and accomplishments. We think you could be a good fit for other future openings and will reach out again if we find a good match.\n\n" + f"We wish you all the best in your job search and future professional endeavors.\n\n" + f"Regards,\n\n" + f"Ashnuta Upadhyaya\nHuman Resources Director\nPhone: 9087654567\nEmail: feedbackmonitor123@gmail.com"
    mail.send(msg)
    return "success"
if __name__ == '__main__':
    app.debug = True
    app.run()