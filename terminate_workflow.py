from temporalio.client import Client
from temporalio.api.workflowservice.v1 import TerminateWorkflowExecutionRequest

async def terminate_workflow():
    client = await Client.connect("localhost:7233")

    # Terminate the workflow with the specific ID
    await client.workflow_service.terminate_workflow_execution(
        TerminateWorkflowExecutionRequest(
            namespace="default",  # Namespace of the workflow, usually "default"
            workflow_id="chat-task-workflow-id",  # Workflow ID to terminate
            reason="Terminating to start a new workflow execution"
        )
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(terminate_workflow())
