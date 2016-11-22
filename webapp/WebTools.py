# --- --- --- --- --- #
# --- Helper Code --- #
# --- --- --- --- --- #

import random, string, os, paramiko
from werkzeug.utils import secure_filename
import smtplib
# from vaults import webapp_dir, pages, errorPage, localPaths, serverPaths

def randomVal():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))

    return state

# ---

def uploadImage(filename, filepath, serverPath, sfn):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='ftp.travellrs.com',
                username='travellr',
                password='RMW@nasa2015',
                port=7822)
    sftp = ssh.open_sftp()
    # ---
    sftp.put( filepath, serverPath + filename, callback=None, confirm=True )
    sftp.close()
    ssh.close()
    os.remove( filepath )

    return str('http://travellrs.com/travellr/' + sfn + '/' + filename)

# ---

def processImage(img, folder, serverPath, sfn):
    file = img
    filename = randomVal() + secure_filename(file.filename)
    file.save( os.path.join( folder , filename ) )
    filepath = folder + filename
    link = uploadImage( filename, filepath, serverPath, sfn )

    return link

# --

def saveImageLocal(img, folder):
    file = img
    filename = randomVal() + secure_filename(file.name)
    file.save(os.path.join( folder , filename ))
    filepath = folder + filename

    return filepath

# --

def SendEmail( toEmail , emailSubject, contents ):
    msg = MIMEMultipart()

    msg['From'] = 'support@travellrs.com'
    msg['To'] = toEmail
    msg['Subject'] = emailSubject

    message = contents
    msg.attach(MIMEText(message))

    mailserver = smtplib.SMTP('a2ss31.a2hosting.com', 465)
    # identify ourselves to smtp gmail client
    mailserver.ehlo()
    # secure our email with tls encryption
    mailserver.starttls()
    # re-identify ourselves as an encrypted connection
    mailserver.ehlo()
    mailserver.login('support@travellrs.com', 'RMW@nasa2015')

    mailserver.sendmail('support@travellrs.com', toEmail, msg.as_string())

    mailserver.quit()

# ---
