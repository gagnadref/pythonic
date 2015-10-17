import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def init_gmail_server(username, password):
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username, password)
	return server


def send_email(server, me, to, subject, message_filename):
	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = me
	msg['To'] = ', '.join(to)
	msg.preamble = subject
	with open(message_filename, 'r') as f:
		attachment = MIMEText(f.read())
		attachment.add_header('Content-Disposition', 'attachment', filename=message_filename)
		msg.attach(attachment)
	server.sendmail(me, to, msg.as_string())

if __name__ == "__main__":
	me = 'jimmyscheesesteak@gmail.com'
	password = 'hashcode'
	server = init_gmail_server(me, password)

	to = ['florian.gagnadre@gmail.com']

	# send_email(server, me, to, "str(score)", "lolilol.txt")

	best_score = 0
	while true:
		score = run_algorithm()
		if score > best_score:
			best_score = score
			send_email(server, me, to, str(score), "lolilol.txt")

	server.quit()