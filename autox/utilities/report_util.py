# import shutil
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders
# import os
# import sys

# import requests

# from utils.common_utils import get_public_ip

# from utils.common_utils import *
# from utils.rest_api_util import *


# def send_email(report_file, recipients):
#     fromaddr = os.environ.get("EMAIL_ADDRESS")
#     password = os.environ.get("EMAIL_PASSWORD")

#     # Get head node version and prepare new report file name
#     head_node_version = get_headnode_version_info()
#     base, ext = os.path.splitext(report_file)
#     new_report_file = f"{base}_{head_node_version}{ext}"

#     # Rename the report file
#     shutil.copy(report_file, new_report_file)

#     msg = MIMEMultipart()
#     msg['From'] = fromaddr
#     msg['To'] = ", ".join(recipients)
#     msg['Subject'] = f"Test Report for cop version: {head_node_version}"

#     body = "Please find the attached HTML report for the recent test run."
#     msg.attach(MIMEText(body, 'plain'))

#     # Attach the renamed report file
#     with open(new_report_file, "rb") as attachment:
#         part = MIMEBase('application', 'octet-stream')
#         part.set_payload(attachment.read())
#         encoders.encode_base64(part)
#         part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(new_report_file)}")
#         msg.attach(part)

#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.starttls()
#     server.login(fromaddr, password)
#     text = msg.as_string()
#     server.sendmail(fromaddr, recipients, text)
#     server.quit()

# if __name__ == "__main__":
#     if len(sys.argv) < 3:
#         print("Usage: python3 report_util.py <report_file> <recipients>")
#         sys.exit(1)

#     report_file = sys.argv[1]
#     recipients = sys.argv[2].split(",")  # comma-separated email addresses

#     send_email(report_file, recipients)
