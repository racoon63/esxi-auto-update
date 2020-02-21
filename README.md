# esxi-auto-update

Update your standalone VMware ESXi from external automatically. Collects versions from [here](https://esxi-patches.v-front.de/ESXi-6.7.0.html) and runs the `esxi-update.yaml` ansible playbook. When the update fails and a `no space left on device` message appears, the auto-update tries to solve this issue by installing the VMware locker tools light.

## Disclaimer

This tool does no backup your ESXi VMs, configs or else!

## Docker

To get the latest version of the VMware ESXi updates, you can just use my docker image `racoon/esxi-version`:

```bash
docker run --rm racoon/esxi-version
```
