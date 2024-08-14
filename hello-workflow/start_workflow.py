from temporalio.client import Client
from simple_workflow import HelloWorkflow  # Import the workflow

async def main():
    # Connect to the Temporal server
    client = await Client.connect("localhost:7233")

    # Start the workflow
    result = await client.start_workflow(
        HelloWorkflow.run,  # Reference the run method of the workflow
        "Temporal",  # Argument to pass to the workflow method
        id="hello-workflow-id-2",  # Workflow ID
        task_queue="hello-task-queue"  # Task queue name
    )

    # Print the result
    print(f"Workflow result: {result}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
