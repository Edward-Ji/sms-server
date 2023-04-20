# SMS Server

Scripts for settings up a Linux server that forwards SMS.

## Setup

You need to have an Android phone and a Raspberry Pi (or some other Linux
device to use as server).

You need to figure out the IP address of your Raspberry Pi `addr` (e.g.
`192.168.1.100`) and device on a `port` for the server to bind to (e.g. `9090`).

### Android

On the Android phone, download [Android SMS Gateway Webhook] and install.

Press the plus icon and input:
- Sender: `*`
- Webhook URL: `http://<addr>:<port>`

See [How to use] for more information on the application.

### Raspberry Pi

Clone and `cd` into the repository. Install Python requirements with `python -m
pip install -r requirements.txt`.

Configure settings in `setttings.json`:
- `port`: the port you decided the server should bind to
- `number`: the mobile number of the Android device, this will be shown on the
  webpage

Inside `sms-server.service`, replace:
- `<user>` by your username (use `whoami`); and
- `<path>` by the path to the local repository (use `pwd`).

Run `./install` as `root` (e.g. `sudo ./install`). The script will add the SMS
server to `systemd`, enable and start the server.

## Usage

If you setup correctly, you should be able to access the messages at
`http://<addr>:<port>`.

If you want to access the Raspberry Pi outside the local network, you need to
setup static IP and port forwarding, or just use something like [PiVPN].

[How to use]: https://github.com/bogkonstantin/android_income_sms_gateway_webhook#how-to-use
[Android SMS Gateway Webhook]: https://github.com/bogkonstantin/android_income_sms_gateway_webhook/releases/latest
[PiVPN]: https://pivpn.io/
