# 🧩 Module: Status (`cogs/status.py`)

The Status module provides a detailed real-time overview of the host system's performance and current bot health.

#### 🛠️ Displayed Metrics:
- ⏱️ **Uptime:** The exact running time of the bot since its last restart (hours, minutes, seconds).
- 🏓 **Ping:** Current WebSocket latency to the Discord gateway in milliseconds (`ms`).
- 🧠 **Memory (RAM):** Memory usage in percentage with a visual progress bar and exact GB footprint (used / total).
- ⚙️ **CPU:** Processor usage in percentage with a visual progress bar and active thread count.
- 💾 **Disk:** Disk usage in percentage with a visual progress bar and exact used / total size.
- 🌐 **Network:** Total transferred data volume (Upload / Download).
- 🔄 **Auto-Update:** Refresh interval (e.g., every 30 seconds) including a relative timestamp of the last update.

---

## ⚙️ Configuration Options (`src/config.json`)

All settings for this module are nested under the `"status"` key in `src/config.json`.

| Key | Type | Default Value | Required | Description |
| :--- | :--- | :--- | :---: | :--- |
| `enabled` | `Boolean` | `true` | Yes | Enables or disables this module globally. If `false`, the cog is not loaded. |
| `channel_id` | `Integer` | `None` | Yes | Discord Channel ID where the status message is posted. |
| `update_interval` | `Integer` | `30` | No | Refresh interval in seconds. Must be greater than 0, otherwise `30` is used. |
| `embed_color` | `String` | `None` (green) | No | Accent color of the container as hex, e.g. `"#ADD8E6"` or `"0xADD8E6"`. Only the lower 24 bits are used (an alpha byte like `FF` is ignored). |
| `modules` | `Object` | all `true` | No | Toggles for the displayed metrics: `uptime`, `ping`, `memory`, `cpu`, `disk`, `network`. At least one must be `true`. |
| `message_id` | `Integer` | `None` | No | ID of the status message to edit. Leave empty to create a new one. |

---

## 📄 JSON Example

```json
{
  "status": {
    "enabled": true,
    "channel_id": None,
    "update_interval": 30,
    "embed_color": "#ADD8E6",
    "modules": {
      "uptime": true,
      "ping": true,
      "memory": true,
      "cpu": true,
      "disk": true,
      "network": true
    }
  }
}
```