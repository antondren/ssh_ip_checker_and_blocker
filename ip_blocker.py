import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_strings_from_file(filename: str) -> list[str]:
    with open(filename, 'r') as f:
        lines = f.readlines()
    strings = [line.strip() for line in lines]
    return strings


def get_logged_in_users() -> list:
    ssh_command = "who"
    who_response = subprocess.check_output(ssh_command, shell=True)
    who_response = who_response.decode().strip().split('\n')
    users_with_pts_and_ips = []
    for who in who_response:
        formatted_who = who.split(" ")
        who_list = []
        for who_f in formatted_who:
            if who_f != "":
                if "(" in who_f and ")" in who_f:
                    who_list.append(who_f.split("(")[1].split(")")[0])
                else:
                    who_list.append(who_f)
        users_with_pts_and_ips.append({"user": who_list[0], "pts": who_list[1], "ip": who_list[-1]})
    return users_with_pts_and_ips


def logout_user_by_pts(pts: str) -> None:
    command = ["sudo", "pkill", "-9", "-t", pts]
    subprocess.run(command, capture_output=False)


def block_ip_on_firewall(ip: str) -> None:
    command = ["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"]
    subprocess.run(command)
    command = ["sudo", "iptables-save"]
    subprocess.run(command)
    print(f"{ip} blocked.")


def prepare_and_send_email(not_allowed_ips: list[dict]) -> None:
    subject = f"Not allowed ips on server {SERVER_NAME}"
    message = "Security breach, not allowed ip connected to server"
    for not_allowed_ip in not_allowed_ips:
        message += f"\nuser {not_allowed_ip['user']} ip {not_allowed_ip['ip']}"

    for receiver_email in RECEIVERS_EMAIL:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            try:
                server.starttls()
            except smtplib.SMTPNotSupportedError:
                server.ehlo()
            if SMTP_AUTH:
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())

        print(f"Email sent successfully to {receiver_email}")


def main() -> None:
    allowed_ips = get_strings_from_file(IP_WHITELISTED_FILE_NAME)
    print(f"loaded those ips from whitelisted configuration - {allowed_ips}")

    logged_users = get_logged_in_users()
    print(f"currently logged users - {logged_users}")

    not_allowed_ips_list = []
    for user_and_ip in logged_users:
        user_ip = user_and_ip["ip"]
        if user_ip not in allowed_ips:
            logout_user_by_pts(user_and_ip["pts"])
            block_ip_on_firewall(user_and_ip["ip"])
            not_allowed_ips_list.append(user_and_ip)

    if not_allowed_ips_list:
        prepare_and_send_email(not_allowed_ips_list)
    print("Ip check is done")


if __name__ == "__main__":
    IP_WHITELISTED_FILE_NAME = "whitelist_ip.conf"

    SERVER_NAME = "Test"
    SENDER_EMAIL = "test_ip_blocker@ipblocker.pl"
    RECEIVERS_EMAIL = ["your_mail@gmail.com"]

    SMTP_AUTH = False
    SMTP_SERVER = "smtp.freesmtpservers.com"
    SMTP_PORT = 25
    SMTP_USERNAME = "your_email@example.com"
    SMTP_PASSWORD = "your_email_password"

    main()
