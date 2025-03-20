import time
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Etherscan page config
ETHERSCAN_API_KEY = "etherscan_api_key"
TOKEN_ADDRESS = "token_address"
API_URL = f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={TOKEN_ADDRESS}&page=1&offset=1&sort=desc&apikey={ETHERSCAN_API_KEY}"

# Email config
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "generated_application_password" # https://support.google.com/mail/answer/185833?hl=en
RECIPIENTS = [
    "recipient_email_1@gmail.com",
    "recipient_email_2@gmail.com",
    "recipient_email_3@gmail.com",
]

def send_email(tx_data):
    """
    Send an email to all recipients with details of the transaction.
    """
    subject = f"⚠️ {tx_data['tokenName']} ({tx_data['tokenSymbol']}) - New Transaction Detected"
    message = f"""
    <h2>New Transaction Detected!</h2>
    <p><b>Hash:</b> {tx_data['hash']}</p>
    <p><b>Block Number:</b> {tx_data['blockNumber']}</p>
    <p><b>Timestamp:</b> {tx_data['timeStamp']}</p>
    <p><b>Nonce:</b> {tx_data['nonce']}</p>
    <p><b>Block Hash:</b> {tx_data['blockHash']}</p>
    <p><b>From:</b> {tx_data['from']}</p>
    <p><b>To:</b> {tx_data['to']}</p>
    <p><b>Amount:</b> {int(tx_data['value']) / (10 ** int(tx_data['tokenDecimal']))} {tx_data['tokenSymbol']}</p>
    <p><b>Token Name:</b> {tx_data['tokenName']}</p>
    <p><b>Gas:</b> {tx_data['gas']}</p>
    <p><b>Gas Price:</b> {tx_data['gasPrice']}</p>
    <p><b>Gas Used:</b> {tx_data['gasUsed']}</p>
    <p><b>Cumulative Gas Used:</b> {tx_data['cumulativeGasUsed']}</p>
    <p><b>Input:</b> {tx_data['input']}</p>
    <p><b>Confirmations:</b> {tx_data['confirmations']}</p>
    <p><a href='https://etherscan.io/tx/{tx_data['hash']}'>View on Etherscan</a></p>
    """

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = ", ".join(RECIPIENTS)  # Combine recipients into a single string
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECIPIENTS, msg.as_string())
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

def check_new_transactions():
    """
    Check for new transactions using the Etherscan API.
    Returns the latest transaction data or None if no new transaction is found.
    """
    try:
        response = requests.get(API_URL)
        data = response.json()

        if "result" in data and len(data["result"]) > 0:
            return data["result"][0]  # Latest transaction
    except Exception as e:
        print(f"❌ Error getting transactions: {e}")
    
    return None

def process_transactions():
    """
    Process the new transaction and send an email if the transaction is new.
    """
    last_tx_hash = None
    is_first_tx = True
    
    while True:
        result = check_new_transactions()
        
        if result:
            if is_first_tx:
                is_first_tx = False
                last_tx_hash = result['hash']
                print("🔰 First transaction detected. No email will be sent.")
            
            elif result['hash'] != last_tx_hash:
                print("⚠️ New transfer detected. Sending email...")
                send_email(result)
                last_tx_hash = result['hash']
        
        time.sleep(20)

if __name__ == "__main__":
    process_transactions()
