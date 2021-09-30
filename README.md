# OpenShift on Nutanix


## Introduction
 OpenShift assisted installer method on Nutanix from CLI. This leverages REST API's from [OpenShift](https://generator.swagger.io/?url=https://raw.githubusercontent.com/openshift/assisted-service/master/swagger.yaml) and [Nutanix Prism Central](https://www.nutanix.dev/reference/prism_central/v3/).


## Pre-requisites


1. Nutanix
* AOS: 5.20 or later
* AHV: 20201105.1045 or later
* Prism Central: pc.2021.8 or later
* VLAN network with AHV IPAM configured



2. OpenShift

* DHCP for the OCP nodes
* DNS server. There must be three DNS entries already configured, two for the API VIP (VIP to use for internal API communication) and Ingress VIP (VIP to use for Ingress traffic). In each record, <cluster_name> is the cluster name and <base_domain> is the cluster base domain. It must be similar to the entries shown below.

```
api.<cluster-name>.<base_domain>		         IN  A           <api_vip_ip_address>
api-int.<cluster-name>.<base_domain>		         IN  A	         <api_vip_ip_address>
*.apps.<cluster-name>.<base_domain>		         IN  A	         <ingress_vip_ip_address>
```

* Reserve the two IP addresses for API VIP and Ingress VIP in DHCP. If you are using Nutanix IPAM/DHCP (as in the demo below), you can reserve it from a CVM - `acli net.add_to_ip_blacklist <network_name> ip_list=ip_address1,ip_address2`



3. Terraform must be installed 

4. python3


## Usage

```
git clone https://github.com/nkunnath/openshift-nutanix.git
```

```
python3 openshift-installer.py -h                                                                              
usage: 
    There are 5 choices to run the script.
    python openshift-installer.py --list_of_ocp_clusters
    python openshift-installer.py --create_cluster_definition
    python openshift-installer.py --get_cluster_status <cluster_uuid>
    python openshift-installer.py --install_cluster <cluster_uuid>
    python openshift-installer.py --get_credentials <cluster_uuid>
    

OpenShift assisted installer on Nutanix

optional arguments:
  -h, --help            show this help message and exit
  --list_of_ocp_clusters
                        Retrieves all OpenShift clusters created by the account
  --create_cluster_definition
                        Create a new OpenShift cluster definition
  --get_cluster_status GET_CLUSTER_STATUS
                        Retrieves the details of a OpenShift cluster.
  --install_cluster INSTALL_CLUSTER
                        Installs the OpenShift cluster.
  --get_credentials GET_CREDENTIALS
                        Retrieves the cluster admin credentials for a cluster

```

A demo workflow is shown in [DEMO.md](DEMO.md)


After the OpenShift installation is over, login to the console and install the [Nutanix CSI Operator](https://www.nutanix.dev/2021/09/29/fast-tracking-persistent-storage-in-openshift/).
