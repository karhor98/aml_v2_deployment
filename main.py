from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from az_config import subscription_id, resource_group

def main():
    
    print("Hello from aml-v2-deployment!")

    ml_client = MLClient(
        DefaultAzureCredential(), subscription_id, resource_group
    )


if __name__ == "__main__":
    main()
