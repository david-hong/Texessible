import sendgrid

sg_username = input("Text us your Send Grid username: ")
sg_password = input("Text us your Send Grid password: ")
sg = sendgrid.SendGridClient(sg_username, sg_password, raise_errors=True)

user_name = input ("Text us your name: ")
user_email = input ("Text us your email: ")
user_email = "<" + user_email + ">"
user_from = user_name + " " + user_email

arb_input = input("Your email has been set up successfully.\nTo send an email, \
text 'Email to user@email.com Re: 'Subject Line' followed by your email message")
arb_input.strip()
text = arb_input.split()
text_body = ""
subject = ""
email_address = ""
c = '"'
c += "'"
if text[0].lower() == "email":
    #if there is a two
    if text[1] == "to":
        if "@" in text[2]:
            email_address = text[2]
            if 're:' in text[3].lower():
                i = len(text)-1
                while text[i][-1] not in c and i > 2:
                    i = i - 1
                x = i + 1
                while x < len(text):
                    text_body += text[x] + " "
                    x +=1
                for x in range(3, i+1):
                    subject += text[x] + " "

            
    #if there is not a to
    else:
        if "@" in text[1]:
            email_address = text[1]
            #append the rest of the text as the content
            if 're:' in text[2].lower():
                #if there is a space after re: 
                i = len(text)-1
                while i > 1 and text[i][-1] not in c:
                    i = i - 1
                x = i + 1
                while x < len(text):
                    text_body += text[x] + " "
                    x+=1
                for x in range(2, i+1):
                    subject +=text[x]+ " "
                
                #no space after re:, find element with last element quote

else:
    print ("Error: Incorrectly Formatted Email")
    

email_address = '<'+email_address+'>'


message = sendgrid.Mail()
message.add_to(email_address)
message.set_subject(subject)
message.set_html(text_body)
message.set_text('Sent from Ambiguous Texter')
message.set_from(user_from)
status, msg = sg.send(message)

