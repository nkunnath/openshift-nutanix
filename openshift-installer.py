import json
import sys
import time
import argparse
import requests
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import update_vm
import new_update_vm
from openshiftvar import *


def refresh_token():
    '''
    Bearer token that has to be refreshed every 15 minutes
    '''
    data_list = {
      "grant_type": "refresh_token",
      "client_id": "cloud-services",
      "refresh_token": OFFLINE_ACCESS_TOKEN
    }
    url = "https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token"
    res = requests.post(url=url, data=data_list)
    return res

TOKEN = refresh_token().json().get("access_token")

# global headers used in multiple API calls below
headers = {"Authorization": "Bearer " + TOKEN, "content-type": "application/json"}


def get_cluster():
    '''
    Retrieves the list of OpenShift clusters.
    '''
    url = "https://api.openshift.com/api/assisted-install/v1/clusters"
    res = requests.get(url=url, headers=headers)
    return res



def create_cluster_definition():
    '''
    Creates a new OpenShift cluster definition. This creates a cluster with vip_dhcp_allocation': True
    '''
    data_list = {
        "kind": "Cluster",
        "name": NAME,
        "openshift_version": OPENSHIFT_VERSION,
        "ocp_release_image": OCP_RELEASE_IMAGE,
        "base_dns_domain": DNS_DOMAIN,
        "hyperthreading": "all",
        "cluster_network_cidr": CLUSTER_NETWORK_CIDR,
        "cluster_network_host_prefix": CLUSTER_NETWORK_HOST_PREFIX,
        "service_network_cidr": SERVICE_NETWORK_CIDR,
        "host_networks": HOST_NETWORKS,
        "hosts": [],
        "high_availability_mode": "Full",
        "ssh_public_key": CLUSTER_SSH_KEY,
        "pull_secret": PULL_SECRET
    }
    url = "https://api.openshift.com/api/assisted-install/v1/clusters"
    res = requests.post(url=url, data=json.dumps(data_list), headers=headers)
    return res



def patch_cluster(cluster_uuid):
    '''
    Updates an OpenShift cluster definition. Here it updates the API VIP and Ingress VIP.
    '''
    data_list = {
        "api_vip": API_VIP,
        "ingress_vip": INGRESS_VIP,
        'vip_dhcp_allocation': False
    }
    url = "https://api.openshift.com/api/assisted-install/v1/clusters/{0}".format(cluster_uuid)
    res = requests.patch(url=url, data=json.dumps(data_list), headers=headers)
    return res




def create_image(cluster_uuid):
    '''
    Creates a new OpenShift per-cluster Discovery ISO.
    '''
    data_list = {
        "image_type": "full-iso",
        "pull_secret": PULL_SECRET,
        "ssh_public_key": CLUSTER_SSH_KEY
    }
    url = "https://api.openshift.com/api/assisted-install/v1/clusters/{0}/downloads/image".format(cluster_uuid)
    res = requests.post(url=url, data=json.dumps(data_list), headers=headers)
    return res



def create_cluster(cluster_uuid):
    '''
    Installs the OpenShift cluster.
    '''
    data_list = {}
    url = "https://api.openshift.com/api/assisted-install/v1/clusters/{0}/actions/install".format(cluster_uuid)
    res = requests.post(url=url, data=json.dumps(data_list), headers=headers)
    return res



def get_credentials(cluster_uuid):
    '''
    Get the cluster admin credentials.
    '''
    url = "https://api.openshift.com/api/assisted-install/v1/clusters/{0}/credentials".format(cluster_uuid)
    res = requests.get(url=url, headers=headers)
    return res



def get_cluster_details(cluster_uuid):
    '''
    Retrieves the details of a OpenShift cluster.
    '''
    TOKEN_NEW = refresh_token().json().get("access_token")
    headers_new = {"Authorization": "Bearer " + TOKEN_NEW, "content-type": "application/json"}
    url = "https://api.openshift.com/api/assisted-install/v1/clusters/{0}".format(cluster_uuid)
    res = requests.get(url=url, headers=headers_new, verify=False)
    cluster_info = res.json()
    host_info = []
    if cluster_info.get("hosts"):
        host_info = cluster_info.get("hosts")
    else:
        print("Hosts not available yet\n")
    return cluster_info,host_info



def progress_func(cluster_uuid):
    '''
    Displays the current installation progress
    '''
    while True:
        cluster_info, host_info = get_cluster_details(cluster_uuid)
        print("Cluster status: {0}".format(cluster_info.get("status_info")), end="\n\n")
        print("Cluster installation progress details: {0}".format(json.dumps(cluster_info.get("progress"), indent=4)), end="\n\n")
        print("""The stages during installation are as follows:
            "Starting installation",
            "Installing",
            "Writing image to disk",
            "Rebooting",
            "Configuring",
            "Joined",
            "Done"
            """)
        for item in host_info:
            print("{0}: {1}".format(item.get("requested_hostname"), item.get("status_info")), end="\n")
            if item.get("status_info") == "Done":
                continue
            print("Host installation progress details: {0}".format(json.dumps(item.get("progress"), indent=4)), end="\n\n")

            if "Expected the host to boot from disk, but it booted the installation image" in item.get("status_info"):
                new_update_vm.update_vm(item.get("requested_hostname"))
                print("Successfully updated {0}".format(item.get("requested_hostname")))
                time.sleep(15)

        print("############### Checking progress after 10 seconds ###############\n")
        time.sleep(10)
        if cluster_info.get("status_info") == "Cluster is installed":
           print("Cluster is installed. Login to the console.")
           print("Hint: Run python3 openshift-installer.py --get_credentials {0}".format(cluster_uuid))
           break




def main():
    parser = argparse.ArgumentParser(description='OpenShift installer on Nutanix', 
                                     usage='''
    There are 5 choices to run the script.
    python openshift-installer.py --list_of_ocp_clusters
    python openshift-installer.py --create_cluster_definition
    python openshift-installer.py --get_cluster_status <cluster_uuid>
    python openshift-installer.py --install_cluster <cluster_uuid>
    python openshift-installer.py --get_credentials <cluster_uuid>
    ''')
    parser.add_argument('--list_of_ocp_clusters', help='Retrieves all OpenShift clusters created by the account', action="store_true")
    parser.add_argument('--create_cluster_definition', help='Create a new OpenShift cluster definition', action="store_true")
    parser.add_argument('--get_cluster_status', type=str, help='Retrieves the details of a OpenShift cluster.')
    parser.add_argument('--install_cluster', type=str, help='Installs the OpenShift cluster.')
    parser.add_argument('--get_credentials', type=str, help='Retrieves the cluster admin credentials for a cluster')
    args = parser.parse_args()
    
    if args.create_cluster_definition:
        cluster = create_cluster_definition().json()
        print("A new OpenShift cluster spec is created with name {0} and ID {1}".format(cluster.get("name"), cluster.get("id")))
        print("Creating the boot image")
        image = create_image(cluster.get("id")).json()
        print("Boot image created. Please copy it to the Terraform file and create the nodes.\n")
        print("The download URI is: \n{0}".format(image.get("image_info").get('download_url')))

    if args.list_of_ocp_clusters:
        cluster = get_cluster().json()
        print("The OpenShift clusters are: ")
        for i in cluster:
            print("Cluster name: {0} and Cluster ID: {1}".format(i.get('name'), i.get("id")))

    if args.get_credentials:
        cluster = get_credentials(args.get_credentials).json()
        print(json.dumps(cluster, indent=4))
        print("""
        Add the following to your local machine's /etc/hosts file.

        {0}	api.ntnx.openshift.local
        {1}	oauth-openshift.apps.ntnx.openshift.local
        {1}	console-openshift-console.apps.ntnx.openshift.local
        {1}	grafana-openshift-monitoring.apps.ntnx.openshift.local
        {1}	thanos-querier-openshift-monitoring.apps.ntnx.openshift.local
        {1}	prometheus-k8s-openshift-monitoring.apps.ntnx.openshift.local
        {1}	alertmanager-main-openshift-monitoring.apps.ntnx.openshift.local
        """.format(API_VIP, INGRESS_VIP))

    if len(sys.argv) == 3:
        if args.get_cluster_status:
            cluster_info, host_info = get_cluster_details(args.get_cluster_status)
            print("Cluster status: {0}".format(cluster_info.get("status_info")), end="\n\n")
            print("Cluster installation progress details: {0}".format(json.dumps(cluster_info.get("progress"), indent=4)), end="\n\n")
            print("""The sequence of stages during installation are as follows:
                "Starting installation",
                "Installing",
                "Writing image to disk",
                "Rebooting",
                "Configuring",
                "Joined",
                "Done"
                """)
            print("Host status is:", end="\n\n")
            for item in host_info:
                print("{0}: {1}".format(item.get("requested_hostname"), item.get("status_info")))
                #print(item.get("requested_hostname"))
                print("Host installation progress details: {0}".format(json.dumps(item.get("progress"), indent=4)), end="\n\n")
                #print(json.dumps(item.get("progress"), indent=4), end="\n\n")
                #print(json.dumps(item, indent=4))
        elif args.install_cluster:
            patch_cluster(args.install_cluster)
            create_cluster(args.install_cluster)
            progress_func(args.install_cluster)
            #p = Process(target=func, args=("args.install_cluster"))
            #p.start()
            #p.join()
            
if __name__ == "__main__":
    main()


