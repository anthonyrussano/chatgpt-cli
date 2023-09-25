You're correct! To see the user running the process and obtain a more verbose output, we can utilize the `-v` flag with the `fuser` command. Let's update the previous instructions to include the `-v` flag.

## Visual Studio Code Server: Checking Users with fuser

In this tutorial, we will walk through the process of using `fuser` with the `-v` flag to check how many users have a Visual Studio Code (VSCode) session open on your server running VSCode Server as a web app on port 8000.

### Prerequisites

Before proceeding, please ensure the following:

- You have `fuser` installed on your server.
- You have VSCode Server set up as a web app and running on port 8000.

### Step 1: Install fuser

On most Linux distributions, `fuser` comes pre-installed. However, if you don't have it installed on your system, follow the instructions corresponding to your distribution:

**Debian/Ubuntu:**

```shell
sudo apt update
sudo apt install psmisc
```

**Red Hat/CentOS:**

```shell
sudo yum install psmisc
```

### Step 2: Identify the Process ID

To check how many users have a VSCode session open on port 8000, we need to identify the associated process ID (PID).

To do this, run the following command:

```shell
sudo fuser -nv tcp 8000
```

This will display the PID(s) of the process(es) bound to port 8000, along with the username(s) of the user(s) running the process, such as:

```
                     USER        PID ACCESS COMMAND
8000/tcp:             user1      1234 F....  vscode
```

In this case, `user1` is the user running the process, and the PID is `1234`.

### Step 3: Check Users

Now that we have the PID and the associated username, we can use `lsof` to obtain further information about the VSCode sessions.

Run the following command, replacing `1234` with the actual PID you obtained in the previous step:

```shell
sudo lsof -p 1234 | grep vscode
```

This will display the detailed information about the user(s) who have a VSCode session open on port 8000.

### Conclusion

Using the `fuser` command with the `-v` flag, along with `lsof`, you can easily check how many users have a VSCode session open on your server running VSCode Server as a web app on port 8000.

Remember to replace `1234` in the command with the actual PID you obtained from `fuser`.

With this information, you can monitor the user sessions and gather more detailed information about their VSCode sessions on your VSCode server.