This describes a demo workflow.


```
python3 openshift-installer.py --create_cluster_definition

A new OpenShift cluster spec is created with name ntnx and ID b4579228-3b86-4e6f-94d7-1b1663ef62cb
Creating the boot image
Boot image created. Please copy it to the Terraform file and create the nodes.

The download URI is: 
https://s3.us-east-1.amazonaws.com/assisted-installer/discovery-image-b4579228-3b86-4e6f-94d7-1b1663ef62cb.iso?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA52ZYGBOVI2P2TOEQ%2F20210930%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20210930T073101Z&X-Amz-Expires=14400&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3Bfilename%3Ddiscovery-image-b4579228-3b86-4e6f-94d7-1b1663ef62cb.iso&X-Amz-Signature=2090dd7b411b1aa34ad4b41b80e0b619c4f9b3ad861fb090d392f5756c794280
```


Copy the download URI to the `terraform.tfvars` file. Update the other Prism Central variables as well.
Now apply the Terraform config. This will upload the discovery ISO boot image and create six nodes, three masters and three workers which are required at a minimum.
  
```
cd terraform 
terraform init
terraform apply

Apply complete! Resources: 7 added, 0 changed, 0 destroyed.
```


Monitor the creation and get the current status of the hosts with the `--get_cluster_status` argument. Once the hosts boot up, the agent running on each host contacts the [Assisted Service] (https://github.com/openshift/assisted-service) via REST API and performs discovery.
The hosts should be able to resolve api.openshift.com for the agent service to run.


Once all the network validations are done and hosts are ready to install, it should look as below.

```
watch -n 5 python3 openshift-installer.py --get_cluster_status b4579228-3b86-4e6f-94d7-1b1663ef62cb 


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

Initiate cluster creation.

```
python3 openshift-installer.py --install_cluster b4579228-3b86-4e6f-94d7-1b1663ef62cb
```


