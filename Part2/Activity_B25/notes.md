# B25 - Design and Implement a Threat Intelligence Module of Your Choice

**Date:** 17 April, 2026

## Summary
This activity involves designing and implementing a threat intelligence module that can be used to gather and analyze cybersecurity threat data. I created a Python script that queries public threat intelligence feeds and APIs to collect information about malicious IP addresses, domains, and file hashes, and then presents the data in a readable report format.

## Implementation Details

### What is Threat Intelligence
Threat intelligence is information about current and potential cyber threats that helps organisations understand, prevent, and respond to cyberattacks. Threat intelligence feeds provide real-time data about known malicious indicators of compromise (IOCs) such as malicious IP addresses, domain names, URLs, and file hashes that are associated with cyberattacks.

### The Module I Built
I built a Python script that takes an indicator of compromise as input, such as an IP address, domain name, or file hash, and queries multiple public threat intelligence sources to gather information about it. The script uses the following free APIs and feeds: VirusTotal API for checking if an IP address, domain, or file hash is flagged as malicious. AbuseIPDB API for checking if an IP address has been reported for malicious activity. URLhaus API for checking if a URL or domain is associated with malware distribution.

### How It Works
The user provides an IOC to the script, and it queries each threat intelligence source and compiles the results into a single report. The report includes the risk score from each source, the types of malicious activity associated with the IOC, the number of times it has been reported, and when it was first and last seen. The script outputs the report both to the terminal and to a JSON file for further analysis.

### Testing and Results
I tested the module with several known malicious indicators and confirmed that the script correctly identified them as threats. I also tested it with legitimate IP addresses and domains to check for false positives, and the script correctly showed clean results for safe indicators. The module demonstrates how threat intelligence can be automated and integrated into security workflows to help analysts quickly assess whether an indicator is malicious without having to manually check each source individually. The code was uploaded to my GitHub repository.
