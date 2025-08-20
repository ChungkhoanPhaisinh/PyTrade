from DNSE import DNSEClient
from Entrade import EntradeClient
from imaplib import IMAP4_SSL
from email import message_from_bytes
from time import sleep, time
from os import getenv
from dotenv import load_dotenv
from json import dump, load

def AutoGetTradingTokenByEmailOTP(gmail, app_password, sender_email, is_dnse_otp = True, check_interval=2):
    print(f"Getting newest email from {sender_email}...")

    mail = IMAP4_SSL("imap.gmail.com")
    mail.login(gmail, app_password)

    try:
        while True:
            mail.select("inbox")
            status, data = mail.search(None, f'(UNSEEN FROM "{sender_email}" SUBJECT "Email OTP")') # Remove "SUBJECT" part if failed
            email_ids = data[0].split()

            if email_ids:
                latest_email_id = email_ids[-1]
                status, data = mail.fetch(latest_email_id, "(RFC822)")
                msg = message_from_bytes(data[0][1])

                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        content = part.get_payload(decode=True).decode()
                        otp_idx = content.index("à:")
                        return content[otp_idx+6:otp_idx+12]

            sleep(check_interval)
    finally:
        mail.close()
        mail.logout()

# Phải có 1 file .env trong cùng thư mục với file python này
load_dotenv()
gmailDNSE = getenv("gmailDNSE") # Email đăng kí tài khoản DNSE
passwordDNSE = getenv("passwordDNSE") # Mật khẩu đăng nhập tài khoản DNSE
appPasswordDNSE = getenv("appPasswordDNSE") # App Password cho email đăng kí tài khoản DNSE

gmailEntrade = getenv("gmailEntrade") # Email đăng kí tài khoản Entrade
passwordEntrade = getenv("passwordEntrade") # Mật khẩu đăng nhập tài khoản Entrade
appPasswordEntrade = getenv("appPasswordEntrade") # App Password cho email đăng kí tài khoản Entrade


def SetupClient(dnse = True):
    # Read from JSON file
    try:
        with open("data.json", 'r') as f:
            loaded_data = load(f)
            f.close()
    except:
        loaded_data = {}

    # Setup Entrade
    entrade_client = EntradeClient()
    entrade_trading_token_acquired_date = -1 # Default value
    try:
        entrade_trading_token_acquired_date = int(loaded_data["entrade_trading_token_acquired_date"])
        if int(time()) - entrade_trading_token_acquired_date > 3600 * 8: # It's more than 8 hours since we get token/trading-token
            raise KeyError # Just so we make the client re-login

        entrade_client.token = loaded_data["entrade_token"]
        entrade_client.trading_token = loaded_data["entrade_trading_token"]
        print("Đăng nhập bằng token đã lưu thành công! (Entrade)")
    except KeyError:
        entrade_client.Authenticate(gmailEntrade, passwordEntrade)
        entrade_client.GetOTP()
        otp = AutoGetTradingTokenByEmailOTP(gmailEntrade, appPasswordEntrade, "noreply@mail.dnse.com.vn")
        entrade_client.GetTradingToken(otp)
        entrade_trading_token_acquired_date = int(time())

    # Setup DNSE
    dnse_client = None
    dnse_trading_token_acquired_date = -1
    if dnse:
        dnse_client = DNSEClient()
        try:
            dnse_trading_token_acquired_date = int(loaded_data["dnse_trading_token_acquired_date"])
            if int(time()) - dnse_trading_token_acquired_date > 3600 * 8: # It's more than 8 hours since we get token/trading-token
                raise KeyError # Just so we make the client re-login

            dnse_client.token = loaded_data["dnse_token"]
            dnse_client.trading_token = loaded_data["dnse_trading_token"]
            print("Đăng nhập bằng token đã lưu thành công! (DNSE)")
        except KeyError:
            dnse_client.Authenticate(gmailDNSE, passwordDNSE)
            dnse_client.GetOTP()
            otp = AutoGetTradingTokenByEmailOTP(gmailDNSE, appPasswordDNSE, "noreply@mail.dnse.com.vn")
            dnse_client.GetTradingToken(otp)
            dnse_trading_token_acquired_date = int(time())

    # Save to JSON file
    with open("data.json", 'w') as f:
        data = {
            "entrade_token": entrade_client.token,
            "entrade_trading_token": entrade_client.trading_token,
            "entrade_trading_token_acquired_date": entrade_trading_token_acquired_date,
            "dnse_token": dnse_client.token,
            "dnse_trading_token": dnse_client.trading_token,
            "dnse_trading_token_acquired_date": dnse_trading_token_acquired_date
        }
        dump(data, f, indent=4)
        f.close()

    return entrade_client, dnse_client