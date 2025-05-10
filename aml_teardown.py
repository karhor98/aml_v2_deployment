from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Workspace
from az_config import RESOURCE_GROUP, SUBSCRIPTION_ID, AML_WORKSPACE

# Initialize credentials and client
try:
    credential = DefaultAzureCredential()
    # Check if given credential can get token successfully.
    credential.get_token("https://management.azure.com/.default")
except Exception as ex:
    # Fall back to InteractiveBrowserCredential in case DefaultAzureCredential not work
    # This will open a browser page for
    credential = InteractiveBrowserCredential()

if __name__ == "__main__":

    # Initialize ResourceManagementClient
    resource_client = ResourceManagementClient(credential, SUBSCRIPTION_ID)
    # Initialize MLClient
    ml_client = MLClient(credential, SUBSCRIPTION_ID, RESOURCE_GROUP)

    # Delete the AML workspace
    ml_client.workspaces.begin_delete(name=AML_WORKSPACE, delete_dependent_resources=True)
    print(f"Workspace '{AML_WORKSPACE}' deletion initiated.")

    # Delete the resource group
    resource_client.resource_groups.begin_delete(RESOURCE_GROUP)
    print(f"Resource group '{RESOURCE_GROUP}' deletion initiated.")