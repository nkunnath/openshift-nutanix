terraform {
  required_providers {
    nutanix = {
      source  = "nutanix/nutanix"
      version = "1.2.0"
    }
  }
}

data "nutanix_cluster" "cluster" {
  name = var.cluster_name
}

data "nutanix_subnet" "subnet" {
  subnet_name = var.subnet_name
}




provider "nutanix" {
  username     = var.user
  password     = var.password
  endpoint     = var.endpoint
  insecure     = true
  wait_timeout = 60
}

resource "nutanix_image" "dcos" {
  name        = "OpenShift Discovery ISO"
  description = "OpenShift boot image"
  image_type  = "ISO_IMAGE"
  source_uri  = var.source_uri
}


resource "nutanix_virtual_machine" "Master1" {
  name                 = "openshift-master1"
  cluster_uuid         = data.nutanix_cluster.cluster.id
  num_vcpus_per_socket = "8"
  num_sockets          = "1"
  memory_size_mib      = "20480"
  boot_device_order_list = ["DISK", "CDROM"]

  disk_list {
    data_source_reference = {
      kind = "image"
      uuid = nutanix_image.dcos.id
    }
  }

  disk_list {
    disk_size_bytes = 120 * 1024 * 1024 * 1024
    device_properties {
      device_type = "DISK"
      disk_address = {
        "adapter_type" = "SCSI"
        "device_index" = "1"
      }
    }
  }
  nic_list {
    subnet_uuid = data.nutanix_subnet.subnet.id
  }
}



resource "nutanix_virtual_machine" "Master2" {
  name                 = "openshift-master2"
  cluster_uuid         = data.nutanix_cluster.cluster.id
  num_vcpus_per_socket = "8"
  num_sockets          = "1"
  memory_size_mib      = "20480"
  boot_device_order_list = ["DISK", "CDROM"]

  disk_list {
    data_source_reference = {
      kind = "image"
      uuid = nutanix_image.dcos.id 
    }
  }

  disk_list {
    disk_size_bytes = 120 * 1024 * 1024 * 1024
    device_properties {
      device_type = "DISK"
      disk_address = {
        "adapter_type" = "SCSI"
        "device_index" = "1"
      }
    }
  }
  nic_list {
    subnet_uuid = data.nutanix_subnet.subnet.id
  }
}

resource "nutanix_virtual_machine" "Master3" {
  name                 = "openshift-master3"
  cluster_uuid         = data.nutanix_cluster.cluster.id
  num_vcpus_per_socket = "8"
  num_sockets          = "1"
  memory_size_mib      = "20480"
  boot_device_order_list = ["DISK", "CDROM"]
  
  disk_list {
    data_source_reference = {
      kind = "image"
      uuid = nutanix_image.dcos.id 
    }
  }

  disk_list {
    disk_size_bytes = 120 * 1024 * 1024 * 1024
    device_properties {
      device_type = "DISK"
      disk_address = {
        "adapter_type" = "SCSI"
        "device_index" = "1"
      }
    }
  }
  nic_list {
    subnet_uuid = data.nutanix_subnet.subnet.id
  }
}

resource "nutanix_virtual_machine" "Worker1" {
  name                 = "openshift-worker1"
  cluster_uuid         = data.nutanix_cluster.cluster.id
  num_vcpus_per_socket = "4"
  num_sockets          = "1"
  memory_size_mib      = "10240"
  boot_device_order_list = ["DISK", "CDROM"]

  disk_list {
    data_source_reference = {
      kind = "image"
      uuid = nutanix_image.dcos.id 
    }
  }

  disk_list {
    disk_size_bytes = 120 * 1024 * 1024 * 1024
    device_properties {
      device_type = "DISK"
      disk_address = {
        "adapter_type" = "SCSI"
        "device_index" = "1"
      }
    }
  }
  nic_list {
    subnet_uuid = data.nutanix_subnet.subnet.id
  }
}


resource "nutanix_virtual_machine" "Worker2" {
  name                 = "openshift-worker2"
  cluster_uuid         = data.nutanix_cluster.cluster.id
  num_vcpus_per_socket = "4"
  num_sockets          = "1"
  memory_size_mib      = "10240"
  boot_device_order_list = ["DISK", "CDROM"]

  disk_list {
    data_source_reference = {
      kind = "image"
      uuid = nutanix_image.dcos.id 
    }
  }

  disk_list {
    disk_size_bytes = 120 * 1024 * 1024 * 1024
    device_properties {
      device_type = "DISK"
      disk_address = {
        "adapter_type" = "SCSI"
        "device_index" = "1"
      }
    }
  }
  nic_list {
    subnet_uuid = data.nutanix_subnet.subnet.id
  }
}


resource "nutanix_virtual_machine" "Worker3" {
  name                 = "openshift-worker3"
  cluster_uuid         = data.nutanix_cluster.cluster.id
  num_vcpus_per_socket = "4"
  num_sockets          = "1"
  memory_size_mib      = "10240"
  boot_device_order_list = ["DISK", "CDROM"]

  disk_list {
    data_source_reference = {
      kind = "image"
      uuid = nutanix_image.dcos.id 
    }
  }

  disk_list {
    disk_size_bytes = 120 * 1024 * 1024 * 1024
    device_properties {
      device_type = "DISK"
      disk_address = {
        "adapter_type" = "SCSI"
        "device_index" = "1"
      }
    }
  }
  nic_list {
    subnet_uuid = data.nutanix_subnet.subnet.id
  }
}


terraform {
  
}
