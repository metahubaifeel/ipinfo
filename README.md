# ipinfo

A tiny CLI that tells you where an IP address lives.

Made by Coco. Quick geolocation, no fluff.

## Install

```bash
pip install -e .
```

## Usage

```bash
# Look up a public IP
$ ipinfo 8.8.8.8
Country : United States
City    : Mountain View
ISP     : Google LLC
Timezone: America/Chicago

# Try a different one
$ ipinfo 1.1.1.1
Country : Australia
City    : Sydney
ISP     : Cloudflare, Inc.
Timezone: Australia/Sydney

# Invalid input? You'll know
$ ipinfo not-an-ip
Error: 'not-an-ip' is not a valid IP address.

# Private IPs are valid too
$ ipinfo 192.168.1.1
Country : N/A
City    : N/A
ISP     : N/A
Timezone: N/A
```
