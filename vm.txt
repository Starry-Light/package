AIM: 
To set up virtual instances, load balancing, server consolidation, and fault tolerance to 
optimize resource use and ensure high availability in a cloud environment. 
PROCEDURE: 
Part 1: Virtual Instances Management 
Task 1: Create and Configure Virtual Instances 
1. Open VMware Workstation Pro 17: 
○ Start VMware Workstation and open the existing Ubuntu 24.04.1 LTS VM. 
2. Clone Virtual Instances (VMs): 
○ Since we already have one Ubuntu VM, we can create additional VMs by cloning. 
○ Right-click on the existing Ubuntu VM and select Manage > Clone. 
○ In the cloning wizard, select Create a full clone to make identical copies of VM. 
○ Clone as many VMs as needed (e.g., two or three additional VMs). 
  
 
 
3. Power On the Cloned VMs: 
○ Power on the newly cloned VMs by right-clicking on each & select Power On. 
 
○ Once powered on, open the terminal in each VM. 
  
 
 
4. Install Apache Web Server on Each VM: 
 
For each VM, install Apache using the following commands: sudo apt update 
 
sudo apt install apache2 -y 
 
  
Enable Apache: sudo systemctl enable apache2 
 
Verify Apache is running: sudo systemctl status apache2 
 
You can modify the Apache default web page to make it unique for each instance: 
sudo nano /var/www/html/index.html 
 
After customizing html template -> Ctrl O + Enter + Ctrl X 
 
5. Configure Networking: ifconfig 
 
  
 
 
 
OUTPUT: 
 
 
 
Task 2: Implement Basic Load Balancing 
1. Install and Configure HAProxy on a Separate VM (Load Balancer): 
○ You can use a separate VM to act as the load balancer or install HAProxy on one 
of your VMs. 
Install HAProxy using the following command: sudo apt install haproxy -y 
2. Configure HAProxy: 
Open the HAProxy configuration file: sudo nano /etc/haproxy/haproxy.cfg 
Add the following configuration to set up load balancing among your VMs: 
frontend http_front 
bind *:80 
default_backend http_back 
backend http_back 
balance roundrobin 
server vm1 <VM1_IP>:80 check 
server vm2 <VM2_IP>:80 check 
server vm3 <VM3_IP>:80 check 
  
 
 
 
3. Start HAProxy Service: 
 
After configuring HAProxy, restart the service to apply changes: sudo systemctl restart haproxy 
 
sudo systemctl enable haproxy 
 
sudo systemctl status haproxy 
 
 
4. Test the Load Balancer: http://<load_balancer_IP> 
 
OUTPUT: 
 
http://192.168.119.128 
Part 2: Server Consolidation 
Task 1: Implement Server Consolidation Strategy 
1. Open VMware Workstation and Identify VMs: 
○ Launch VMware Workstation and review all VMs by opening each VM’s 
configuration to check its resource allocations. 
○ List VMs with low usage or redundant workloads that could be consolidated. 
2. Select a Consolidation Host: 
○ Choose a host VM with sufficient CPU, memory, and storage to accommodate the 
combined workloads. 
3. Adjust Resources for Each VM: 
○ Open each VM setting by selecting the VM in VMware Workstation, clicking Edit 
virtual machine settings, and adjusting Memory and Processor values to optimize 
the combined workload. 
○ Avoid over-provisioning to ensure balanced performance. 
4. Migrate Services to a Consolidated VM: 
○ For each VM to be consolidated, copy files and services to the target consolidated 
VM. 
○ Start the services on the consolidated VM and confirm they are running as 
expected. 
5. Power Off and Decommission Unused VMs: 
○ After successfully migrating services, power off the original VMs to ensure the 
services are fully operational on the consolidated VM. 
○ Delete unused VMs by right-clicking the VM in VMware Workstation and 
selecting Remove. 
6. Validate Resource Utilization on the Consolidated VM: 
○ Check the resource usage (CPU, Memory) by accessing the Performance Monitor 
(for Windows) or using tools like top or htop (for Linux). 
○ Verify that the consolidated VM can handle the load without performance 
degradation. 
Part 3: Fault Tolerance 
Task 1: Implement Fault-Tolerant Design 
1. Create Redundant VM Copies for High Availability: 
○ For critical services, create a clone of the primary VM by selecting the VM in 
VMware Workstation, going to VM > Manage > Clone, and choosing Full Clone 
to make a complete backup. 
2. Set Up Data Synchronization: 
For Linux, use rsync to sync files between primary and backup VMs by running a 
command like: rsync -av /source_directory/ user@backup_vm_ip:/destination_directory 
3. Enable Snapshots for Quick Recovery: 
○ In VMware Workstation, select a critical VM, go to VM > Snapshot > Take 
Snapshot, and give it a name (e.g., “Pre-Consolidation Snapshot”). 
○ Take snapshots before major updates or configurations to quickly revert if needed. 
RESULT: 
Virtual instances with load balancing, server consolidation, and fault tolerance were 
successfully deployed, optimizing performance and ensuring service continuity. 
UIT2702 - Cloud and Distributed Computing 
Exercise 6: Task Scheduling and Load Balancing in a Cloud Environment 
AIM: 
To automate task scheduling and implement load balancing in a cloud environment for 
efficient resource management and high availability. 
PROCEDURE: 
Part 1: Task Scheduling 
Task 1: Implement Task Scheduling with Cloud Services 
1. Open VMware Workstation Pro 17: 
○ Power on the VMs (e.g., UbuntuSelcia). 
2. Configure Task Scheduling on Ubuntu VMs: 
○ We will use cron to schedule tasks, which is the Linux utility for task scheduling. 
3. Create a Task in Ubuntu VM: 
Create a script file using: nano script.sh 
Add: echo “Hello Selcia” 
Open the cron file using the command: crontab -e 
Add a scheduled task (for example, to run a script every 1 minute): */1 * * * * ./script.sh >> 
./output.log 
4. Verify the Task: 
○ Check if the task is running by checking the output of the script or inspecting 
logs, if any: tail -f /var/log/syslog | grep CRON 