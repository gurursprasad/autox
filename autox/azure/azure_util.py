import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient


def get_vm_public_ip():
    try:
        credential = DefaultAzureCredential()
        compute_client = ComputeManagementClient(credential, os.environ.get("AZURE_SUBSCRIPTION_ID"))
        resource_group_name = os.environ.get("AZURE_RESOURCE_GROUP")
        vm_name = os.environ.get("AZURE_VM_NAME")
        vm = compute_client.virtual_machines.get(resource_group_name, vm_name)

        # nic_id = vm.network_profile.network_interfaces[0].id
        # nic_segments = nic_id.split('/')
        # nic_rg = nic_segments[4]
        # nic_name = nic_segments[-1]

        # network_client = NetworkManagementClient(credential, os.environ.get("AZURE_SUBSCRIPTION_ID"))

        # nic = network_client.network_interfaces.get(nic_rg, nic_name)

        # public_ip_id = nic.ip_configurations[0].public_ip_address.id
        # public_ip_name = public_ip_id.split('/')[-1]

        # public_ip = network_client.public_ip_addresses.get(nic_rg, public_ip_name)
        # return public_ip.ip_address
        return vm

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "Not available"


ip = get_vm_public_ip()
