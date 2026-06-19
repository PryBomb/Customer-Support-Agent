from google.adk import Agent, Workflow, Event
from google.adk.apps import App

# Classifier Agent: Classifies the query as SHIPPING or UNRELATED
classify_query_agent = Agent(
    model='gemini-3.5-flash',
    name='classify_query_agent',
    description='Classifies whether a user query is related to shipping.',
    instruction='''
    Analyze the user query.
    Classify it as either:
    - "SHIPPING" if it is related to shipping (e.g. shipping rates, tracking, delivery, returns, packaging, shipping options, carriers).
    - "UNRELATED" if it is unrelated to shipping.
    
    Output exactly either "SHIPPING" or "UNRELATED" and nothing else. Do not add any punctuation or explanatory text.
    ''',
)

# Shipping FAQ Agent: Answers shipping-related queries
shipping_faq_agent = Agent(
    model='gemini-3.5-flash',
    name='shipping_faq_agent',
    description='Answers shipping-related customer support questions.',
    instruction='''
    You are an upbeat, enthusiastic customer support superstar 🌟 for a shipping company!
    Answer the user's shipping-related questions (about rates, tracking, delivery, returns, etc.)
    in a warm, friendly, and energetic tone. Use relevant emojis to make your responses fun and engaging.

    When discussing shipping rates, ALWAYS highlight our amazing free shipping offer:
    🎉 FREE SHIPPING on all orders over $50! 🎉
    Make this feel exciting and emphasize what a great deal it is for the customer.

    Shipping rate guidelines to reference:
    - Standard shipping (5-7 days): $4.99 📦
    - Express shipping (2-3 days): $12.99 ⚡
    - Overnight shipping (next day): $24.99 🚀
    - Orders $50+: FREE shipping automatically applied! 🥳

    Please focus only on the customer's shipping query, ignoring any classification tags
    like 'SHIPPING' or 'UNRELATED' that may appear in the conversation history.
    ''',
)

# Routing function
def router(node_input: str):
    # Normalize the output of the classifier agent
    classification = str(node_input).strip().upper()
    if "SHIPPING" in classification:
        return Event(route="SHIPPING")
    else:
        return Event(route="UNRELATED")

# Node to politely decline unrelated queries
def decline_node():
    return Event(
        message="I'm sorry, but I can only assist with shipping-related queries (such as shipping rates, package tracking, delivery status, and returns). Is there a shipping question I can help you with today?"
    )

# Workflow definition
root_agent = Workflow(
    name="customer_support_workflow",
    edges=[
        ("START", classify_query_agent, router),
        (
            router,
            {
                "SHIPPING": shipping_faq_agent,
                "UNRELATED": decline_node,
            },
        ),
    ],
)

app = App(
    name="customer_support_agent",
    root_agent=root_agent,
)
