#!/bin/bash

path='deployments'
common_dir="$path/common"

deployment_list=`find $path -maxdepth 1 -type d | grep -vE "^$path\$|common"`

red='\033[0;31m'
green='\033[0;32'
nc='\033[0m'

cat << END_COMMENT
USER INFO
---------
User Tag: `niet aws_owner_tag $common_dir/vars.yml`
Keypair:  `niet aws_key_name $common_dir/vars.yml`

DEPLOYMENTS
-----------
END_COMMENT
for i in $deployment_list; do
  if [ -s $i/inventory.ini ]; then
    color=$green
  else
    color=$red
  fi
  printf "${color}`niet deployment_name $i/vars.yml`:${nc} `niet cluster_node_count $i/vars.yml` nodes, `niet redis_version $i/vars.yml`-`niet redis_build $i/vars.yml` on `niet redis_distro $i/vars.yml`\n"
  printf "  Terraform: ${color}`test -f inventory.ini && echo yes || echo no`${nc}  DNS: `test -f *.json && echo ${green}yes || echo ${red}no`${nc}\n\n"
done

