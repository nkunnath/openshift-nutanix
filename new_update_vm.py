import json
import time
import requests
from variables import *
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



header = {"content-type": "application/json"}
auth = HTTPBasicAuth(PC_USERNAME,PC_PASSWORD)



def list_vms(ip_address):
    '''
    List all the VMs in the cluster
    '''
    data_list = {
      "kind": "vm",
      "length": 500
    }
    url_list = "https://{0}:9440/api/nutanix/v3/vms/list".format(ip_address)
    res_list = requests.post(url=url_list, data=json.dumps(data_list), auth=auth, headers=header, verify=False)
    return res_list



def get_node_uuid(vm_name):
    '''
    Obtain VM UUID from name
    '''
    res_list = list_vms(PC_IP_ADDRESS)
    for vm_item in res_list.json().get('entities'):
        if vm_item.get('spec').get('name') == vm_name:
            vm_uuid = vm_item.get('metadata').get('uuid')
    return vm_uuid



def power_off_nodes(vm_uuid):
    """
    Power OFF a VM
    """
    url = "https://{0}:9440/api/nutanix/v3/vms/{1}".format(PC_IP_ADDRESS, vm_uuid)
    res = requests.get(url=url, auth=auth, headers=header, verify=False)
    spec = res.json().get('spec')
    spec.get('resources')['power_state'] = "OFF"  # Update VM spec
    list_meta_dict = ['kind', 'uuid', 'spec_version']
    new_metadata = {key : res.json().get('metadata')[key] for key in list_meta_dict}
    new_payload = {"api_version" : res.json().get('api_version'), "metadata" : new_metadata, "spec" : spec}
    res = requests.put(url=url, data=json.dumps(new_payload),auth=auth, headers=header, verify=False)
    return res
    

def update_disks(vm_uuid):
    """
    Change the boot disk of a VM
    """
    url = "https://{0}:9440/api/nutanix/v3/vms/{1}".format(PC_IP_ADDRESS, vm_uuid)
    res = requests.get(url=url, auth=auth, headers=header, verify=False)
    spec = res.json().get('spec')
    update_spec = {"boot_config" : {"boot_type": "LEGACY", "boot_device": {"disk_address": {"device_index": 1, "adapter_type": "SCSI"}}}}
    spec.get('resources').update(update_spec)               # Update VM spec
    list_meta_dict = ['kind', 'uuid', 'spec_version']
    new_metadata = {key : res.json().get('metadata')[key] for key in list_meta_dict}
    new_payload = {"api_version" : res.json().get('api_version'), "metadata" : new_metadata, "spec" : spec}
    res = requests.put(url=url, data=json.dumps(new_payload),auth=auth, headers=header, verify=False)
    return res



def power_on_nodes(vm_uuid):
    """
    Power ON a VM
    """
    url = "https://{0}:9440/api/nutanix/v3/vms/{1}".format(PC_IP_ADDRESS, vm_uuid)
    res = requests.get(url=url, auth=auth, headers=header, verify=False)
    spec = res.json().get('spec')
    spec.get('resources')['power_state'] = "ON"          # Update VM spec
    list_meta_dict = ['kind', 'uuid', 'spec_version']
    new_metadata = {key : res.json().get('metadata')[key] for key in list_meta_dict}
    new_payload = {"api_version" : res.json().get('api_version'), "metadata" : new_metadata, "spec" : spec}
    res = requests.put(url=url, data=json.dumps(new_payload),auth=auth, headers=header, verify=False)
    return res



def update_vm(vm_name):
    """
    Updating the boot disk of a VM when called from OpenShift installer
    """
    vm_uuid = get_node_uuid(vm_name)
    url = "https://{0}:9440/api/nutanix/v3/vms/{1}".format(PC_IP_ADDRESS, vm_uuid)
    print("Powering OFF {0}".format(vm_name), end="\n")
    power_off_nodes(vm_uuid)
    time.sleep(20)
    res = requests.get(url=url, auth=auth, headers=header, verify=False)
    if res.json().get('spec').get('resources').get('power_state') == "OFF":
        print("{0} is powered off successfully". format(vm_name), end="\n")
        print("Updating the boot disk for {0}".format(vm_name), end="\n")
        update_disks(vm_uuid)
    time.sleep(20)
    res = requests.get(url=url, auth=auth, headers=header, verify=False)
    print("AFTER UPDATING DISKS, GET IT ----- {0}".format(res.json()))
    if res.json().get('spec').get('resources').get('boot_config').get('boot_device').get('disk_address').get('adapter_type') == "SCSI":
        print("{0} boot device is updated successfully". format(vm_name), end="\n")
        print("Powering ON {0}".format(vm_name), end="\n") 
        power_on_nodes(vm_uuid)
    time.sleep(20)
    res = requests.get(url=url, auth=auth, headers=header, verify=False)
    if res.json().get('spec').get('resources').get('power_state') == "ON":
        print("{0} is powered on successfully". format(vm_name), end="\n")




