# OpenShift variables
OPENSHIFT_VERSION = "4.12.0-rc.1"                                                     
NAME = "phx186-ocp-delta-ai"        # OCP cluster name                                                           
OCP_RELEASE_IMAGE = "quay.io/openshift-release-dev/ocp-release:4.12.0-rc.1-x86_64" 
DNS_DOMAIN = "domain"               # Domain                                
CLUSTER_NETWORK_CIDR =  "10.128.0.0/14"
CLUSTER_NETWORK_HOST_PREFIX = 23
SERVICE_NETWORK_CIDR = "172.30.0.0/16"
HOST_NETWORKS = "10.38.186.0/25"                                                 
API_VIP = "10.38.186.140"                                                        
INGRESS_VIP = "10.38.186.141"                                                   


# SSH key of local host that can be used for troubleshooting during installation
CLUSTER_SSH_KEY = ""

# Your OpenShift Cluster Manager account tokens
# Default validity of OFFLINE_ACCESS_TOKEN is 24 hours
PULL_SECRET = ''                    # Fetch from https://console.redhat.com/openshift/downloads
OFFLINE_ACCESS_TOKEN = ""           # Fetch from https://console.redhat.com/openshift/downloads

# Nutanix Prism Central variables
PC_IP_ADDRESS = "10.38.186.39"                                                  
PC_USERNAME = "admin"                                                           
PC_PASSWORD = "xxx"                                                    
