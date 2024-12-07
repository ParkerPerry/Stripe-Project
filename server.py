"""
Python 3.6 or newer required.
"""
import stripe
import os

# This is your test secret API key.
stripe.api_key = 'sk_test_51QTAfbKnfO2fVDmQMLtsinL5px8nA5SpzN9ETmdvE4JfJmePBsc2JIamI5fgPQ63RrSdjCM5OzkOdEPsNeTwUujM00WJr04s83'

stripe.api_version = '2023-10-16'

from flask import Flask, jsonify, send_from_directory, request

app = Flask(__name__, static_folder='dist',
  static_url_path='/<path:path>', template_folder='dist')

@app.route('/account/<account>', methods=['POST'])
def update_account(account):
    try:
        connected_account = stripe.Account.modify(
          account,
          business_type="individual",
        )

        return jsonify({
          'account': connected_account.id,
        })
    except Exception as e:
        print('An error occurred when calling the Stripe API to update an account: ', e)
        return jsonify(error=str(e)), 500

@app.route('/account', methods=['POST'])
def create_account():
    try:
        account = stripe.Account.create(
          controller={
            "stripe_dashboard": {
              "type": "none",
            },
            "fees": {
              "payer": "application"
            },
            "losses": {
              "payments": "application"
            },
            "requirement_collection": "application",
          },
          capabilities={
            "transfers": {"requested": True}
          },
          country="US",
        )

        return jsonify({
          'account': account.id,
        })
    except Exception as e:
        print('An error occurred when calling the Stripe API to create an account: ', e)
        return jsonify(error=str(e)), 500

@app.route('/', defaults={'path': ''})

# Flask does not like serving static files with a sub-path, so just force them to serve up the frontend here
@app.route('/return/<path>')
@app.route('/refresh/<path>')
@app.route('/<path:path>')
def catch_all(path, **kwargs):
    if path and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(port=4242)