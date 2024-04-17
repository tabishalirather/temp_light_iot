from flask import Flask, request, jsonify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

# Set up SendGrid API key
SENDGRID_API_KEY = "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"

@app.route('/send-email', methods=['GET'])
def send_email():
    email = request.args.get('email', None)
    subject = "Hello from your IoT Application"
    content = "This is a test email sent from your Flask app using SendGrid."

    if email:
        message = Mail(
            from_email='103534434@student.swin.edu.au',  # Your SendGrid verified sender email
            to_emails=email,
            subject=subject,
            html_content=content
        )
        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            return jsonify({"message": "Email sent successfully!", "status_code": response.status_code})
        except Exception as e:
            print(e)
            return jsonify({"message": "Failed to send email.", "error": str(e)}), 500
    else:
        return jsonify({"message": "Email parameter is missing."}), 400

if __name__ == '__main__':
    app.run(debug=True)
