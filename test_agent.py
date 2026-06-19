import asyncio
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
import sys
import os
sys.path.append(os.path.abspath("customer_support_agent"))
import agent
app = agent.app

# Load environment variables
load_dotenv("customer_support_agent/.env")

async def test_query(query: str):
    runner = InMemoryRunner(app=app)
    print(f"\n--- Testing Query: '{query}' ---")
    try:
        # run_debug runs the agent and returns the events
        events = await runner.run_debug(query)
        print(f"Events returned: {len(events)}")
        for event in events:
            # Print messages and outputs
            author = event.author or event.node_name or "System"
            if event.message:
                print(f"[{author}]: {event.message}")
            elif event.output:
                print(f"[{author} Output]: {event.output}")
    except Exception as e:
        print(f"Error executing agent: {e}")

async def main():
    # Test 1: Shipping query
    await test_query("How much does it cost to ship a 5lb package to New York?")
    
    # Test 2: Unrelated query
    await test_query("Who wrote Hamlet?")

if __name__ == "__main__":
    asyncio.run(main())
