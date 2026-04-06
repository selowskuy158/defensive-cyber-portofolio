# B17 - Implement One of the Current State-of-the-Art Solutions and Evaluate It

**Date:** 13 April, 2026

## Summary
This activity involves implementing one of the state-of-the-art cybersecurity solutions I surveyed in Activity B16 and evaluating its effectiveness. I chose to implement a basic Zero Trust access control model on my home network using a combination of network segmentation and device authentication to demonstrate the principles of Zero Trust architecture in a small-scale environment.

## Implementation Details

### What I Implemented
I set up a basic Zero Trust model on my home network by configuring my router to create separate network segments for different types of devices, and implementing device-level authentication rules. The idea behind Zero Trust is that no device should be trusted by default, even if it is connected to the home network.

### Steps Taken
First, I created three separate VLANs on my router: one for trusted personal devices like my laptop and phone, one for IoT devices like the smart speaker and doorbell camera, and one for guest devices. Each VLAN has its own subnet and devices on different VLANs cannot communicate with each other by default. Second, I configured MAC address filtering on the trusted network so that only my registered devices can connect to it. Third, I enabled logging on the router to track all connection attempts and identify any unauthorized devices trying to join the network.

### Evaluation
After running the setup for two weeks, I evaluated the effectiveness of this basic Zero Trust implementation. The network segmentation successfully isolated IoT devices from my personal devices, meaning that even if the smart speaker or doorbell camera was compromised, the attacker would not be able to access my laptop or phone on the trusted network. The MAC address filtering added an extra layer of device authentication, although I acknowledged that MAC addresses can be spoofed by sophisticated attackers. The logging feature helped me identify two unknown devices that had tried to connect to my WiFi network during the testing period, which I was able to block immediately.

### Conclusion
While my home implementation is a simplified version of enterprise Zero Trust, it effectively demonstrated the core principles of the architecture: network segmentation, device verification, and continuous monitoring. The main limitation is that a home router does not have the same capabilities as enterprise Zero Trust platforms, but the fundamental concepts can still be applied to improve home network security significantly.
