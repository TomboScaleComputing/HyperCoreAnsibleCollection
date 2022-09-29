# Ansible Collection for Scale Computing HyperCore

The Ansible Collection for Scale Computing HyperCore ([HyperCore](https://www.scalecomputing.com/sc-hypercore))
a variety of Ansible content to help automate the management of Scale Computing HyperCore products.


<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.12**.

The collection should work with any Ansible version **>=2.9.10**,
but this is not granted.
<!--end requires_ansible-->

## Python version compatibility

This collection requires Python 3.8 or greater.

## HyperCore cluster API version compatibility

This collection has been tested against HyperCore cluster API version v9.1.14.208456.

## Included content

### Inventory plugins

Name | Description
--- | ---
scale_computing.hypercore.hypercore | Inventory source to list HyperCore Virtual Machines.

### Modules

Module name | Description
--- | ---
scale_computing.hypercore.vm | Create, update or delete a virtual machine.
scale_computing.hypercore.vm_info | Get information about existing virtual machines.
scale_computing.hypercore.vm_params | Partialy update a virtual machine. Use when changing some of the properties of an existing VM.
scale_computing.hypercore.vm_disk | Update block devices on VM.
scale_computing.hypercore.vm_nic | Update network interfaces (NICs) on a VM.
scale_computing.hypercore.vm_boot_devices | Set up a boot order for the specified VM.
scale_computing.hypercore.vm_node_affinity | Set up node affinity for a specified VM.
scale_computing.hypercore.node_info | Get the list of all nodes on a cluster. Needed to set node affinities for VMs.
scale_computing.hypercore.remote_cluster_info | Get Information regarding remote replication clusters.
scale_computing.hypercore.vm_replication | Configure a VM replication.
scale_computing.hypercore.vm_replication_info | Get a VM replication configuration.
scale_computing.hypercore.snapshot_schedule | Configure a snapshot schedule.
scale_computing.hypercore.snapshot_schedule_info | Get the existing list of snapshot schedules.
scale_computing.hypercore.iso | Upload a new ISO image, or edit an existing one.
scale_computing.hypercore.iso_info | Get a list of available ISO images.
scale_computing.hypercore.api | Use to directly access to HyperCore API.
scale_computing.hypercore.vm_export | Export a VM to an SMB server.
scale_computing.hypercore.vm_import | Import a VM from an SMB or an HTTP URI.
scale_computing.hypercore.vm_clone | Clone a VM.

# Examples

The [examples](https://github.com/ScaleComputing/HyperCoreAnsibleCollection/tree/main/examples)
subdirectory contains usage examples for individual modules.
Look at [examples/README.md](https://github.com/ScaleComputing/HyperCoreAnsibleCollection/tree/main/examples/README.md) to see how to use each example.

# Development

See [DEVELOPMENT.md](https://github.com/ScaleComputing/HyperCoreAnsibleCollection/tree/main/DEVELOPMENT.md).
