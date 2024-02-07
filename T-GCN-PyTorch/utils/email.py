# import dotenv
# import smtplib
# from email.mime.text import MIMEText
# from email.utils import formataddr
#
#
# def send_experiment_results_email(args, results, subject):
#     msg_args = str(vars(args))
#     msg_results = str(results)
#     msg = msg_args + "\n\n" + msg_results
#     send_email(msg, subject)
#
#
# def send_email(message, subject=None):
#     config = dotenv.dotenv_values(".env")
#     msg = MIMEText(message, "plain", "utf-8")
#     msg["From"] = formataddr([config["FROM_REALNAME"], config["FROM_ADDRESS"]])
#     msg["To"] = formataddr([config["TO_REALNAME"], config["TO_ADDRESS"]])
#     msg["Subject"] = subject
#     server = smtplib.SMTP()
#     server.connect(config["SMTP_ADDRESS"])
#     try:
#         server.login(config["FROM_ADDRESS"], config["EMAIL_PASSWORD"])
#     except:  # noqa: E722
#         print("Email login failed.")
#     server.sendmail(config["FROM_ADDRESS"], config["TO_ADDRESSES"].split(","), msg.as_string())
#     server.quit()


import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def send_experiment_results_email(args, results, subject):
    msg_args = str(vars(args))
    msg_results = str(results)
    msg = msg_args + "\n\n" + msg_results
    send_email(msg, subject)


def send_email(message, subject=None):
    # Use environment variables directly
    from_realname = os.environ.get("FROM_REALNAME")
    from_address = os.environ.get("FROM_ADDRESS")
    to_realname = os.environ.get("TO_REALNAME")
    to_address = os.environ.get("TO_ADDRESS")
    smtp_address = os.environ.get("SMTP_ADDRESS")
    email_password = os.environ.get("EMAIL_PASSWORD")

    msg = MIMEText(message, "plain", "utf-8")
    msg["From"] = formataddr([from_realname, from_address])
    msg["To"] = formataddr([to_realname, to_address])
    msg["Subject"] = subject

    server = smtplib.SMTP()
    server.connect(smtp_address)

    try:
        server.login(from_address, email_password)
    except Exception as e:
        print("Email login failed:", str(e))

    server.sendmail(from_address, to_address.split(","), msg.as_string())
    server.quit()

