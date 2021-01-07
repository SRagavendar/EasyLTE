#!/usr/bin/env python
import geni.portal as portal
import geni.rspec.pg as rspec
import geni.rspec.igext as IG
import geni.rspec.emulab.pnext as PN
import geni.urn as URN

Description = """

# srsLTE RF

Using this profile to instantiate an end-to-end LTE network in a controlled RF environment 
(Over-the-Air connection between UE and eNodeB). The UE can be srsLTE based UE or any COTS UE
like Xiaomi Poco X3.

If you decide to use a COTS UE, the following nodes will be deployed:

* COTS UE (`rue1`)
* Generic Compute Node w/ ADB image (`adbnode`)
* Dell Optiplex-3070/B205mini w/ srsLTE eNB/EPC (`enbepc`)

"""

Instructions = """

### Start EPC and eNodeB

After your setup becomes ready, login and do:

```
/home/ses002/EasyLTE/srsLTE/start.sh
```

This will start a 'tmux' session with three panes, running 'srsepc' and 'srsenb', and then
leaves your cursor in the last pane. After you've associated an UE with this eNB, you can use
the third pane to run tests with `ping` or `iperf` or even mirror the UE using `scrcpy`. If you
are not familiar with `tmux`, it's a terminal multiplexer that has some similarities to screen.
Here's a [tmux cheat sheet](https://tmuxcheatsheet.com), but `ctrl-b o` (move to another pane)
and `ctrl-b x` (kill pane) will be sufficient. `ctrl-b d` will detach from the `tmux` session
and leave it running in the background. You can reattach with `tmux attach`.

If you'd like to state `srsepc` and `srsenb` manually, here is how:

```
# Start srsepc
sudo srsepc /home/ses002/EasyLTE/srsLTE/config/epc.conf

# Start srsenb
sudo srsenb /home/ses002/EasyLTE/srsLTE/config/enb.conf
```

### COTS UE
If you've deployed a COTS UE, you should see it sync with the eNodeB eventually and obtain
an IP address. Check the phone using `scrcpy` to confirm

If the UE fails to sync with the eNodeB, try rebooting the device via `scrcpy` and after the
reboot, you'll have to repeat the `scrcpy` to reestablish a connection to the UE.00

"""

class GLOBALS(object):
	NUC_HWTYPE = "Optiplex-3070"
	COTS_UE_HWTYPE = "pocox3"
	UBUNTU_1804_IMG = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU18-64-STD"
	SRSLTE_IMG = "urn:publicid:IDN+emulab.net+image+PowderProfiles:U18LL-SRSLTE:1"
	COTS_UE_IMG = URN.Image(PN.PNDEFS.PNET_AM, "PhantomNet:ANDROID444-STD")
	ADB_IMG = URN.Image(PN.PNDEFS.PNET_AM, "PhantomNet:UBUNTU14-64-PNTOOLS")

pc = portal.Context()
pc.defineParameter("ue_type", "UE Type", portal.ParameterType.STRING, "pocox3",
					[("srsue", "srsLTE UE (B205mini)"), ("pocox3", "COTS UE (Poco X3)")],
					longDescription="Type of UE to deploy.")

pc.defineParameter("enb_node", "eNodeB Node ID",
					portal.ParameterType.STRING, "", advanced=True,
					longDescription="Specific eNodeB node to bind to.")

pc.defineParameter("ue_node", "UE Node ID",
					portal.ParameterType.STRING, "", advanced=True,
					longDescription="Specific UE node to bind to.")

params = pc.bindParameters()
pc.verifyParameters()
request = pc.makeRequestRSpec()

# Add a NUC eNB node
enbepc = request.RawPC("enbepc")
enbepc.component_id = params.enb_node
enbepc.hardware_type = GLOBALS.NUC_HWTYPE
enbepc.disk_image = GLOBALS.SRSLTE_IMG
enbepc.Desire("rf-controlled", 1)
enbepc_rue1_rf = enb1.addInterface("rue1_rf")
enbepc.addService(rspec.Execute(shell="bash", commands="/home/ses002/EasyLTE/srsLTE/tune-cpu.sh"))
enbepc.addService(rspec.Execute(shell="bash", commands="/home/ses002/EasyLTE/srsLTE/add-nat-and-ip-forwarding.sh"))

# Add a UE node
if params.ue_type == "pocox3":
	adbnode = request.RawPC("adbnode")
	adbnode.disk_image = GLOBALS.ADB_IMG
	rue1 = request.UE("rue1")
	rue1.hardware_type = GLOBALS.COTS_UE_HWTYPE
	rue1.disk_image = GLOBALS.COTS_UE_IMG
	rue1.adb_target = "adbnode"
elif params.ue_type == "srsue":
	rue1 = request.RawPC("rue1")
	rue1.hardware_type = GLOBALS.NUC_HWTYPE
	rue1.disk_image = GLOBALS.SRSLTE_IMG
	rue1.addService(rspec.Execute(shell="bash", command="/home/ses002/EasyLTE/srsLTE/tune-cpu.sh"))

rue1.component_id = params.ue_node
rue1.Desire("rf-controlled", 1)
rue1_enb1_rf = rue1.addInterface("enb1_rf")
