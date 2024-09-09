# Netbox to Obsidian

Python script to pull data from [Netbox](https://netboxlabs.com) and convert it to [Obsidian](https://obsidian.md) metadata Markdown-friendly format.

Some unneeded background:

I love using Obsidian's wikilink, and sometimes when writing daily notes I'll refer to a device that I need to manage/troubleshoot. This scripts help giving me more context to the devices, while also keeping it in sync with my infrastructure SSOT.

## Usage

### Install Requirements

```bash
py -m pip install -r requirements.txt
```

### Define URL and and API Token in .env

For example:

```bash
NETBOX_API_TOKEN=super-secret-token
NETBOX_URL=https://netbox.domain.tld
```

### Configure `config.yaml` as required

For example:

```yaml
---

config:

  - netbox_endpoint: "/api/dcim/devices"
    obsidian_template: "device.md.j2"
    obsidian_folder: "output/Devices"

  - netbox_endpoint: "/api/dcim/manufacturers"
    obsidian_template: "manufacturer.md.j2"
    obsidian_folder: "output/Manufacturers"

  - netbox_endpoint: "/api/dcim/device-roles"
    obsidian_template: "device_role.md.j2"
    obsidian_folder: "output/Device Roles"

  - netbox_endpoint: "/api/dcim/sites"
    obsidian_template: "site.md.j2"
    obsidian_folder: "output/Sites"

```

You can also add more Netbox models or modify templates as you want, just add/modify the file inside the `/templates` folder for the templates.

### Run the script

```bash
py ./netbox-to-obsidian.py
```

You can setup scheduler to run the script periodically.

## License

MIT, use at your own risk.
