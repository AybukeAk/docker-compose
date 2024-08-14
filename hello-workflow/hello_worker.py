from temporalio.client import Client
from temporalio.worker import Worker
from simple_workflow import HelloWorkflow, say_hello

async def main():
    # Connect to the Temporal server
    client = await Client.connect("localhost:7233")

    # Set up the worker with the workflow and activity
    worker = Worker(client, task_queue="hello-task-queue", workflows=[HelloWorkflow], activities=[say_hello])

    # Run the worker
    await worker.run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

