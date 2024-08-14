from datetime import timedelta
from temporalio import workflow
from llm.src.services.activities import process_create_task_for_chat_messages, created_tasks_for_message
from llm.src.utilities.utils import read_file_as_string

@workflow.defn
class ChatTaskWorkflow:
    @workflow.run
    async def run(self, messages):
        # Execute the read_file_as_string activity
        prompt_template = await workflow.execute_activity(
            read_file_as_string,  # The activity function
            "llm/src/templates/create_task_for_message_prompt.txt",  # Argument as a single tuple
            start_to_close_timeout=timedelta(seconds=60)
        )
        
        # Step 2: Process the chat messages via an activity

        task_create_response = await workflow.execute_activity(
            process_create_task_for_chat_messages,
            args=[prompt_template, messages],
            start_to_close_timeout=timedelta(seconds=60)
        )
        print(f"Task creation response: {task_create_response}")  # Debugging line


        task_create_response_model_result = await workflow.execute_activity(
            created_tasks_for_message,
            (messages,),  # Single argument in a tuple
            start_to_close_timeout=timedelta(seconds=60)
        )
        print(f"Task creation model result: {task_create_response_model_result}")  # Debugging line

        return task_create_response_model_result
