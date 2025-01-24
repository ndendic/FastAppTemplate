from stripe import StripeClient
from dotenv import load_dotenv
import os


load_dotenv()

# stripe_key = os.environ["STRIPE_SECRET_KEY"]
# client = StripeClient(stripe_key)

# # list customers
# customers = client.customers.list()
# products = client.products.list()
# # print the first customer's email
# print(products.data)

# retrieve specific Customer
# customer = client.customers.retrieve("cus_123456789")

# print that customer's email
# print(customer.email)
