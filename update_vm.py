import json
import time
import getpass
import requests
from openshiftvar import *
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



header = {"content-type": "application/json"}
auth = HTTPBasicAuth(PC_USERNAME,PC_PASSWORD)

def make_request(ip_address):
    '''
    Function that return the response of the REST API call to list all the roles
    '''
    data_list = {
      "kind": "vm",
      "length": 20
    }
    url_list = "https://{0}:9440/api/nutanix/v3/vms/list".format(ip_address)
    res_list = requests.post(url=url_list, data=json.dumps(data_list), auth=auth, headers=header, verify=False)
    return res_list



def get_node_uuid(vm_name):
    #Get nodes UUID
    res_list = make_request(PC_IP_ADDRESS)
    vm_list = []
    for vm_item in res_list.json().get('entities'):
        if vm_item.get('spec').get('name') == vm_name:
            vm_uuid = vm_item.get('metadata').get('uuid')
    #print("VM UUID IS {0}".format(vm_uuid))
    return(vm_uuid) 





def power_off_nodes(vm_uuid):
    get_url = "https://{0}:9440/api/nutanix/v3/vms/{1}".format(PC_IP_ADDRESS, vm_uuid)
    res = requests.get(url=get_url, auth=auth, headers=header, verify=False)
    #print(res.json().get('spec').get('resources').get('power_state'))
    spec = res.json().get('spec')
    spec.get('resources')['power_state'] = "OFF"
    #print(spec)
    list_meta_dict = ['kind', 'uuid', 'spec_version']
    new_metadata = {key : res.json().get('metadata')[key] for key in list_meta_dict}
    new_payload = {"api_version" : res.json().get('api_version'), "metadata" : new_metadata, "spec" : spec}
    #print(new_payload)
    put_url = "https://{0}:9440/api/nutanix/v3/vms/{1}".format(PC_IP_ADDRESS, vm_uuid)
    res = requests.put(url=put_url, data=json.dumps(new_payload),auth=auth, headers=header, verify=False)
    

def update_disks(vm_uuid):
    get_url = "https://{0}:9440/api/nutanix/v3/vms/{1}".format(PC_IP_ADDRESS, vm_uuid)
    res = requests.get(url=get_url, auth=auth, headers=header, verify=False)
    #print(res.json().get('spec').get('resources').get('power_state'))
    spec = res.json().get('spec')
    b = {"boot_config" : {"boot_type": "LEGACY", "boot_device": {"disk_address": {"device_index": 1, "adapter_type": "SCSI"}}}}
    spec.get('resources').update(b)
    #print(spec)
    list_meta_dict = ['kind', 'uuid', 'spec_version']
    new_metadata = {key : res.json().get('metadata')[key] for key in list_meta_dict}
    new_payload = {"api_version" : res.json().get('api_version'), "metadata" : new_metadata, "spec" : spec}
    #print(new_payload)
    put_url = "https://{0}:9440/api/nutanix/v3/vms/{1}".format(PC_IP_ADDRESS, vm_uuid)
    res = requests.put(url=put_url, data=json.dumps(new_payload),auth=auth, headers=header, verify=False)



def power_on_nodes(vm_uuid):
    get_url = "https://{0}:9440/api/nutanix/v3/vms/{1}".format(PC_IP_ADDRESS, vm_uuid)
    res = requests.get(url=get_url, auth=auth, headers=header, verify=False)
    #print(res.json().get('spec').get('resources').get('power_state'))
    spec = res.json().get('spec')
    spec.get('resources')['power_state'] = "ON"
    #print(spec)
    list_meta_dict = ['kind', 'uuid', 'spec_version']
    new_metadata = {key : res.json().get('metadata')[key] for key in list_meta_dict}
    new_payload = {"api_version" : res.json().get('api_version'), "metadata" : new_metadata, "spec" : spec}
    #print(new_payload)
    put_url = "https://{0}:9440/api/nutanix/v3/vms/{1}".format(PC_IP_ADDRESS, vm_uuid)
    res = requests.put(url=put_url, data=json.dumps(new_payload),auth=auth, headers=header, verify=False)



def update_vm(vm_name):
    vm_uuid = get_node_uuid(vm_name)
    print("Powering OFF {0}".format(vm_name), end="\n")
    power_off_nodes(vm_uuid)
    time.sleep(15)
    get_url = "https://{0}:9440/api/nutanix/v3/vms/{1}".format(PC_IP_ADDRESS, vm_uuid)
    res = requests.get(url=get_url, auth=auth, headers=header, verify=False)
    if res.json().get('spec').get('resources').get('power_state') == "OFF":
        print("{0} is powered off successfully". format(vm_name), end="\n")
        print("Updating the boot disk for {0}".format(vm_name), end="\n")
        update_disks(vm_uuid)
    time.sleep(15)
    get_url = "https://{0}:9440/api/nutanix/v3/vms/{1}".format(PC_IP_ADDRESS, vm_uuid)
    res = requests.get(url=get_url, auth=auth, headers=header, verify=False)
    if res.json().get('spec').get('resources').get('boot_config').get('boot_device').get('disk_address').get('adapter_type') == "SCSI":
        print("{0} boot device is updated successfully". format(vm_name), end="\n")
        print("Powering ON {0}".format(vm_name), end="\n") 
        power_on_nodes(vm_uuid)    
    time.sleep(15)
    get_url = "https://{0}:9440/api/nutanix/v3/vms/{1}".format(PC_IP_ADDRESS, vm_uuid)
    res = requests.get(url=get_url, auth=auth, headers=header, verify=False)
    if res.json().get('spec').get('resources').get('power_state') == "ON":
        print("{0} is powered on successfully". format(vm_name), end="\n")




