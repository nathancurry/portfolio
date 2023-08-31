#!/bin/bash
export ANSIBLE_LOG_PATH="./logs/ansible-$(date +%Y%m%d).log"

# set absolute path, or relative to $autoredis_directory
export deployment_base="deployments"

eval `ssh-agent` &>/dev/null
trap "ssh-agent -k &>/dev/null" exit &>/dev/null

if [ ! -d "${deployment_base}/common/keys" ]; then
  mkdir -p "${deployment_base}/common/keys"
  chmod 750 "${deployment_base}/common/keys"
  echo "Please add private keys to 'deployments/common/keys' directory and set permissions 600" 
  exit 2
elif [ $(ls "${deployment_base}/common/keys" | wc -l) -eq 0 ]; then
  echo "Please add private keys ending in '.pem' to \"${deployment_base}/common/keys\" directory and set permissions 600"
  exit 2
else
  for i in "${deployment_base}/common/keys/*.pem"; do
    chmod 600 $i
    ssh-add $i
  done
fi


usage () {
cat <<END_USAGE

Usage:
  autoredis <deployment_name> [create|info|all] | [terraform|dns|cluster] ...

1. Run './autoredis <deployment> create' to create a deployment directory
   and vars file at "${deployment_base}/<deployment>".
2. Edit your credentials at "${deployment_base}/common/vars.yml" and place your
   private key in pem format in ".${deployment_base}/common/keys"
3. Run autoredis with the following options:

DEPLOYMENT MANAGEMENT:
  create:   Create deployment directory and deployment vars file
  info:     Show deployment info
  list:     List deployments
TERRAFORM:
  init:     Generate terraform template and run 'terraform init'
  apply:    Run 'terraform apply'"
  destroy:  Destroy cluster and DNS, retaining deployment directory
DNS:
  dns:         create DNS entries
  dns-delete:  delete DNS entries
CLUSTER:
  firstboot: update and reboot nodes, prepare files
  install:   software installation tasks
  config:    apply cluster configuration
ALL:
  terraform: terraform init + apply
  cluster:   all cluster tasks 
  all:       terraform + dns + cluster

END_USAGE
}

list_deployments() {
deployment_list=`find ${deployment_base} -maxdepth 1 -type d | grep -vE "^${deployment_base}\$|common"`
red='\033[1;31m'
green='\033[0;32m'
yellow='\033[1;33m'
blue="\033[1;34m"
gray="\033[1;30m"
nc='\033[0m'

echo -e "$(
cat << END_COMMENT

${blue}USER INFO
---------${nc}
User Tag: `niet aws_owner_tag ${deployment_base}/common/vars.yml`
Keypair:  `niet aws_key_name ${deployment_base}/common/vars.yml`

${blue}DEPLOYMENTS
-----------${nc}
END_COMMENT
)"
for i in $deployment_list; do
  deployment_name=`niet deployment_name $i/vars.yml`
  if test -s $i/inventory; then
    tf=${green}yes
    title_color=${green}
  else
    tf=${yellow}no
    title_color=${red}
  fi
  test  "$(niet deploy_ready $i/vars.yml)" == "True" && ready=${green}yes || ready=${yellow}no 
  test -s $i/create_A_results.json && dns=${green}yes || dns=${yellow}no
  printf "${title_color}${deployment_name}:${nc} `niet cluster_node_count $i/vars.yml` nodes, `niet redis_version $i/vars.yml`-`niet redis_build $i/vars.yml` on `niet redis_distro $i/vars.yml`\n"
  printf "  Ready: ${ready}${nc} Terraform: ${tf}${nc}  DNS: ${dns}${nc}\n\n"
done
}

if [ "$1 " == "list " ]; then
  list_deployments
  exit 0
fi

if [ $# -ne 2 ]; then
  usage
  exit 1 
fi

deployment_name="$1"
deployment_directory="${deployment_base}/${deployment_name}"

case $2 in
  create)
    echo "ansible-playbook site.yml -e deployment_name=$deployment_name -t create"
    ansible-playbook create.yml -e deployment_name=$deployment_name
    ;;
  init)
    echo "ansible-playbook site.yml -e @${deployment_directory}/vars.yml -t init"
    ansible-playbook site.yml -e @deployments/${deployment_name}/vars.yml -t init
    ;;
  apply)
    echo "ansible-playbook site.yml -e @${deployment_directory}/vars.yml -t apply"
    ansible-playbook site.yml -e @${deployment_directory}/vars.yml -t apply
    ;;
  destroy)
    echo "ansible-playbook site.yml -e @${deployment_directory}/vars.yml -t destroy"
    ansible-playbook site.yml -e @${deployment_directory}/vars.yml -t destroy
    ;;
  info)
    echo "ansible-playbook site.yml -e @${deployment_directory}/vars.yml -i ${deployment_directory}/inventory -t info"
    ansible-playbook site.yml -e @${deployment_directory}/vars.yml -i ${deployment_directory}/inventory -t info
    ;;
  all)
    echo "ansible-playbook site.yml -e @${deployment_directory}/vars.yml -i ${deployment_directory}/inventory -t all"
    ansible-playbook site.yml -e @${deployment_directory}/vars.yml -i ${deployment_directory}/inventory -t all 
    ;;
  terraform)
    echo "ansible-playbook site.yml -e @${deployment_directory}/vars.yml -i ${deployment_directory}/inventory -t init -t apply"
    ansible-playbook site.yml -e @${deployment_directory}/vars.yml -i ${deployment_directory}/inventory -t init -t apply 
    ;;
  dns)
    echo "ansible-playbook site.yml -e @${deployment_directory}/vars.yml -i ${deployment_directory}/inventory -t dns"
    ansible-playbook site.yml -e @${deployment_directory}/vars.yml -i ${deployment_directory}/inventory -t dns
    ;;
  dns-delete)
    echo "ansible-playbook site.yml -e @${deployment_directory}/vars.yml -i ${deployment_directory}/inventory -t dns-delete"
    ansible-playbook site.yml -e @${deployment_directory}/vars.yml -i ${deployment_directory}/inventory -t dns-delete
    ;;
  firstboot)
    echo "ansible-playbook site.yml -e @${deployment_directory}/vars.yml -i ${deployment_directory}/inventory -t firstboot"
    ansible-playbook site.yml -e @${deployment_directory}/vars.yml -i ${deployment_directory}/inventory -t firstboot
    ;;
  install)
    echo "ansible-playbook site.yml -e @${deployment_directory}/vars.yml -i ${deployment_directory}/inventory -t install"
    ansible-playbook site.yml -e @${deployment_directory}/vars.yml -i ${deployment_directory}/inventory -t install
    ;;
  config)
    echo "ansible-playbook site.yml -e @${deployment_directory}/vars.yml -i ${deployment_directory}/inventory -t config"
    ansible-playbook site.yml -e @${deployment_directory}/vars.yml -i ${deployment_directory}/inventory -t config
    ;;
  cluster)
    echo "ansible-playbook site.yml -e @${deployment_directory}/vars.yml -i ${deployment_directory}/inventory -t cluster"
    ansible-playbook site.yml -e @${deployment_directory}/vars.yml -i ${deployment_directory}/inventory -t cluster
    ;;
  list)
    list_deployments
    ;;
  *)
    usage
    ;;
esac

exit 0
