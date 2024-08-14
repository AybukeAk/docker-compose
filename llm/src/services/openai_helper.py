from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    import os
    import json
    from openai import OpenAIError
    from dotenv import load_dotenv
    from datetime import datetime, timedelta
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
    from llm.src.utilities.utils import read_file_as_string
    from langchain_openai import ChatOpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_LLM_MODEL = "gpt-3.5-turbo-0125" #gpt-4o-mini"
print(f"API Key: {OPENAI_API_KEY[:5]}...{OPENAI_API_KEY[-5:]}")

class OpenAi:

    def __init__(self):
        self.api_key = OPENAI_API_KEY
        self.chat = ChatOpenAI(model=DEFAULT_LLM_MODEL, temperature=0.1)

    def convert_messages_to_langchain_format(self, messages):
        chat_history = []
        last_guest_message = None
        for message in messages:
            text = message['text']  
            sender_type = message['senderType']  
            if sender_type == "guest":
                chat_history.append(HumanMessage(content=text))
                last_guest_message = text
            else:  # Both bot and client messages are saved as AI messages
                chat_history.append(AIMessage(content=text))
        return chat_history, last_guest_message
    
    def process_create_task_for_chat_messages(self, prompt_template, messages):
        # Debugging output
        print("Debug: prompt_template:", prompt_template)
        print("Debug: messages:", messages)

        # Initialize output variable
        output = None
        
        try:
            if not prompt_template:
                raise ValueError("Prompt template is None or invalid")

            if not messages or not isinstance(messages, list):
                raise ValueError("Messages are invalid or None")
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", prompt_template),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}")
            ])
            chain = prompt | self.chat

            chat_history, last_guest_message = self.convert_messages_to_langchain_format(messages)
            output = chain.invoke({"chat_history": chat_history, "input": last_guest_message})

        except OpenAIError as e:
            print(f"OpenAI API error: {e}")
            raise
        except ValueError as e:
            print("ValueError occurred: ", e)
            raise  
        except Exception as e:
            print("An unexpected error occurred: ", e)
            raise  

        return output

    def created_tasks_for_message(self, messages):
        created_tasks_for_message_prompt = read_file_as_string("src/templates/create_task_for_message_prompt.txt")

        task_create_response = self.process_create_task_for_chat_messages(
            created_tasks_for_message_prompt, messages
        )

        task_create_response_model_result = json.loads(task_create_response.content)

        return task_create_response_model_result
