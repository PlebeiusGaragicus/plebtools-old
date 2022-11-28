import sys

import smtplib, ssl, mimetypes

from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

class EmailHelper:
    
    address: str = None
    secret: str = None

    def __init__(self, address: str, secret: str):
        """ These arguments aren't set to default = None... we're not going
                to store these in an environment variable

        """

        self.address = address
        self.secret = secret


    def sendalert(self, subject: str, message: str, toList: str=None) -> bool:

        # send an email to myself if toList == None
        if toList == None:
            toList = self.address

        context = ssl.create_default_context()
        messagetosend = "Subject: {}\n\n{}".format(subject, message)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(self.address, self.secret)
            senterrors = server.sendmail(self.address, toList, messagetosend)
            server.quit()
            return senterrors


    def sendfile_inline(self, subject, filename, tolist=None):
        
        # send an email to myself if toList == None
        if tolist == None:
            tolist = self.address
        
        with open(filename, 'r') as msgfile:
            message = msgfile.read()
            context = ssl.create_default_context()
            messagetosend = "Subject: {}\n\n{}".format(subject, message)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                server.login(self.address, self.secret)
                senterrors = server.sendmail(self.address, tolist, messagetosend)
                server.quit()
                return senterrors











# #https://stackoverflow.com/questions/23171140/how-do-i-send-an-email-with-a-csv-attachment-using-python
# #https://docs.python.org/3.4/library/email-examples.html
# #######################################################################################
# def sendcsv(subject, filename, to=None):
#     if to == None:
#         to = credentials.adr

#     # BUG - only ONE recip at a time.... put in a for loop to get all addresses...

#     msg = MIMEMultipart()
#     msg["From"] = credentials.adr
#     msg["To"] = to
#     msg["Subject"] = subject
#     msg.preamble = "see attached"

#     ctype, encoding = mimetypes.guess_type(filename)
#     if ctype is None or encoding is not None:
#         ctype = "application/octet-stream"

#     maintype, subtype = ctype.split("/", 1)

#     if maintype == "text":
#         fp = open(filename)
#         # Note: we should handle calculating the charset
#         attachment = MIMEText(fp.read(), _subtype=subtype)
#         fp.close()
#     elif maintype == "image":
#         fp = open(filename, "rb")
#         attachment = MIMEImage(fp.read(), _subtype=subtype)
#         fp.close()
#     elif maintype == "audio":
#         fp = open(filename, "rb")
#         attachment = MIMEAudio(fp.read(), _subtype=subtype)
#         fp.close()
#     else:
#         fp = open(filename, "rb")
#         attachment = MIMEBase(maintype, subtype)
#         attachment.set_payload(fp.read())
#         fp.close()
#         encoders.encode_base64(attachment)
#     attachment.add_header("Content-Disposition", "attachment", filename=filename)
#     msg.attach(attachment)

#     server = smtplib.SMTP("smtp.gmail.com:587") # 465
#     server.starttls()
#     server.login(credentials.adr,credentials.psk)
#     server.sendmail(credentials.adr, to, msg.as_string())
#     server.quit()





# what would main do?
# ... run the user through a test/simple program.. a utility?
# ###########################
# if __name__ == "__main__":
#     if len(sys.argv) != 4:
#         print()
#         print("give only 3 arguments")
#         print(f"eg: {str(sys.argv[0])} 'to' 'subject' 'message'")
#         exit()

#     print(f"sending message:\nSubj:{str(sys.argv[1])}\nMesg:{str(sys.argv[2])}")
#     sendalert(str(sys.argv[1]), str(sys.argv[2]))
