# 🤖 Simple Discord Bot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/discord.py-2.3%2B-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord.py">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License">
</p>

A lightweight, modular, and open-source Discord bot template built in Python using `discord.py`. Designed with a clean architecture to simplify open-source contributions, feature expansion, and dynamic module loading.

---

## 📂 Project Architecture

The source code is cleanly isolated inside the `src/` directory, separating your core application logic from configuration files and documentation:

```text
Simple-Discord-Bot/
├── src/
│   ├── cogs/              # Modular extension files (welcome, moderation, etc.)
│   │   ├── status.py
│   │   └── moderation.py
│   ├── utils/             # Additional Functions
│   │   └── config.py      # Creates the config.json based on the existing cogs
│   ├── config.json        # Global bot settings (prefix, colors, roles)
│   └── main.py            # Entry point & dynamic extension loader
├── .env                   # Secret credentials (never commit this!)
├── .env.example           # Environment template
├── .gitignore             # Ignored files and directories
├── CONTRIBUTING.md        # Guidelines for contributors
├── LICENSE                # MIT License
└── requirements.txt       # Python dependencies
```

---

## 🚀 Getting Started

Follow these steps to get your bot up and running locally.

### 1. Clone the Repository
```bash
git clone https://github.com/F2y0n0n7/Simple-Discord-Bot.git
cd Simple-Discord-Bot
```

### 2. Install Dependencies
Make sure you have Python 3.10 or higher installed, then install the required packages:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy the example environment file and add your secret bot token:
```bash
cp .env.example .env
```
Open `.env` and fill in your credentials:
```env
DISCORD_TOKEN=your_actual_discord_bot_token_here
```

### 4. Configure the Bot Settings (`src/config.json`)
After the bot is started for the first time, a `config.json` file is created based on the available modules. 
You can adjust global settings in `src/config.json`.

You can find the config Documentaion under `docs/cog`


### 5. Run the Bot
Start the application from the project root:
```bash
python src/main.py
```

---

## 🛠️ Adding New Modules (Cogs)

Want to add a new feature? Simply create a new Python file inside the `src/cogs/` folder following the Cog structure guidelines. The bot will automatically detect and load it on startup!

---

## 🤝 Contributing

We love open-source contributions! Whether it's reporting a bug, improving documentation, or creating a brand-new Cog, please check out our [CONTRIBUTING.md](CONTRIBUTING.md) guide to get started.

---

## 📄 License

This project is licensed under the terms of the [MIT License](LICENSE).