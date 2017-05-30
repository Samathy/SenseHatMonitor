xset s off
xset -dpms

matchbox-window-manager &
echo "Started matchbox"
while true; do
    WEBKIT_DISABLE_TBS=1 epiphany -a --profile=/home/rruk/.config file:///home/rruk/SenseHatMonitor/websockets_chart.html
done

