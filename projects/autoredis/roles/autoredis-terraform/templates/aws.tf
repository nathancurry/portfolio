terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "local" {}

provider "aws" {
  profile = "default"
  region  = "us-east-1"
  
}

resource "aws_instance" "node" {
  count                  = "{{ cluster_node_count }}"
  ami                    = "{{ aws_instance_ami }}"
  instance_type          = "{{ aws_instance_type }}"
  vpc_security_group_ids = [ "{{ aws_security_group }}" ]
  key_name               = "{{ aws_key_name }}"
  tags = {
    Name  = "{{ aws_node_name }}-${count.index +1}"
    Owner = "{{ aws_owner_tag }}"
    autoredis = ""
  }
}

resource "local_file" "{{ deployment_name }}_inventory"{
  content = templatefile("inventory_template",
    {
     hostname = aws_instance.node.*.tags.Name
     private_ip = aws_instance.node.*.private_ip
     ansible_user = "{{ aws_host_login }}"
     count = "{{ cluster_node_count }}"
     quorum_node = "{{ cluster_quorum_node }}"
     cluster_name = "{{ cluster_name }}"
    }
  )
  filename = "inventory"
}


output "private_ips" {
  value = "${aws_instance.node.*.private_ip}"
}

output "node_names" {
  value = "${aws_instance.node.*.tags.Name}"
}
