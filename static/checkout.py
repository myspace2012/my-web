from flask import Flask, render_template, request
import stripe

app = Flask(__name__)

# Set up Stripe API keys
stripe.api_key = "YOUR_STRIPE_SECRET_KEY"
stripe_public_key = "YOUR_STRIPE_PUBLIC_KEY"

# Define route for index page
@app.route("/")
def index():
    return render_template("index.html", stripe_public_key=stripe_public_key)

# Define route for charge page
@app.route("/charge", methods=["POST"])
def charge():
    # Get amount and Stripe token from request
    amount = request.form["amount"]
    stripe_token = request.form["stripeToken"]

    try:
        # Create Stripe charge
        charge = stripe.Charge.create(
            amount=int(float(amount) * 100), # Convert to cents
            currency="usd",
            source=stripe_token,
            description="Payment example"
        )
        # Render success page
        return render_template("success.html", amount=amount)
    except stripe.error.StripeError as e:
        # Render error page
        return render_template("error.html", error_message=str(e))

if __name__ == "__main__":
    app.run(debug=True)
