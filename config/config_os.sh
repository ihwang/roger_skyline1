#!/bin/sh
SSHD_CONF="/etc/ssh/sshd_config"
JAIL_CONF="/etc/fail2ban/jail.conf"
POSTSENTRY_CONF="/etc/portsentry/portsentry.conf"
CRONTAB="/etc/crontab"

ROOT_PWD=$1
DEBIAN_PWD=$2
SSH_PORT=$3

config_sudo()
{
    echo "roger_skyline_1: Starting sudo configuration.."
    echo $ROOT_PWD | su -c "apt-get upgrade ; apt-get update ; apt-get install sudo -y >/dev/null 2>&1"
    echo $ROOT_PWD | su -c "sed -i '20 a debian\ \ \ ALL=(ALL:ALL) ALL' /etc/sudoers"
    echo "roger_skyline_1: Sudo configuration completed."
}

config_ssh() 
{
    echo "roger_skyline_1: Starting ssh configuration.."
    echo "$DEBIAN_PWD" | sudo -S sed -i '13,13d' $SSHD_CONF; echo "$DEBIAN_PWD" | sudo -S sed -i '13 a Port '$SSH_PORT $SSHD_CONF
    echo "$DEBIAN_PWD" | sudo -S sed -i '32,32d' $SSHD_CONF; echo "$DEBIAN_PWD" | sudo -S sed -i '32 a PermitRootLogin no' $SSHD_CONF
    echo "$DEBIAN_PWD" | sudo -S sed -i '37,37d' $SSHD_CONF; echo "$DEBIAN_PWD" | sudo -S sed -i '37 a PubkeyAuthentication yes' $SSHD_CONF
    echo "$DEBIAN_PWD" | sudo -S sed -i '58 a PasswordAuthentication no' $SSHD_CONF
    echo "$DEBIAN_PWD" | sudo -S sed -i '112,112d' $SSHD_CONF; echo "$DEBIAN_PWD" | sudo -S sed -i '112 a #AcceptEnv Lang LC_*' $SSHD_CONF
    echo "$DEBIAN_PWD" | sudo -S systemctl restart ssh
    echo "roger_skyline_1: Ssh configuration completed."
}

config_firewall()
{
    echo "roger_skyline_1: Starting firewall configuration.."
    echo "$DEBIAN_PWD" | sudo -S apt-get install ufw -y >/dev/null 2>&1
    echo "$DEBIAN_PWD" | sudo -S ufw allow $SSH_PORT
    echo "$DEBIAN_PWD" | sudo -S ufw allow from 192.168.1.4/30
    echo "$DEBIAN_PWD" | sudo -S systemctl enable ufw
    echo "$DEBIAN_PWD" | sudo -S ufw enable
    echo "roger_skyline_1: Firewall configuration completed."
}

config_dos()
{
    echo "roger_skyline_1: Starting DOS configuration.."
    echo "$DEBIAN_PWD" | sudo -S apt-get install fail2ban -y >/dev/null 2>&1
    echo "$DEBIAN_PWD" | sudo -S sed -i '244,244d' $JAIL_CONF; echo "$DEBIAN_PWD" | sudo -S sed -i '244 a #port=ssh' $JAIL_CONF
    echo "$DEBIAN_PWD" | sudo -S sed -i "245 a enabled=true" $JAIL_CONF
    echo "$DEBIAN_PWD" | sudo -S sed -i "246 a port=$SSH_PORT" $JAIL_CONF
    echo "$DEBIAN_PWD" | sudo -S systemctl restart fail2ban
    echo "roger_skyline_1: Firewall configuration completed."
}

block_portscan()
{
    echo "roger_skyline_1: Starting blocking post scanning.."
    echo "$DEBIAN_PWD" | sudo -S apt-get install portsentry -y >/dev/null 2>&1
    LINE_TO_MODIFY=$(echo "$DEBIAN_PWD" | sudo -S grep -n "BLOCK_UDP=" $PORTSENTRY_CONF | cut -d ":" -f 1 $PORTSENTRY_CONF)
    echo "$DEBIAN_PWD" | sudo -S sed -i "$LINE_TO_MODIFY,$LINE_TO_MODIFY d"
    echo "$DEBIAN_PWD" | sudo -S sed -i "$LINE_TO_MODIFY a BLOCK_UDP="1" " $PORTSENTRY_CONF
    LINE_TO_MODIFY=$(echo "$DEBIAN_PWD" | sudo -S grep -n "BLOCK_TCP=" $PORTSENTRY_CONF | cut -d ":" -f 1 $PORTSENTRY_CONF)
    echo "$DEBIAN_PWD" | sudo -S sed -i "$LINE_TO_MODIFY,$LINE_TO_MODIFY d"
    echo "$DEBIAN_PWD" | sudo -S sed -i "$LINE_TO_MODIFY a BLOCK_TCP="1" " $PORTSENTRY_CONF
    echo "$DEBIAN_PWD" | sudo -S systemctl restart portsentry
    echo "roger_skyline_1: Portsentry configuration completed."
}

spawn_scripts()
{
    echo "roger_skyline_1: Spawning scripts.."
    echo "$DEBIAN_PWD" | sudo -S apt-get install mailutils -y >/dev/null 2>&1
    #Updating pkgs
    echo '#!/bin/sh
    echo "$DEBIAN_PWD" | sudo -S apt-get update >> /var/log/update_script.log
    echo "$DEBIAN_PWD" | sudo -S apt-get upgrade >> /var/log/update_script.log
    ' > /home/debian/update_pkgs.sh
    chmod +x /home/debian/update_pkgs.sh

    #Get current crontab and compare
    echo '#!/bin/sh

    crontab -l > /home/debian/.crontab.new
    CHANGED=$(diff .crontab.old .crontab.new)

    if [ "$CHANGED" -eq "1" ]; then
        echo "." | mail -s "Crontab has been changed" root
    else
        rm /home/debian.crontab.new
    fi
    ' >>/home/debian/monitor_crontab.sh
    chmod +x /home/debian/monitor_crontab.sh
    echo "roger_skyline_1: Spawning scripts completed."
}

config_crontab()
{
    echo 'roger_skyline_1: Setting cron..'
    echo '0 4 * * 0 /home/debian/update_pkgs.sh
    0 2 * * * /home/debian/monitor_crontab.sh
    @reboot /home/debian/monitor_crontab.sh' > /tmp/my_cron
    crontab /tmp/my_cron
    rm /tmp/my_cron
    echo 'roger_skyline_1: Cron setting completed.'
    #Save old crontab
    crontab -l > /home/debian/.crontab.old
}

config_sudo
config_ssh
config_firewall
config_dos
block_portscan
spawn_scripts
config_crontab