# B23 - Test an Intrusion Detection System and Discuss Its Effectiveness

**Date:** 16 April, 2026

## Summary
This activity involves setting up, testing, and evaluating the effectiveness of an intrusion detection system (IDS). I installed and configured Snort, which is one of the most popular open-source network intrusion detection systems, on a virtual machine running Ubuntu and tested it by simulating different types of network attacks to see how well it detects and alerts on suspicious traffic.

## Implementation Details

### Setting Up Snort
I installed Snort 3 on an Ubuntu virtual machine running on my laptop using VirtualBox. I configured Snort to monitor network traffic on the virtual network interface and loaded the community ruleset which contains signatures for thousands of known attack patterns. I also configured Snort to log alerts to a text file and set up the output to display alerts in real time on the terminal so I could see detections as they happened.

### Testing the IDS

#### Test 1: Port Scanning Detection
I used Nmap from a separate virtual machine to perform a port scan against the machine running Snort. Snort successfully detected the port scan and generated multiple alerts identifying the scanning activity, including the source IP address, destination ports being scanned, and the type of scan being performed. The alerts were generated within seconds of the scan starting, showing that Snort is very responsive to this type of reconnaissance activity.

#### Test 2: Ping Sweep Detection
I performed a ping sweep across the virtual network to simulate network discovery activity. Snort detected the ICMP traffic and generated alerts for the excessive ping activity, correctly identifying it as potential network reconnaissance. This showed that Snort can detect even simple network enumeration techniques.

#### Test 3: Simulated SQL Injection Attempt
I sent HTTP requests containing SQL injection payloads to a test web server running on the Snort machine. Snort detected the SQL injection attempts in the HTTP traffic and generated alerts with the specific SQL injection patterns that triggered the detection rules. This demonstrated that Snort can inspect application-layer traffic and identify web application attacks.

### Evaluation of Effectiveness
Snort proved to be very effective at detecting known attack patterns that match its ruleset. However, I also identified some limitations. Snort can generate false positives when legitimate traffic matches attack signatures, which requires careful tuning of the rules. Also, Snort is a signature-based IDS, meaning it can only detect attacks that match known patterns in its ruleset and may miss novel or zero-day attacks that have no existing signature. Despite these limitations, Snort is a very powerful tool for network security monitoring and is widely used by organisations around the world as part of their defence-in-depth strategy.
