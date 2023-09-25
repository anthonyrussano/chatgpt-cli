# How to View Available Disk Space in Debian Linux

In this tutorial, we will learn how to view the available disk space in Debian Linux. We will also cover how to perform a cleanup of temporary files to reclaim disk space.

## 1. Viewing Disk Space

To view the available disk space in Debian Linux, we can use the `df` command. This command displays disk space usage information for all mounted filesystems.

Open a terminal and run the following command:

```bash
df -h
```

The `-h` option is used to display the output in a human-readable format, showing sizes in kilobytes (K), megabytes (M), or gigabytes (G).

The output will include information about each filesystem, including the total size, used space, available space, and mount point.

## 2. Performing Cleanup of Temp Files

To perform a cleanup of temporary files in Debian Linux, we can use the `tmpreaper` utility. `tmpreaper` is a command-line tool designed to clean up files in directories based on their age.

### 2.1. Install tmpreaper

To install `tmpreaper`, open a terminal and run the following command:

```bash
sudo apt-get install tmpreaper
```

Enter your password when prompted.

### 2.2. Configure tmpreaper

After installing `tmpreaper`, you need to configure it. Open the configuration file using a text editor:

```bash
sudo nano /etc/tmpreaper.conf
```

In this file, you can define rules for file deletion based on their age and location.

For example, to delete all files older than 7 days in the `/tmp` directory, add the following line to the configuration file:

```
7d /tmp
```

Save the file and exit the text editor.

### 2.3. Run tmpreaper

To run `tmpreaper` and perform the cleanup, open a terminal and run the following command:

```bash
sudo tmpreaper -a
```

The `-a` option tells `tmpreaper` to operate interactively, prompting before deleting files.

You can automate the cleanup process by adding the `tmpreaper` command to a cron job. For example, to run it every day at 3 AM, run the following command in the terminal:

```bash
sudo crontab -e
```

Add the following line to the cron file:

```bash
0 3 * * * /usr/sbin/tmpreaper -a
```

Save the file and exit the text editor.

From now on, `tmpreaper` will automatically clean up temporary files, helping you reclaim disk space.