from temporalio.client import Client
from temporalio.worker import Worker
from workflows import ChatTaskWorkflow
from llm.src.services.activities import process_create_task_for_chat_messages, created_tasks_for_message
from llm.src.utilities.utils import read_file_as_string

async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="chat-task-queue",
        workflows=[ChatTaskWorkflow],
        activities=[read_file_as_string, process_create_task_for_chat_messages, created_tasks_for_message]
    )

    print("Worker started")
    await worker.run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
