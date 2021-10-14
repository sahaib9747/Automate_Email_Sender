import smtplib
import speech_recognition as sprecog
import pyttsx3
import abc 

from email.message import EmailMessage


class EmailSenderTemplate(metaclass = abc.ABCMeta):
    def build_server(self):
        pass

    def send_email(self):
        pass

    def get_data(self):
        pass 

    def speaker(self):
        pass


class EmailSender(EmailSenderTemplate):
    def __init__(self):
        self.email = 'exmaple@gmail.com'
        self.passowrd = 'passwordOfexample@gmail.com'
        self.receiver = ''
        self.subject = ''
        self.body = ''

    def build_server(self):
        ''' 
        It will create a SMPT server and Will try to log in with the desired credentials
        To logged in successfully, you have to follow few steps:
        log in > manage google account > security > allow less secure apps, otherwise it will fail to log in. 
        '''

        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls() 
        # go to your account and allow third party app script
        self.server.login(self.email, self.passowrd)

    def send_email(self):
        ''' This function will send the email to the desired recipients'''

        email = self.make_email()
        self.server.send_message(email)


    def make_email(self):
        '''
        This function will take required information from another function named get_data
        '''

        self.receiver = self.get_data() + '@gmail.com'
        self.speaker(self.receiver)

        self.subject = self.get_data().title()
        self.speaker(self.subject)

        self.body = self.get_data()
        self.speaker(self.body)

        email_template = EmailMessage()
        email_template['From'] = self.email
        email_template['To'] = self.receiver
        email_template['Subject'] = self.subject
        email_template.set_content = self.body

        return email_template


    def get_data(self):
        '''
        This function will try to connect microhpone first afterwards it will listen the speech from the user and will convert
        the speech into text using google API. 
        '''

        try: 
            with sprecog.Microphone as source:
                print('say, listening....')
                voice = sprecog.Recognizer.listen(source)
                text = sprecog.Recognizer.recognize_google(voice).lower()
                print(f"We captured: {text}")

                return text 
        except:
            print('Microphoen error occured')
    
    def speaker(self, text):
        '''
        It will make a sound stream and can play audio.
        '''
        SoundEngine = pyttsx3.init()
        SoundEngine.say(text)
        SoundEngine.runAndWait()


def app():
    while True: 
        email = EmailSender()
        email.build_server()  # prepare the server
        email.send_email()

        email.speaker('Do you want to continue sending emails say YES or No')
        
        if 'no' in email.get_data():
            break
        else:
            continue


if __name__ == '__main__':
    app()
