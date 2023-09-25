## Visual Studio Code Server: Checking Users with fuser

In this tutorial, we will walk through the process of using `fuser` to check how many users have a Visual Studio Code (VSCode) session open on your server running VSCode Server as a web app on port 8000.

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
sudo fuser -n tcp 8000
```

This will display the PID(s) of the process(es) bound to port 8000, such as:

```
8000/tcp: 1234
```

In this case, the PID is `1234`.

### Step 3: Check Users

Now that we have the PID, we can use it to check the users associated with the VSCode sessions.

Run the following command, replacing `1234` with the actual PID you obtained in the previous step:

```shell
sudo lsof -p 1234 | grep vscode
```

This will display the information about the users who have a VSCode session open on port 8000.

### Conclusion

Using the `fuser` and `lsof` commands, you can easily check how many users have a VSCode session open on your server running VSCode Server as a web app on port 8000.

Remember to replace `1234` in the command with the actual PID you obtained from `fuser`.

With this information, you can better monitor and manage user sessions on your VSCode server.