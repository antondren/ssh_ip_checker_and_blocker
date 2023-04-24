# ssh_ip_checker_and_blocker
# IP Blocker README
This Python script checks currently logged users on the server and blocks their IP addresses if they are not on the whitelist of allowed IP addresses. It can also send an email notification to alert the server admin about the security breach.

# Installation
Install Python 3.
Install the required packages
# Configuration
Edit the configuration values in the if __name__ == "__main__": section of the script as follows:

IP_WHITELISTED_FILE_NAME: The filename of the file containing the list of allowed IP addresses.
SERVER_NAME: The name of the server.
SENDER_EMAIL: The email address of the sender.
RECEIVERS_EMAIL: A list of email addresses of the receivers.
SMTP_AUTH: Set it to True if your SMTP server requires authentication, otherwise set it to False.
SMTP_SERVER: The hostname or IP address of the SMTP server.
SMTP_PORT: The port number of the SMTP server.
SMTP_USERNAME: The username of the SMTP server, if SMTP_AUTH is True.
SMTP_PASSWORD: The password of the SMTP server, if SMTP_AUTH is True.
# Usage
Run the script using python ip_blocker.py.
The script will check the logged users and their IP addresses, and block the IP addresses that are not on the whitelist of allowed IP addresses.
If any IP address is blocked, an email notification will be sent to the admin email addresses specified in the configuration.
The script will print a message to indicate that the IP check is done.
