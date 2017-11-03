# Groom Helm chart

## Install

### Prerequisites

-  A `Kubernetes` cluster with `kubectl` configured

- `Helm` must be installed and configured on your local machine and
  `tiller` daemon must be running on the cluster.
  You can see [Here](https://github.com/kubernetes/helm/blob/master/docs/install.md)
  how to setup both of these components.


### Install

```sh
git clone https://github.com/Xide/groom.git
cd groom
helm install ./chart
```
