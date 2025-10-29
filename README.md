# 🖥️ YAML Dashboard – Raspberry Pi & macOS

A lightweight, open-source project to **automatically display dashboards and web pages (Grafana, Notion, TweetDeck, etc.)** based on the time of day — perfect for an **agency wallboard** or personal workspace.

---

## 🚀 1. Installation

### On macOS or Raspberry Pi (Debian / Raspberry Pi OS)

1️⃣ Install **Chromium / Chrome** and **unclutter** (for Raspberry Pi only):

```bash
# On Raspberry Pi
sudo apt update
sudo apt install -y chromium-browser unclutter

# On macOS
brew install --cask google-chrome
```

2️⃣ Clone this repository:

```bash
git clone https://github.com/romain/yamldash.git
cd yamldash
```

3️⃣ Make the script executable:

```bash
chmod +x dashboard.sh
```

🧩 Install **yq** (used to parse the YAML configuration):

```bash
# On Raspberry Pi
sudo apt update
sudo apt install -y yq

# On macOS
brew install yq
```

---

## 🧩 2. Configuration File

Edit the `schedule.yaml` file to define your time blocks and URLs:

```yaml
schedule:
  - name: Morning
    start: "08:00"
    end: "09:30"
    urls:
      - "https://www.lac-annecy.com/meteo/"
      - "https://calendar.google.com"
```

You can add as many time ranges and links as you want — for example, “Workday”, “Lunch Break”, “Evening”.

---

## ⚙️ 3. Running the Dashboard

Start the dashboard manually:

```bash
./dashboard.sh
```

The script will:

- Read `schedule.yaml`
- Detect the current time block
- Open all corresponding URLs in **Chromium/Chrome**
- Run in **kiosk / fullscreen mode**
- Automatically refresh when the next schedule block starts

> 💡 On macOS, Chrome might display a message saying  
> “Chrome is being controlled by automated software.”  
> This is normal and harmless.

---

## ⏰ 4. Auto-Start on Boot (Optional)

### Raspberry Pi (GUI Autostart)

Edit this file:

```bash
nano ~/.config/lxsession/LXDE-pi/autostart
```

Add:

```bash
@/home/pi/yamldash/dashboard.sh
```

### Or via Cron (both macOS & Raspberry Pi)

```bash
crontab -e
```

Add the following lines:

```bash
@reboot /home/pi/yamldash/dashboard.sh
```

---

## 🌙 5. Useful Tips

- **Hide the mouse cursor (Pi)**
  ```bash
  unclutter -idle 0 &
  ```
- **Prevent Chrome keyring prompts**  
  Add `--password-store=basic` to your Chromium launch options.
- **Turn the screen off at night**
  ```bash
  xset dpms force off
  ```
- **Use a smart plug (e.g. TP-Link Tapo)** to power off/on the Pi automatically.

---

## 🧠 6. Daily Automation Example

```bash
0 8 * * * /home/pi/yamldash/dashboard.sh  # Start at 8 AM
0 23 * * * sudo shutdown now              # Power off at 11 PM
```

---

## ✅ 7. Checking Logs

To watch live logs and debug output:

```bash
tail -f dashboard.log
```

---

## 💡 8. Advanced Ideas

- Add smooth transitions between pages (using `xdotool` or JavaScript)
- Run a small Node.js server for remote control
- Block cookie or consent popups (with uBlock Origin or custom Chrome extension)
- Display an overlay clock or the current schedule name
- Integrate analytics dashboards (Grafana, Looker Studio, Metabase)
- Connect Slack, Notion, or GitLab boards for team monitoring
