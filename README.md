# Signa

Signa can help break your boundaries, broaden your horizon, and make friends. Now you can talk with people just by using ASL. It will start translating your actions into words, and at the same time, the translated text will be spoken out using an AI voice so that your friend can easily understand you. 

<details>
      <summary><b><h3>Why American Sign Language?</h3></b></summary>

    
## Why American Sign Language?

For millennia, deaf people were neither considered humans nor were they treated with respect. Nobody even tried to communicate with them. But this injustice against them started coming to an end in the Renaissance, when people understood that deaf people were also capable of language. <b>`The person who played a big role in this transformation Charles-Michel de l'Épée, a French priest and philanthropist, who is now hailed as the Father of the deaf.`</b>
             
In the 1700s, Charles-Michel de l'Épée had a chance encounter with two young deaf sisters who were communicating with sign language. This inspired him to dedicate his life for the deaf. Soon, he developed a system of instruction of the French language and religion using the sign language and founded the world's first free school for the deaf (SEE THE SCHOOL BELOW).


![school](https://user-images.githubusercontent.com/99767517/215754432-3396b1ba-6e10-41e6-b574-a4aebc24147e.jpg)


Decades later, De lÉpée's methods inspired Laurent Clerc, a deaf teacher from France. In 1815, Thomas Hopkins Gallaudet, an American searching for a way to teach
the deaf, met Clerc. Gallaudet invited Clerc to come to the USA. Once they arrived there, Clerc taught Gallaudet how to use the sign language, and in return, 
Gallaudet taught Clerc English. Together, they established the first school for the deaf Connecticut in the USA, where it stands even today (Source: <a href ="https://www.hearinglikeme.com/sign-languages-around-the-world/#:~:text=American%20Sign%20Language%20(ASL)%20is,Thomas%20Gallaudet%20and%20Laurent%20Clerc." target="_blank">www.hearinglikeme.com</a>). This is how ASL came into existence. Today, ASL is the widely used sign language across the world, with signers in the USA, Canada, Mexico, Africa, and Asia (Source: <a href = "https://www.amazon.com/American-Sign-Language-Workbook-Vocabulary/dp/1646119509" target="_blank">American Sign Language Workbook</a>). That's why I chose ASL - To help as much as many people as possible. 
    
</details>

<details>
    <summary><b><h3>What can Signa do for you?</h3></b></summary>

## What can Signa do for you?

Want to make friends with those who can only use sign language? Or are you a sign language user who wants to make friends with those who speak English? Either way, Signa can be a great companion who can help you reach your goal faster. After all, everyone deserves to make friends despite the abilities they are born with. 
And Signa is your key to doing that.

    
</details>

# Workflow

![design](https://user-images.githubusercontent.com/99767517/214328113-27cb8464-5776-4ca8-8633-35fedecdf53e.gif)

# Usage
NB: I'm using Windows 10.

## Installing libraries

I suggest creating a virtual environment and installing the libraries there.

       cd sign_language_folder
       python -m venv your_virtual_env_name
       your_virtual_env_name\code\strive.bat
       pip install -r requirement.txt

## Saving data

Run `app.py`

When the webcam vieo has loaded, press 'a' on the keyboard to activate the logging mode. By pressing '0' to '9' data get saved in `keypoint.csv`; whereby the first column represents the class labels (pressed keys) and the other columns are the normalized keypoints an distances. To save class labels extending from '10' to potentially '35', you can press alphabet keys (capital letters) from 'A' to 'Z', respectively.
If you change the number of classes, make sure to correspondingly update the variable `n_classes` in `model_architecture.py` file.

## Training

For training the model, simply run the entire file `train.ipynb`. If you change data, you'll probably need to experiment to obtain an acceptable model#s performance. In case you change the model architecture, make sure to correspondingly update the `model_architecture.py`.

## Running the web app

      cd flask_app
      python app.py
      
You'll be provided with a link where the app is running. In the image below, it's running for example at `http://127.0.0.1:5000`.

  
  ![Screenshot 2023-01-31 125549](https://user-images.githubusercontent.com/99767517/215753419-5156f5a5-0de8-421e-bc84-a1a0503594ac.png)
  
Go to that url, then you can see a breif about Signa, Sign language and American Sign Language. After that at the topic of <i>What can Signa do for you?</i> under that topic click below you will direct to another page after following the instruction given in that page you will directed to the Webcam. 

       To start the action you need to follow the instruction given below:
                   
                   * To append (press 'a')
                   * To convert the action into text (press 'r')
                   * To delete the stored information (press 'd')
  
 Full demonstration about this app is given in the link ↓ 😃


  https://www.youtubetrimmer.com/view/?v=r1NlKqTegO8&start=1316&end=1526&loop=0
  
  The list of the implemented interactions are stored in `label.csv`.
  
<img src="https://media.giphy.com/media/LnQjpWaON8nhr21vNW/giphy.gif" width="60"> <em><b>I love connecting with different people</b> so if you want to say <b>hi, I'll be happy to meet you more!</b> 😃 All feedback about this project are welcome here.
  
  
