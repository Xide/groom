# Roadmap
---



<!-- - Core services:
  - [ ] HTTP gate
  - [ ] provisionner
  - [ ] Instances API -->
- [ ] Allow hardware provisionning using [Terraform](https://github.com/hashicorp/terraform)
- [ ] Allow provisionning using [Ansible](https://github.com/ansible/ansible).


!!! warning
    Ansible will be much slower to provision ephemeral instances than `packer`, as
    by design it operate at runtime, and have to execute for each instance creation. When possible, the usage
    of whatever + `packer` is advised, as this technique allow you to provision your image ahead of time.


- [ ] Allow application provisionning with a [Packer](https://github.com/hashicorp/packer) image.
