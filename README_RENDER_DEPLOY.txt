Aditya Accounting - Render Ready (Option 2: Secure + Subscription)

This ZIP contains two separate services you can deploy on Render as two web services:
1) flask_dashboard/        -> The main accounting dashboard (Flask)
2) streamlit_subscription/ -> The subscription portal (Streamlit)

DEPLOY STEPS (Render):
- Create a GitHub repo and push the contents of this ZIP (keep folder structure).
- In Render, create TWO new web services:
  A) Service 1 - Flask Dashboard
     - Connect to the repo
     - In 'Advanced' choose the root folder: flask_dashboard
     - Build Command: pip install -r requirements.txt
     - Start Command (Procfile used): web: gunicorn app:app
  B) Service 2 - Streamlit Subscription
     - Connect to the same repo
     - In 'Advanced' choose the root folder: streamlit_subscription
     - Build Command: pip install -r requirements.txt
     - Start Command (Procfile used): web: streamlit run aditya_subsctiption_app.py --server.port $PORT

HOW IT WORKS:
- The Streamlit app is the subscription UI (QR payments). After payment, it calls the dashboard webhook:
  POST https://<your-flask-service>.onrender.com/payment_webhook
  with JSON {"email":"user@example.com","plan":"Monthly"}.
- The Flask dashboard has a simple /payment_webhook endpoint which marks an email as authorized.
- Users then login on the dashboard using the same email to access the protected pages.

SECURITY NOTES:
- This demo uses a simple in-memory authorized list (AUTHORIZED_USERS). In production:
  - Use a real DB (Postgres) on Render for persistence.
  - Validate signatures from payment gateway when receiving webhooks.
  - Use HTTPS (Render provides TLS by default).
  - Hash passwords and manage sessions securely.

PASSWORD:
- For local admin scripts, password used in examples: aditya@7357

If you want, I can also:
- Initialize a GitHub repo and push this code for you (if you provide access/token).
- Or walk you step-by-step to deploy on Render.
