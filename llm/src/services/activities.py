from temporalio import activity
from llm.src.services.openai_helper import OpenAi

@activity.defn
async def process_create_task_for_chat_messages(prompt_template, messages):
    openai_instance = OpenAi()
    result = openai_instance.process_create_task_for_chat_messages(prompt_template, messages)
    print(f"OpenAI process: {result}")  
    return result

@activity.defn
async def created_tasks_for_message(messages):
    openai_instance = OpenAi()
    result = openai_instance.created_tasks_for_message(messages)
    print(f"OpenAI create tasks response: {result}")  
    return result 
