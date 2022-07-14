# Drawer of Any Network Topology (DANT)
This is a demo repository for an automation tool, which collects the operational data from network devices using NETCONF/YANG and visualise it in the way you need.

## Discalaimer
This tool allows you provide insights how you can draw any network topology you need for any vendor as long as the following conditions are met:
- Network devices supports NETCONF/YANG
- You have access to YANG modules or knows how to retrieve them from a network device via NETCONF
- You have some Python knowledge

The provided demo builds physical network connectivity's topology between Cisco Nexus 9000 devices leveraging CDP and OSPF information. However, it can be easy extensible to draw any other topology.

## Frameworks used
- Nornir for managing interaction with devices in a threaded way
- NETCONF/YANG (using `scrapli_netconf`) for interacting with network devices
- `network` and `graphviz` for building math graph and visualisation

## Usage
1. Install Python dependencies:
```
$ pip install -r requirements.txt
```
2. Set the following environment variables:
```
$ export AUTOMATION_USERNAME='username_for_switches'
$ export AUTOMATION_PASSWORD='password_for_switches'
```
3. Update inventory in `app/inventory` per standard Nornir inventory pattern. You can integrate it with NetBox or another source of truth, if needed.
5. Check how to specify topology:
```
$ cd app
$ python main.py --help
```
4. Launch the script with arguments `--topology` to specify topology (e.g., OSPF or CDP) of choice and `--format` (e.g. static or dymamic):
```
$ python main.py --topology cdp --format static
```

## Supported
### Network Operating Systems
- Cisco NX-OS (tested with 9.3.9)
- Cisco IOS XR (testes with 7.2.1)
- Nokia SR OS (tested with 21.5.R1)

### Topologies
- CDP
- OSPF

### Visualisation
- `static` leverages Graphviz to create static PNG image.
- `dynamic` leverages VisJS/pyvis to create dynamic HTML pages.

# More details
This repository supports our blog [Karneliuk.com](https://karneliuk.com). Find the corresponding blogposts explaing these files.

# Want to Be The Automation Expert?
This is just a tiny example of what our students from [Zero-to-Hero Network Automation Training](https://training.karneliuk.com/forms/) can create to help them to do troubleshooting or real-time analysis. [Enroll to the training](https://training.karneliuk.com/forms/) today and start studying.

# Need Help?
[Contact us](https://karneliuk.com/contact/) with your request and we will find the most suitable solution for you.

(c)2022, Karneliuk.com