from datetime import datetime, timedelta
from temporalio.client import Client

async def main():
    client = await Client.connect("localhost:7233")
    
    messages = [
        {"text": "there is no hot water", "senderType": "guest"}  
    ]
    
    result = await client.start_workflow(
        "ChatTaskWorkflow",                # Workflow type (workflow function name)
        messages,                          # Correctly structured messages
        id=f"workflow-{datetime.now().isoformat()}",  # Unique ID for the workflow
        task_queue="chat-task-queue",  # Task queue to use
        execution_timeout=timedelta(minutes=30),  
    )
    
    print(f"Workflow started: {result.id}")  # Use 'result.id' to get the workflow ID

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
