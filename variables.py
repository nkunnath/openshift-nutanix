# OpenShift variables
OPENSHIFT_VERSION = "4.8.9"                                                     
NAME = "ntnx"                                                                   
OCP_RELEASE_IMAGE = "quay.io/openshift-release-dev/ocp-release:4.8.9-x86_64" 
DNS_DOMAIN = "openshift.local"                                                  
CLUSTER_NETWORK_CIDR =  "10.128.0.0/14"
CLUSTER_NETWORK_HOST_PREFIX = 23
SERVICE_NETWORK_CIDR = "172.30.0.0/16"
HOST_NETWORKS = "10.63.16.0/22"                                                 
API_VIP = "10.63.19.122"                                                        
INGRESS_VIP = "10.63.19.123"                                                   


# SSH ky of local host that can be used for troubleshooting during installation
CLUSTER_SSH_KEY = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDkYEGnmZrr6HAWr5VASaa0gvIBgKU2t6JovquKUSOJVW4XBSmpjVLdMw41eXxYz9v1u9fJ8ftGTHPQlG5tCmDyp8HVubdueT6lgJUZRD/qzx8b+p2ouyYC+rIsu8f5DFRXqW9W8g1NN7iM2nt5LhWJQjUixJW2EABto1Ho2a6XzhuE/ucrP+nZkmLn1FCvPbO+Ee1Er9E1CU8YEqj4db6LEaB0vJ5Y2XLyeXWtwXAVJ+X08D65BLXm+rcsP1UU0u3zSuP6zb3yEv+zrbCNc4t9rKS7PeGqwDIVyoHWBi31HTbfzhKZofGhjorJWJnl1pMPXSrq2206CJ07wQxFZNh9DTM463XZJR59n2MjEZEfK0L7wlz0UpIk0xWzNlBJakudMVKOzfMWJe8c8+nPuSN/0zF6Ylitiov3hBLu6myuId99wxWY+gvKpyMZNeE7Eunyz47DXmw0BsNM9C+nivP8bMlzunETtQmeQ4iwf1K9hBEiUTFZQmJjNDk3WWHv8nE= nimal.kunnath@C02C76CRMD6R"

# Your OpenShift Cluster Manager account tokens
# Default validity of OFFLINE_ACCESS_TOKEN is 24 hours
PULL_SECRET = ''
OFFLINE_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJhZDUyMjdhMy1iY2ZkLTRjZjAtYTdiNi0zOTk4MzVhMDg1NjYifQ.eyJpYXQiOjE2MzI5NTY5NDksImp0aSI6Ijg0NDk4ODE0LWM2OTItNDM2Ny1iNmJlLWJjYjY2ZjllZTJmYyIsImlzcyI6Imh0dHBzOi8vc3NvLnJlZGhhdC5jb20vYXV0aC9yZWFsbXMvcmVkaGF0LWV4dGVybmFsIiwiYXVkIjoiaHR0cHM6Ly9zc28ucmVkaGF0LmNvbS9hdXRoL3JlYWxtcy9yZWRoYXQtZXh0ZXJuYWwiLCJzdWIiOiJmOjUyOGQ3NmZmLWY3MDgtNDNlZC04Y2Q1LWZlMTZmNGZlMGNlNjpua3VubmF0aCIsInR5cCI6Ik9mZmxpbmUiLCJhenAiOiJjbG91ZC1zZXJ2aWNlcyIsIm5vbmNlIjoiMzU5MjhhOTMtNzJmMi00OGFmLTgwNGYtYzAyMjhiMGRkYWUyIiwic2Vzc2lvbl9zdGF0ZSI6IjQ3ZWJkOWFkLTU1ZTUtNDQ4NC1hNTk2LTMyNjBiY2NhNzFkZiIsInNjb3BlIjoib3BlbmlkIG9mZmxpbmVfYWNjZXNzIn0.wJDKleK9jdYkFSHAUElxzvEZR9-dNtLyPqAa8IfGU6I"

# Nutanix Prism Central variables
PC_IP_ADDRESS = "10.63.19.124"                                                  
PC_USERNAME = "admin"                                                           
PC_PASSWORD = "Nutanix/1234"                                                    
