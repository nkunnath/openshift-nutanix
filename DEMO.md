This describes a demo workflow.

Open variables.py and update the values as required.

```
python3 openshift-installer.py --create_cluster_definition
```
```
A new OpenShift cluster spec is created with name ntnx and ID b4579228-3b86-4e6f-94d7-1b1663ef62cb
Creating the boot image
Boot image created. Please copy it to the Terraform file and create the nodes.

The download URI is: 
https://s3.us-east-1.amazonaws.com/assisted-installer/discovery-image-b4579228-3b86-4e6f-94d7-1b1663ef62cb.iso?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA52ZYGBOVI2P2TOEQ%2F20210930%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20210930T073101Z&X-Amz-Expires=14400&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3Bfilename%3Ddiscovery-image-b4579228-3b86-4e6f-94d7-1b1663ef62cb.iso&X-Amz-Signature=2090dd7b411b1aa34ad4b41b80e0b619c4f9b3ad861fb090d392f5756c794280
```
<br/><br/>

Copy the download URI to the `terraform.tfvars` file. Update the other Prism Central variables as well.
Now apply the Terraform config. This will upload the discovery ISO boot image and create six nodes, three masters and three workers which are required at a minimum.
  
```
cd terraform 
terraform init
terraform apply
.
.
Apply complete! Resources: 7 added, 0 changed, 0 destroyed.
```
<br/><br/>

Kick off the cluster creation.

```
python3 openshift-installer.py --install_cluster b4579228-3b86-4e6f-94d7-1b1663ef62cb
```
<br/><br/>
Monitor the creation and get the current status of the hosts with the `--get_cluster_status` argument. Once the hosts boot up, the agent running on each host contacts the [Assisted Service](https://github.com/openshift/assisted-service) via REST API and performs discovery.
The hosts should be able to resolve api.openshift.com for the agent service to run.




Once all the network validations are done and hosts are ready to install, it should look as below.

```
watch -n 5 python3 openshift-installer.py --get_cluster_status b4579228-3b86-4e6f-94d7-1b1663ef62cb 
```
```
Cluster status: Cluster is not ready for install

Cluster installation progress details: {}

The sequence of stages during installation are as follows:
                "Starting installation",
                "Installing",
                "Writing image to disk",
                "Rebooting",
                "Configuring",
                "Joined",
                "Done"

Host status is:

openshift-worker2: Host is ready to be installed
Host installation progress details: {
    "current_stage": "",
    "stage_started_at": "0001-01-01T00:00:00.000Z",
    "stage_updated_at": "0001-01-01T00:00:00.000Z"
}

openshift-worker1: Host is ready to be installed
Host installation progress details: {
    "current_stage": "",
    "stage_started_at": "0001-01-01T00:00:00.000Z",
    "stage_updated_at": "0001-01-01T00:00:00.000Z"
}

openshift-master3: Host is ready to be installed
Host installation progress details: {
    "current_stage": "",
    "stage_started_at": "0001-01-01T00:00:00.000Z",
    "stage_updated_at": "0001-01-01T00:00:00.000Z"
}

openshift-worker3: Host is ready to be installed
Host installation progress details: {
    "current_stage": "",
    "stage_started_at": "0001-01-01T00:00:00.000Z",
    "stage_updated_at": "0001-01-01T00:00:00.000Z"
}

openshift-master1: Host is ready to be installed
Host installation progress details: {
    "current_stage": "",
    "stage_started_at": "0001-01-01T00:00:00.000Z",
    "stage_updated_at": "0001-01-01T00:00:00.000Z"
}

openshift-master2: Host is ready to be installed
Host installation progress details: {
    "current_stage": "",
    "stage_started_at": "0001-01-01T00:00:00.000Z",
    "stage_updated_at": "0001-01-01T00:00:00.000Z"

```
<br/><br/>
Initiate cluster creation. This will display the progress on the terminal.

```
python3 openshift-installer.py --install_cluster b4579228-3b86-4e6f-94d7-1b1663ef62cb
```
```
Cluster status: Preparing cluster for installation

Cluster installation progress details: {}

The stages during installation are as follows:
            "Starting installation",
            "Installing",
            "Writing image to disk",
            "Rebooting",
            "Configuring",
            "Joined",
            "Done"
            
openshift-worker1: Host is preparing for installation
Host installation progress details: {
    "current_stage": "",
    "stage_started_at": "0001-01-01T00:00:00.000Z",
    "stage_updated_at": "0001-01-01T00:00:00.000Z"
}

openshift-master2: Host is preparing for installation
Host installation progress details: {
    "current_stage": "",
    "stage_started_at": "0001-01-01T00:00:00.000Z",
    "stage_updated_at": "0001-01-01T00:00:00.000Z"
}

openshift-worker3: Host is preparing for installation
Host installation progress details: {
    "current_stage": "",
    "stage_started_at": "0001-01-01T00:00:00.000Z",
    "stage_updated_at": "0001-01-01T00:00:00.000Z"
}

openshift-worker2: Host is preparing for installation
Host installation progress details: {
    "current_stage": "",
    "stage_started_at": "0001-01-01T00:00:00.000Z",
    "stage_updated_at": "0001-01-01T00:00:00.000Z"
}

openshift-master1: Host is preparing for installation
Host installation progress details: {
    "current_stage": "",
    "stage_started_at": "0001-01-01T00:00:00.000Z",
    "stage_updated_at": "0001-01-01T00:00:00.000Z"
}

openshift-master3: Host is preparing for installation
Host installation progress details: {
    "current_stage": "",
    "stage_started_at": "0001-01-01T00:00:00.000Z",
    "stage_updated_at": "0001-01-01T00:00:00.000Z"
}
.
.
.
.
.
.
.
.
############### Checking progress after 10 seconds ###############

Cluster status: Cluster is installed

Cluster installation progress details: {
    "finalizing_stage_percentage": 100,
    "installing_stage_percentage": 100,
    "preparing_for_installation_stage_percentage": 100,
    "total_percentage": 100
}

The stages during installation are as follows:
            "Starting installation",
            "Installing",
            "Writing image to disk",
            "Rebooting",
            "Configuring",
            "Joined",
            "Done"
            
openshift-worker3: Done
openshift-worker2: Done
openshift-master3: Done
openshift-master1: Done
openshift-master2: Done
openshift-worker1: Done
############### Checking progress after 10 seconds ###############

Cluster is installed. Login to the console.
Hint: Run python3 openshift-installer.py --get_credentials b4579228-3b86-4e6f-94d7-1b1663ef62cb
```
<br/><br/>
You can get the credentials to the cluster and login to the console.

```
python3 openshift-installer.py --get_credentials b4579228-3b86-4e6f-94d7-1b1663ef62cb
```

```
{
    "console_url": "https://console-openshift-console.apps.ntnx.openshift.local",
    "password": "PpX56-2TSCB-x3vUB-8AjdJ",
    "username": "kubeadmin"
}

        Add the following to your local machine's /etc/hosts file.

        10.63.19.122	api.ntnx.openshift.local
        10.63.19.123	oauth-openshift.apps.ntnx.openshift.local
        10.63.19.123	console-openshift-console.apps.ntnx.openshift.local
        10.63.19.123	grafana-openshift-monitoring.apps.ntnx.openshift.local
        10.63.19.123	thanos-querier-openshift-monitoring.apps.ntnx.openshift.local
        10.63.19.123	prometheus-k8s-openshift-monitoring.apps.ntnx.openshift.local
        10.63.19.123	alertmanager-main-openshift-monitoring.apps.ntnx.openshift.local
       
```
