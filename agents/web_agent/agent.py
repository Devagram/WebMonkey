from dotenv import load_dotenv
import os

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

project_id = os.getenv("PROJECT_ID")
region = os.getenv("REGION")
service_name = os.getenv("SERVICE_NAME")
port = os.getenv("PORT")
google_api_key = os.getenv("GOOGLE_API_KEY")


def obfuscate(val):
    if not val:
        return None
    if len(val) <= 4:
        return '*' * len(val)
    return val[:2] + '*' * (len(val) - 4) + val[-2:]


print("Loaded ENV variables:")
print(f"PROJECT_ID: {obfuscate(project_id)}")
print(f"REGION: {obfuscate(region)}")
print(f"SERVICE_NAME: {obfuscate(service_name)}")
print(f"PORT: {obfuscate(port)}")
print(f"GOOGLE_API_KEY: {obfuscate(google_api_key)}")

from google.adk.agents import Agent, LlmAgent, SequentialAgent
from .custom_tools import search_product_tool, add_to_cart_tool, proceed_to_checkout_tool


search_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="SearchAgent",
    description="Finds the product on the site",
    instruction="Use search_product and google_search tools to locate the correct product link.",
    tools=[search_product_tool],
)

add_to_cart_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="AddToCartAgent",
    description="Adds the found product to the cart",
    instruction="Use add_to_cart_tool to add the product to the cart.",
    tools=[add_to_cart_tool],
)

checkout_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="CheckoutAgent",
    description="Proceeds to the checkout page",
    instruction="Use proceed_to_checkout_tool to go to the checkout page.",
    tools=[proceed_to_checkout_tool],
)

workflow = SequentialAgent(
    name="PurchasePipelineAgent",
    sub_agents=[search_agent, add_to_cart_agent, checkout_agent],
    description="Orchestrates product search, add to cart, and checkout steps sequentially.",
)

root_agent = workflow
