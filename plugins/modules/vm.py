#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: vm

author:
  - Domen Dobnikar (@domen_dobnikar)
  - Tjaž Eržen (@tjazsch)
short_description: Create VM
description:
  - Module creates a new virtual machine alongside with disks, nics, boot order and cloud init data. After creation,
    the VM is also put into the specified power state.
version_added: 0.0.1
extends_documentation_fragment:
  - scale_computing.hypercore.cluster_instance
seealso: []
options:
  vm_name:
    description:
      - VM's name.
      - Serves as unique identifier across endpoint C(VirDomain).
    type: str
    required: True
  description:
    description:
      - VM's description.
    type: str
  memory:
    description:
      - VM's physical memory in bytes.
      - Required if C(state=present).
    type: int
  vcpu:
    description:
      - Number of Central processing units on the VM.
      - Required if C(state=present).
    type: int
  power_state:
    description:
      - VM's Desired power state.
      - If not specified, the VM will be running by default.
    choices: [ start, shutdown, stop, reboot, reset ]
    type: str
    default: start
  state:
    description:
      - Desired state of the VM.
    choices: [ present, absent ]
    type: str
    required: True
  tags:
    description:
      - Tags of the VM.
      - The first tag determines the group that the VM is going to belong.
    type: list
    elements: str
  disks:
    description:
      - List of disks we want to create.
      - Required if C(state=present).
    default: []
    suboptions:
      disk_slot:
        type: int
        description:
          - Virtual slot the drive will occupy.
        required: true
      size:
        type: int
        description:
          - Logical size of the device in bytes.
      type:
        type: str
        description:
          - The bus type the VM will use.
          - If C(type==ide_cdrom), it's assumed you want to attach ISO image to cdrom disk. In that
            case, field iso_name is required.
        choices: [ ide_cdrom, virtio_disk, ide_disk, scsi_disk, ide_floppy, nvram ]
        required: true
      iso_name:
        type: str
        description:
          - The name of the ISO image we want to attach to the CD-ROM.
          - Required if C(type==ide_cdrom)
          - Only relevant if C(type==ide_cdrom).
      cache_mode:
        type: str
        description:
          - The cache mode the VM will use.
        choices: [ none, writeback, writethrough ]
    type: list
    elements: dict
  nics:
    description:
      - List of network interfaces we want to create.
      - Required if C(state=present).
    type: list
    elements: dict
    default: []
    suboptions:
      vlan:
        type: int
        default: 0
        description:
          - Network interface virtual LAN.
      mac:
        type: str
        description:
          - Mac address of the network interface.
      type:
        type: str
        default: virtio
        description:
          - Defines type of the network interface.
        choices: [ virtio, RTL8139, INTEL_E1000 ]
      connected:
        type: bool
        default: true
        description:
          - Is network interface connected or not.
  boot_devices:
    description:
      - Ordered list of boot devices (disks and nics) you want to set
    type: list
    elements: dict
  attach_guest_tools_iso:
    description:
      - If supported by operating system, create an extra device to attach the Scale Guest OS tools ISO.
    default: false
    type: bool
  cloud_init:
    description:
      - Configuration to be used by cloud-init (Linux) or cloudbase-init (Windows).
      - When non-empty will create an extra ISO device attached to VirDomain as a NoCloud datasource.
      - Only relevant if C(state==present).
    type: dict
    suboptions:
      user_data:
        description:
          - Configuration user-data to be used by cloud-init (Linux) or cloudbase-init (Windows).
          - Valid YAML syntax.
        type: dict
      meta_data:
        type: dict
        description:
          - Configuration meta-data to be used by cloud-init (Linux) or cloudbase-init (Windows).
          - Valid YAML syntax.
"""

EXAMPLES = r"""
- name: Create and start the VM with disks, nics and boot devices set. Attach ISO onto the VM. Add cloud init data
  scale_computing.hypercore.vm:
    vm_name: vm-integration-test-vm
    description: Demo VM
    state: present
    tags:
      - my-group
      - mytag1
      - mytag2
    memory: "{{ '512 MB' | human_to_bytes }}"
    vcpu: 2
    attach_guest_tools_iso: true
    power_state: start
    disks:
      - type: virtio_disk
        disk_slot: 0
        size: "{{ '10.1 GB' | human_to_bytes }}"
      - type: ide_cdrom
        disk_slot: 0
        iso_name: TinyCore-current.iso
    nics:
      - vlan: 0
        type: RTL8139
    boot_devices:
      - type: virtio_disk
        disk_slot: 0
      - type: nic
        nic_vlan: 0
    cloud_init:
      user_data: |
        valid:
        - yaml: 1
        - expression: 2
      meta_data: "{{ lookup('file', 'cloud-init-user-data-example.yml') }}"
  register: result
"""

RETURN = r"""
record:
  description:
    - Created VM, if creating the record. If deleting the record, none is returned.
  returned: success
  type: list
  sample:
    vm_name: demo-vm
    description: demo-vm-description
    vcpu: 2
    power_state: stopped
    tags: group-name,tag1,tag2
    uuid: f0c91f97-cbfc-40f8-b918-ab77ae8ea7fb
    boot_devices:
      - cache_mode: none
        disable_snapshotting: false
        disk_slot: 2
        mount_points: []
        name: ""
        read_only: false
        size: 10737418240
        tiering_priority_factor: 8
        type: virtio_disk
        uuid: d48847d0-91b1-4edf-ab28-3be864494711
        vm_uuid: 183c5d7c-1e2e-4871-84e8-9ef35bfda5ca
    disks:
      - uuid: e8c8aa6b-1043-48a0-8407-2c432d705378
        vm_uuid: 1596dab1-6f90-494c-9607-b14221830433
        type: virtio_disk
        cache_mode: none
        size: 8100100100
        disk_slot: 0
        name: ""
        disable_snapshotting: false
        tiering_priority_factor: 8
        mount_points: []
        read_only: false
    nics:
      - uuid: 07a2a68a-0afa-4718-9c6f-00a39d08b67e
        vlan: 15
        type: virtio
        mac: 12-34-56-78-AB
        connected: true
        ipv4_addresses: []
    node_affinity:
      strict_affinity: true
      preferred_node:
        backplane_ip: "10.0.0.1"
        lan_ip: "10.0.0.2"
        peer_id: 1
        node_uuid: 638920f2-1069-42ed-b311-5368946f4aca
      backup_node:
        node_uuid: f6v3c6b3-99c6-475b-8e8e-9ae2587db5fc
        backplane_ip: 10.0.0.3
        lan_ip: 10.0.0.4
        peer_id: 2
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils import arguments, errors
from ..module_utils.client import Client
from ..module_utils.rest_client import RestClient
from ..module_utils.vm import VM
from ..module_utils.task_tag import TaskTag
from ..module_utils.errors import DeviceNotUnique


def ensure_absent(module, rest_client):
    vm = VM.get_by_name(module.params, rest_client)
    if vm:
        if vm.power_state != "shutdown":  # First, shut it off and then delete
            vm.update_vm_power_state(module, rest_client, "stop")
        # raise ValueError(vm.to_ansible())
        task_tag = rest_client.delete_record(
            "{0}/{1}".format("/rest/v1/VirDomain", vm.uuid), module.check_mode
        )
        TaskTag.wait_task(rest_client, task_tag)
        output = vm.to_ansible()
        return True, [output], dict(before=output, after=None)
    return False, [], dict()


def ensure_present(module, rest_client):
    vm_before = VM.get_by_name(module.params, rest_client)
    if vm_before:
        raise DeviceNotUnique("VM with name {0}".format(module.params["vm_name"]))
    new_vm = VM.from_ansible(module.params)
    task_tag = rest_client.create_record(
        "/rest/v1/VirDomain",
        new_vm.post_vm_payload(rest_client, module.params),
        module.check_mode,
    )
    TaskTag.wait_task(rest_client, task_tag)
    (
        vm_created,
        boot_devices_uuid_created,
        boot_deviced_created,
    ) = VM.get_vm_and_boot_devices(module.params, rest_client)
    if module.params["boot_devices"]:
        vm_created.set_boot_devices(
            module.params["boot_devices"],
            module,
            rest_client,
            boot_devices_uuid_created,
        )
    if module.params["power_state"] != "shutdown":
        vm_created.update_vm_power_state(
            module, rest_client, module.params["power_state"]
        )
    vm_after = VM.get_by_name(module.params, rest_client)
    after = vm_after.to_ansible()
    return True, [after], dict(before=None, after=after)


def run(module, rest_client):
    if module.params["state"] == "absent":
        return ensure_absent(module, rest_client)
    return ensure_present(module, rest_client)


def main():
    module = AnsibleModule(
        supports_check_mode=False,  # False ATM
        argument_spec=dict(
            arguments.get_spec("cluster_instance"),
            vm_name=dict(
                type="str",
                required=True,
            ),
            description=dict(
                type="str",
            ),
            memory=dict(
                type="int",
            ),
            vcpu=dict(
                type="int",
            ),
            power_state=dict(
                type="str",
                choices=[
                    "start",
                    "shutdown",
                    "stop",
                    "reboot",
                    "reset",
                ],
                default="start",
            ),
            state=dict(
                type="str",
                choices=[
                    "present",
                    "absent",
                ],
                required=True,
            ),
            tags=dict(type="list", elements="str"),
            disks=dict(
                type="list",
                elements="dict",
                options=dict(
                    disk_slot=dict(
                        type="int",
                        required=True,
                    ),
                    size=dict(
                        type="int",
                    ),
                    type=dict(
                        type="str",
                        choices=[
                            "ide_cdrom",
                            "virtio_disk",
                            "ide_disk",
                            "scsi_disk",
                            "ide_floppy",
                            "nvram",
                        ],
                        required=True,
                    ),
                    iso_name=dict(
                        type="str",
                    ),
                    cache_mode=dict(
                        type="str",
                        choices=["none", "writeback", "writethrough"],
                    ),
                ),
            ),
            nics=dict(
                type="list",
                elements="dict",
                options=dict(
                    vlan=dict(
                        type="int",
                        default=0,
                    ),
                    connected=dict(
                        type="bool",
                        default=True,
                    ),
                    type=dict(
                        type="str",
                        choices=[
                            "virtio",
                            "RTL8139",
                            "INTEL_E1000",
                        ],
                        default="virtio",
                    ),
                    mac=dict(
                        type="str",
                    ),
                ),
            ),
            boot_devices=dict(
                type="list",
                elements="dict",
            ),
            attach_guest_tools_iso=dict(type="bool", default=False),
            cloud_init=dict(
                type="dict",
                default={},
                options=dict(
                    user_data=dict(type="dict"),
                    meta_data=dict(type="dict"),
                ),
            ),
        ),
        required_if=[
            (
                "state",
                "present",
                (
                    "memory",
                    "vcpu",
                    "disks",
                    "nics",
                ),
                False,
            ),
        ],
    )

    try:
        host = module.params["cluster_instance"]["host"]
        username = module.params["cluster_instance"]["username"]
        password = module.params["cluster_instance"]["password"]
        client = Client(host, username, password)
        rest_client = RestClient(client)
        changed, record, diff = run(module, rest_client)
        module.exit_json(changed=changed, record=record, diff=diff)
    except errors.ScaleComputingError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
