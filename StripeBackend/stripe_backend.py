from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import stripe
import os
from dotenv import load_dotenv
import uvicorn

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Stripe Payment Backend",
    description="Backend for handling Stripe payments in React Native"
)

# Enable CORS for React Native requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Stripe API key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Pydantic model for request validation
class PaymentRequest(BaseModel):
    amount: int

# Test route to check if backend is working
@app.get("/")
def home():
    return {"message": "Stripe Backend is running"}

# Route to create a Stripe PaymentIntent
@app.post("/create-payment-intent")
async def create_payment_intent(payment: PaymentRequest):
    try:
        # Create a PaymentIntent with Stripe
        intent = stripe.PaymentIntent.create(
            amount=payment.amount,
            currency="usd",
            automatic_payment_methods={"enabled": True}
        )

        return JSONResponse({
            "clientSecret": intent.client_secret,
            "publishableKey": os.getenv("STRIPE_PUBLISHABLE_KEY")
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run the server on a different port (8001) to avoid conflicts
    uvicorn.run(app, host="0.0.0.0", port=8001)
