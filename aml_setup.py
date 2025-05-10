from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential, TokenCachePersistenceOptions, SharedTokenCacheCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Workspace, ComputeInstance, AmlCompute
from az_config import RESOURCE_GROUP, SUBSCRIPTION_ID, AML_WORKSPACE
import datetime

# Initialize credentials and client
try:
    credential = DefaultAzureCredential()
    # Check if given credential can get token successfully.
    credential.get_token("https://management.azure.com/.default")
except Exception as ex:
    credential = InteractiveBrowserCredential()

def create_resource_group(resource_client, resource_group_name, location):
    """
    Create a resource group in Azure.
    
    This function creates a resource group in the specified location using the Azure SDK for Python.
    If the resource group already exists, it will be updated with the new parameters.
    """
    # Check if the resource group already exists
    try : 
        existing_rg = resource_client.resource_groups.get(resource_group_name)
        if existing_rg:
            print(f"Resource group '{resource_group_name}' already exists.")
            return
    except Exception as ex:
        # If the resource group does not exist, an exception will be raised
        print(f"Resource group '{resource_group_name}' does not exist. Creating a new one.")

    # Create the resource group parameters
    resource_group_params = {
        "location": location,
        "tags": {
            "environment": "demo",
            "owner": "Kar Hor Yap",
        },
    }   
    # Create the resource group
    resource_client.resource_groups.create_or_update(resource_group_name, parameters=resource_group_params)

    print(f"Resource group '{resource_group_name}' created in location '{location}'.")

def create_aml_workspace(ml_client, resource_group_name, workspace_name, location):
    """
    Create an Azure Machine Learning workspace.
    
    This function creates a new Azure Machine Learning workspace in the specified resource group and location.
    """

    try:
        # Check if the workspace already exists
        existing_workspace = ml_client.workspaces.get(workspace_name)
        if existing_workspace:
            print(f"Azure Machine Learning workspace '{workspace_name}' already exists in resource group '{resource_group_name}'.")
            return
        
    except Exception:
        # If the workspace does not exist, an exception will be raised
        print(f"Azure Machine Learning workspace '{workspace_name}' does not exist. Creating a new one.")
    
        ## Create the workspace
        workspace = Workspace(
            name=workspace_name,
            location=location,
            display_name="Op Insight AML Workspace",
            description="Workspace created via Python SDK",
            tags={"purpose": "demo"},
            )
        
        # Begin workspace creation
        ml_client.workspaces.begin_create(workspace)
        print(f"Azure Machine Learning workspace '{workspace_name}' created in resource group '{resource_group_name}'.")

def create_compute_instance(ml_client, workspace_name, compute_instance_name):
    """
    Create a compute instance in the Azure Machine Learning workspace.
    
    This function creates a new compute instance in the specified Azure Machine Learning workspace.
    
    """
    ci_basic_name = compute_instance_name + datetime.datetime.now().strftime("%Y%m%d%H%M")
    ci_basic = ComputeInstance(name=ci_basic_name, 
                               size="STANDARD_DS3_v2",
                               tags={"purpose": "demo"})
    
    print(ci_basic)
    
    ml_client.begin_create_or_update(ci_basic).result()

    print(f"Compute instance '{ci_basic_name}' created in workspace '{workspace_name}'.")

if __name__ == "__main__":

    # Initialize ResourceManagementClient
    resource_client = ResourceManagementClient(credential, SUBSCRIPTION_ID)
    # Initialize MLClient
    ml_client = MLClient(credential, SUBSCRIPTION_ID, RESOURCE_GROUP)
    # create resource group
    create_resource_group(resource_client, RESOURCE_GROUP, location='uksouth')
    # Define workspace parameters
    # Create AML workspace
    create_aml_workspace(ml_client, RESOURCE_GROUP, AML_WORKSPACE, location='uksouth')
    # Create Compute instance
    # create_compute_instance(ml_client, AML_WORKSPACE, "basic-ci")