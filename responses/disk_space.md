To check the available disk space on your system, you can use the `df` command. Here's how:

1. Open the terminal on your Debian Linux system.
2. Type the following command and press Enter:

```shell
df -h
```

This will display disk usage information in a human-readable format.

The `-h` flag tells `df` to display sizes in a "human-readable" format, which means using units like "K" for kilobytes, "M" for megabytes, and "G" for gigabytes.

The output will include information about all mounted file systems on your system, their used and available space, the file system type, and the mount point.