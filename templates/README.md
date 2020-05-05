# Cuckoo nest and guest deployment role

This role deploys a cuckoo host (nest) and guest (or guests, since this role has autoscaling in aws configured) in AWS

## Prerequisites

* Snapshot of your guest filesystem in AWS
* AMI of your guest in AWS 
* Security group of your guest in AWS

### System Requirements

* RHEL 7.x EC2 instance with the EPEL repo configured (cuckoo nest server)
* Windows guest (requires python 2.7 and the agent.py from cuckoo to reside in the startup folder: https://cuckoo.sh/docs/installation/guest/index.html)

### Role Dependencies

 _None_ 

## Usage

This role deploys an instance of cuckoo with an api server, a django webserver, and cuckoo running as a systemd service (this service is responsible for task delegation and scaling)

### Required Variables


Do note that vars can come from multiple places: group_vars, extra_vars, inline (example playbook).  Subsequent documentation on how roles can be used in playbooks can be found in the [Ansible Documentation On Roles](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html).

```yaml
---
  - aws_access_key: ""
  - aws_secret_key: ""
  - cuckoo_resultserver_ip: "<your cuckoo private ip>"
  - cuckoo_systemd_svc_file: "cuckoo.service"
  - virt_platform: "aws"
  #### aws autoscaling config
  - aws_autoscale: "yes"
  - aws_running_machines_gap: "5"
  - aws_dynamic_machines_limit: "10"
  - aws_image_id: ""
  - aws_instance_type: "t2.medium"
  - aws_subnet_id: ""
  - aws_security_groups: ""
  - aws_platform: "windows"
  #### django web vars
  - mongodb_user: "cuckoo"
  - mongodb_password: "redhat"
  - mongodb_admin_user: "admin"
  - mongodb_admin_password: "admin"
  - mongodb_admin_database: "admin"
  - mongodb_database: "cuckoo"
  - deploy_django_web: "True"
  #### api server vars
  - api_server_port: "8090"
  - deploy_api_server: "True"
```

### Example Playbook

```yaml
---
- name: deploy cuckoo
  hosts: <your cuckoo public ip>
  remote_user: ec2-user
  become: true
  become_user: root
  vars:
  - aws_access_key: ""
  - aws_secret_key: ""
  - cuckoo_resultserver_ip: "<your cuckoo private ip>"
  - cuckoo_systemd_svc_file: "cuckoo.service"
  - virt_platform: "aws"
  #### aws autoscaling config
  - aws_autoscale: "yes"
  - aws_running_machines_gap: "5"
  - aws_dynamic_machines_limit: "10"
  - aws_image_id: ""
  - aws_instance_type: "t2.medium"
  - aws_subnet_id: ""
  - aws_security_groups: ""
  - aws_platform: "windows"
  #### django web vars
  - mongodb_user: "cuckoo"
  - mongodb_password: "redhat"
  - mongodb_admin_user: "admin"
  - mongodb_admin_password: "admin"
  - mongodb_admin_database: "admin"
  - mongodb_database: "cuckoo"
  - deploy_django_web: "True"
  #### api server vars
  - api_server_port: "8090"
  - deploy_api_server: "True"
  roles:
  - role: '/your/role/path/cuckoo_deploy_role'
```

## Variable Options


Variable Name | Type | Required | Default | Notes
--- | --- | --- | --- | ---
aws_access_key | String | yes | "" | access key generated in aws (https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html)
aws_secret_key | String | yes | "" | secret access key generated in aws (https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html)
cuckoo_resultserver_ip | String | yes | "" | public ip of your cuckoo nest server
cuckoo_systemd_svc_file | String | yes | "cuckoo.service"| used to create a systemd service to start/stop/restart cuckoo
virt_platform | String | yes | "aws" | the 'machinery' type to be used by cuckoo; this code base only works with aws currently
aws_autoscale | String | yes | "yes" | needs to be set to yes to enable autoscaling of guests for analysis 
aws_running_machines_gap | String | yes | "5" | the minimum number of guests that need to be running when cuckoo is started
aws_dynamic_machines_limit | String | yes | "10" | the maximum number of guests that cuckoo will attempt to spin up concurrently 
aws_image_id | String | yes | "" | the ami of your guest image
aws_instance_type | String | yes | "t2.medium" | ec2 instance size for your guest images
aws_subnet_id | String | yes | "" | subet id of your vpc in aws
aws_security_groups | String Array | yes | "" | comma separated list of security groups to attach to the dynamic guests
aws_platform | String | yes | "windows" | guest operating system
mongodb_admin_user | String | yes | "admin" | mongo db admin user 
mongodb_admin_password | String | yes | "admin" | mongo db admin password
mongodb_admin_database | String | yes | "admin" | mongo db admin database
mongodb_user | String | yes | "cuckoo" | mongo db user used by the django frontend to connect to the db on the cuckoo nest server
mongodb_password | String | yes | "redhat" | mongo db password used by the django frontend to connect to the db on the cuckoo nest server
mongodb_database | String | yes | "cuckoo" | mongo db database used by the django frontend to connect to the db on the cuckoo nest server
api_server_port | String | yes | "8090" | port used by the cuckoo api server
deploy_api_server | Boolean | yes | "True" | used to conditionally include the api server code

## Installation

When installing roles from the command line, please keep in mind that roles can be installed to the `roles-path` directories as definied by your `ansible.cfg`.  Alternatively, you can tell them to install in your directory for your next module.

### Manual Installation

To install in a defined path:

```bash
ansible-galaxy install ssh://git@gitlab.consulting.redhat.com:2222/DHS/DOMino/ansible-role-cuckoo-deploy.git
```

Or, to install in the directory of your Ansible code:

```bash
ansible-galaxy install --roles-path ./roles/ ssh://git@gitlab.consulting.redhat.com:2222/DHS/DOMino/ansible-role-cuckoo-deploy.git
```

### Requirements.yml Installation

Role and installation can also be defined in a file (which is subseqnetly used in Ansible Tower):

```yaml
# from GitLab or other git-based scm
- src: ssh://git@gitlab.consulting.redhat.com:2222/DHS/DOMino/ansible-role-cuckoo-deploy.git
  scm: git
```

There are other ways to configure your `requirements.yml` file.  You may reference them [here](https://docs.ansible.com/ansible/latest/galaxy/user_guide.html#install-multiple-collections-with-a-requirements-file).

Installation of the requirements can now be completed with the following.

```bash
ansible-galaxy install -r requirements.yml
```

## Authors

Author - [kritchie@redhat.com]

## License

BSD


