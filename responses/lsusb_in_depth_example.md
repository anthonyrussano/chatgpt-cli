# In-Depth Usage of `lsusb` Command

`lsusb` is a powerful command-line utility used to list USB devices connected to your system. In this tutorial, we will explore more in-depth examples of using `lsusb` and its various options.

## Prerequisites

Before we start, ensure that you have `lsusb` installed on your system. If it is not already installed, you can usually install it using your distribution's package manager.

## Usage

To begin, open your terminal and run the `lsusb` command:

```bash
lsusb
```

This will provide you with a list of USB devices connected to your system. Each line represents a separate USB device with the following information:

- `Bus`: The USB bus number on which the device is connected.
- `Device`: The device number on the bus.
- `ID`: The device's vendor and product IDs.
- `Description`: A brief description of the device.

### Verbose Output

For more detailed information about each USB device, use the `-v` option:

```bash
lsusb -v
```

This will display comprehensive output, including detailed information about each USB device, such as its class, protocol, and more.

### Bus Tree Output

To obtain a visual representation of the USB device tree, utilize the `-t` option:

```bash
lsusb -t
```

This will show the hierarchical structure of the USB devices connected to your system.

### Filtering by Vendor or Product ID

If you want to filter the output based on a specific vendor or product ID, you can use the `-d` option. Here are a couple of examples:

To list USB devices with a specific vendor ID, use the following command:

```bash
lsusb -d <vendor_id>
```

Replace `<vendor_id>` with the desired vendor ID. For instance, to filter by vendor ID `8086` (Intel Corp.), run:

```bash
lsusb -d 8086
```

To list USB devices with a specific product ID, use the following command:

```bash
lsusb -d :<product_id>
```

Replace `<product_id>` with the desired product ID. For example, to filter by product ID `1234`, execute:

```bash
lsusb -d :1234
```

You can combine the vendor and product IDs to filter the output further:

```bash
lsusb -d <vendor_id>:<product_id>
```

### Displaying USB Speed

To obtain the USB speed (e.g., Low-Speed, Full-Speed, High-Speed, SuperSpeed) of the connected devices, you can use the `-s` option:

```bash
lsusb -s <bus_number>:<device_number>
```

Replace `<bus_number>` and `<device_number>` with the corresponding values from the `Bus` and `Device` columns of the `lsusb` output. For example, to check the speed of Bus 001, Device 003, run:

```bash
lsusb -s 001:003
```

### Continuous Monitoring

If you want to continuously monitor changes in the USB device connections, you can use the `-watch` option:

```bash
lsusb -watch
```

This will continuously update the `lsusb` output, providing real-time information about USB devices as they are connected or disconnected.

## Conclusion

Congratulations! You have now explored more in-depth examples of how to use `lsusb` and its various options. The `lsusb` command is a valuable tool for understanding and managing USB devices connected to your system. Feel free to explore additional options and specific use cases based on your requirements.