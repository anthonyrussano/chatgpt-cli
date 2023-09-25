# How to Use `lsusb` to List USB Devices

`lsusb` is a command-line utility that provides information about USB devices connected to your system. In this tutorial, we will go through some basic examples on how to use `lsusb`.

## Prerequisites

Before we begin, make sure you have `lsusb` installed on your system. The command is usually available on Linux distributions by default. If it's not installed, you can install it using the package manager of your distribution.

## Usage

To use `lsusb`, open your terminal and run the following command:

```bash
lsusb
```

This command will list all the USB devices connected to your system. Here is an example output:

```
Bus 001 Device 006: ID 8087:0a2b Intel Corp.
Bus 001 Device 004: ID 0781:5580 SanDisk Corp.
Bus 001 Device 003: ID 046d:c31d Logitech, Inc. Keyboard K120
Bus 001 Device 002: ID 1a40:0101 Terminus Technology Inc. Hub
Bus 001 Device 005: ID 046d:c077 Logitech, Inc. M105 Optical Mouse
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```

Each line in the output represents a USB device. Here is the breakdown of the information provided:

- `Bus`: Represents the USB bus number.
- `Device`: Represents the device number connected to the bus.
- `ID`: Represents the vendor and product IDs of the device.
- `Description`: Represents the vendor and product description of the device.

You can also use additional options with `lsusb` to get more specific information. Here are some examples:

### Verbose Output

To get a more detailed output including the USB device classes, run the following command:

```bash
lsusb -v
```

This will provide comprehensive information about each USB device connected to your system.

### Suppressed Summary Output

To suppress the summary output and only display information about USB devices connected to the system, use the `-t` option:

```bash
lsusb -t
```

This option is useful when you want to focus on the device tree structure.

### Search by Vendor or Product ID

You can search for USB devices using their vendor or product ID. For example, to find devices with vendor ID `046d`, run the following command:

```bash
lsusb -d 046d:
```

To find devices with product ID `c077`, run the following command:

```bash
lsusb -d :c077
```

## Conclusion

Congratulations! You now have a basic understanding of how to use `lsusb` to list USB devices on your system. The provided examples should help you get started, and you can explore additional options and features of `lsusb` based on your requirements.