# Overclocking the Raspberry Pi 4 - Interactive Script

## Introduction
In this tutorial, we will create a Bash script that allows the user to overclock a Raspberry Pi 4 with interactive prompts to set the overclock settings. Overclocking can provide a performance boost but may also increase power consumption and generate more heat.

## Steps

1. Open a text editor and create a new file, for example, `overclock_pi4.sh`.

2. Add the following code to the file to define the script and its interactive prompts:

```bash
#!/bin/bash

# Function to prompt for an integer input
get_integer_input() {
    local prompt_string="$1"
    while true; do
        read -p "$prompt_string" input_value
        if [[ "$input_value" =~ ^[0-9]+$ ]]; then
            break
        else
            echo "Please enter a valid integer value."
        fi
    done
    echo "$input_value"
}

# Prompt for overclock settings
echo "Raspberry Pi 4 Overclocking Script"
echo "Please enter the required overclock settings:"

# ARM frequency
arm_freq=$(get_integer_input "ARM frequency (in MHz): ")

# GPU frequency
gpu_freq=$(get_integer_input "GPU frequency (in MHz): ")

# Overvolt
over_voltage=$(get_integer_input "Overvoltage (in mV, e.g., 6 for +6mV): ")

# Configure the overclock settings
echo "config.txt settings:"
echo "arm_freq=$arm_freq"
echo "gpu_freq=$gpu_freq"
echo "over_voltage=$over_voltage"
```

3. Save and close the file.

4. Make the script executable by running the following command in the terminal:
```
chmod +x overclock_pi4.sh
```

5. Execute the script using the following command:
```
./overclock_pi4.sh
```

6. The script will prompt you to enter the required overclock settings. Follow the prompts and enter the desired values.

7. After entering the values, the script will display the configured overclock settings.

8. If desired, you can copy the displayed `config.txt` settings into the `/boot/config.txt` file to apply the overclocking permanently.

## Conclusion
By creating this interactive script, you can easily prompt the user for overclock settings and configure the Raspberry Pi 4 accordingly. Remember to be cautious when overclocking and monitor the system for stability and temperature.