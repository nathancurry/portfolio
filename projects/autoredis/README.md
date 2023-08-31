# autoredis (beta)

Dockerized Redis Enterprise cluster automation with Ansible and Terraform

## NOTES

- This has a bit of hardcoding that puts it in us-east-1, as was the requirement at the time.
- AMI and VPC needs updated.
- Note the missing DNS module which was designed for a private DNS server.  Just add DNS records per Redis Enterprise docs

## Installation

You can either run in a docker container, or in a virtual env.

### Docker Install

At present you need to either [run docker rootless](https://docs.docker.com/engine/security/rootless/), or deal with docker creating files with root ownership.

1. Build from `docker/Dockerfile`


    ```bash
    cd docker
    docker build . -t autoredis
    ```

    **NOTE:** It's possible to add AWS credentials to the docker image but this is not preferred.  If you do, copy out the docker directory before editing, to avoid pushing your credentials to github.

2. Add an alias and run to see instructions:

    ```bash
    alias autoredis='docker run --rm -it --name autoredis -v /path/to/home/.aws/:/root/.aws -v /path/to/cloned/git/autoredis/:/autoredis autoredis'  # put in your .bashrc
    # podman:
    # alias autoredis='podman run --privileged --rm -it --name autoredis -v /path/to/home/.aws/:/root/.aws -v /path/to/cloned/git/autoredis/:/autoredis autoredis'
    autoredis
    ```
    - The `-it` switch allows you to send a Ctrl+C to cancel if necessary.
    - The `--rm` switch removes the container on termination, so you don't accumulate dead containers

### Docker advanced install

The current config mounts the autoredis working directory for maximum transparency. You can package as much of it as you want into the docker container by using COPY to place the files and folders in `/autoredis` in the container.

The only directories you definitely should keep outside the container and mount at runtime are `projects` (templates, terraform state, and private keys) and `logs`.

### Local install

Add AWS credentials to your environment, either through the `.aws/credentials` file or environment variables.

1. Set up venv

    ```bash
    python -m venv venv   # if you change this path, edit the top of the autoredis script accordingly
    . venv/bin/activate
    pip install -r requirements.txt
    ```

  After installing the virtual env, you don't need to source the venv when using the autoredis script, only if running ansible-playbook directly.

2. Run autoredis.sh


## Currently supported options

- Install cluster of n nodes
- Quorum only node (node:1/master)
- Distro: Ubuntu 18.04, 16.04, RHEL7 (CentOS), RHEL8 (Rocky)

  **NOTE:** RHEL installs take longer to reboot, and while I've conditionally set the pause timer longer for RHEL7 and RHEL8, they still occasionally fail.

## Usage

Run autoredis to see usage:

```yaml
Usage: Run './autoredis.sh <deployment> create' to create a deployment directory
         and vars file at ./deployments/<deployment>/
       Please edit your credentials at ./deployments/common/vars.yml and place
         your private key in pem format in ./deployments/common/keys
       Edit the vars.yml file in that directory with your credentials and 
         cluster criteria, then run './autoredis.sh <deployment> all'
       The process can be broken down further with the following commands:


autoredis.sh <deployment_name> [create|info] | [all] | [terraform|dns|cluster] | [init|apply|destroy|firstboot|install|config]

DEPLOYMENT MANAGEMENT:
  create:   create deployment directory and deployment vars file
            ## you must edit the deployment vars file before proceeding ##

  info:     Output deployment info
  delete:   NOT IMPLEMENTED, DELETE THINGS YOURSELF

TERRAFORM: 
  init:     generate terraform template and run 'terraform init'
  apply:    run 'terraform apply'
  destroy:  destroy cluster and DNS, retaining deployment directory

# DNS BROKEN
# DNS:
#  dns:         create DNS entries
#  dns-delete:  delete DNS entries

CLUSTER: 
  firstboot: update and reboot nodes, prepare files
  install:   software installation tasks
  config:    apply cluster configuration

ALL:
  terraform: terraform init + apply
  cluster:   all cluster tasks 
  all:       terraform + cluster
```

### Quickstart

The quickest way to deploy a cluster:

```bash
autoredis new_project create 
vim projects/new_project/vars.yml
autoredis new_project all
## ALL runs terraform (init, apply) > [add_hosts] > dns > cluster (firstboot, install, config)
```
**NOTE:** If `all` fails when first connecting to the cluster, you need to extend `pause_duration` in the project vars.yml file to extend the wait period during the add_hosts task


### Detailed install workflow

This is the full workflow, see `Quickstart` below for the fast spin-up

1. Create a project

    ```bash
    autoredis new_project create
    ```

    This will create:
    - If necessary, common vars at deployments/common/vars.yml
    - A project folder at deployments/new_project
    - A vars file at projects/new_project/vars.yml

2. Add your owner tag and aws key to `deployments/common/vars.yml`

   ```yaml
   # aws_owner_tag:  # Identify your resources within your org
   # aws_key_name: "keyname" # keypair name on AWS. Place key at deployments/keys/<key>.pem
   ```

3. Edit `deployments/new_project/vars.yml` and then set deploy_ready: true


    ```yaml
    #####################
    ### REQUIRED VARS ###
    #####################

    deployment_name: new_project

    # LOCK
    # Set this to "true" once you've filled out this top section
    deploy_ready: true

    # Node ID and access
    aws_owner_tag: "nathan.curry" # 
    aws_key_name: "nathancurry" # keypair name on AWS

    # Cluster credentials
    cluster_username: "demo@example.com"
    cluster_password: "demo"

    # Cluster FQDN
    cluster_name: "{{ deployment_name }}"
    cluster_domain: lab.example.com
    cluster_fqdn: "{{ cluster_name }}.{{ cluster_domain }}"

    # AWS tags
    aws_node_name: "{{ deployment_name }}"

    ### CLUSTER CUSTOMIZATION ###
    #############################
    cluster_node_count: 3
    cluster_quorum_node: yes

    ### SOFTWARE VERSION ###
    ########################
    # The values below render 6.2.8-39
    redis_version: "6.2.8"
    redis_build: "39"
    redis_distro: bionic # bionic, xenial, rhel7, rhel8
    ```

4. Place your private key in `projects/keys`

   Autoredis will set necessary permissions on this directory and files in the directory, and will add any files as SSH keys to a subshell-constrained instance of ssh-agent.

5. Run Terraform init

   ```bash
   autoredis new_project init
   ```

   This will generate, based on your vars:
   - projects/new_project/main.tf
   
   It will also copy the inventory template that Terraform will use to generate your inventory

   After you've run this step, you can apply and destroy either through autoredis or using terraform directly, and don't need to run autoredis init again.

6. Run Terraform apply

   ```bash
   autoredis new_project apply
   ```

   This will run `terraform apply`, generating the file at projects/new_project/inventory

7. Add DNS

   ```bash
   autoredis new_project dns
   ```

   This will run add DNS entries for your cluster


8. Run cluster firstboot

   ```bash
   autoredis new_project firstboot
   ```   

   This updates packages, applies node customization (will be based on OS), reboots, and installs a lockfile to prevent a repeat.

9. Run cluster install

   ```bash
   autoredis new_project install
   ```

   This downloads and installs the Redis software. For now, this is static.  No lockfile is created, but it uses the install log to skip tasks.

10. Run cluster config

   ```bash
   autoredis new_project config
   ```

   This runs rladmin tasks to create and configure the cluster, and creates a lockfile to prevent a repeat.

## LICENSE

Steal anything you want from this, just give credit (attribute with links)
