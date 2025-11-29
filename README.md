
# WSL-Virt

WSL-Virt is a project that enables you to use Virt Manager, QEMU, and libvirt on your Windows PC via Windows Subsystem for Linux (WSL). With WSL-Virt, you can manage, configure, and run virtual machines directly on Windows with a native Linux virtualization stack.

---

## Prerequisites

- Windows 10 or 11 (with WSL2 enabled)
- WSL2 installed and running (a preferred Linux distro: Ubuntu/Debian)
- X server for Windows ([VcXsrv](https://sourceforge.net/projects/vcxsrv/) or [X410](https://x410.dev/)) to display GUI applications

---

## Installation

Open your WSL terminal (Ubuntu/Debian recommended) and run the following commands:

```bash
# Update package lists and upgrade system
sudo apt update
sudo apt upgrade -y

# Install QEMU, Virt-Manager, and libvirt
sudo apt install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virt-manager

# (Optional) Add your WSL user to the libvirt group for management privileges
sudo usermod -aG libvirt $(whoami)

# Restart libvirtd service (some distros require systemctl; on WSL, try:)
sudo service libvirtd restart
```

---

## Running Virt Manager

1. Start your X server on Windows (e.g., VcXsrv).
2. In your WSL terminal, export your display:

    ```bash
    export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
    ```

3. Launch Virt Manager:

    ```bash
    virt-manager
    ```

Virt Manager's GUI will appear on Windows via the X server.

---

## Notes

- Hardware virtualization (VT-x/AMD-V) support in WSL2 depends on your Windows host and system configuration.
- For USB/device passthrough and advanced networking, additional configuration may be required.
- Testing and optimization for different Windows versions and WSL distributions are recommended.

---

## License

MIT
