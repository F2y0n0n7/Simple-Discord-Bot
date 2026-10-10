# Contributing to Simple-Discord-Bot 🤖

First off, thank you for considering contributing to this project! It's open-source contributions like yours that make this community an amazing place to learn, inspire, and create.

Please follow these guidelines to ensure a smooth contribution process.

---

## 📋 Table of Contents
1. [Prerequisites & Local Setup](#-1-prerequisites--local-setup)
2. [How to Contribute a New Cog / Feature](#-2-how-to-contribute-a-new-cog--feature)
3. [Cog Code Guidelines & Boilerplate](#-3-cog-code-guidelines--boilerplate)
4. [Submitting Your Work (Pull Request)](#-4-submitting-your-work-pull-request)
5. [Reporting Bugs & Requesting Features](#-5-reporting-bugs--requesting-features)

---

## 🛠️ 1. Prerequisites & Local Setup

Before you start writing code or testing things out, get your local development environment ready:

1. **Fork & Clone:**
   - Fork this repository on GitHub (`https://github.com/F2y0n0n7/Simple-Discord-Bot`).
   - Clone your fork locally to your computer:
     ```bash
     git clone https://github.com/YOUR-USERNAME/Simple-Discord-Bot.git
     cd Simple-Discord-Bot
     ```

2. **Install Dependencies:**
   - Install all required Python packages:
     ```bash
     pip install -r requirements.txt
     ```

3. **Configure Environment:**
   - Copy the example environment file to create your own `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open the newly created `.env` file and insert your personal Discord Bot Token:
     ```env
     DISCORD_TOKEN=your_bot_token_here
     BOT_PREFIX=!
     ```

4. **Test Locally:**
   - Run the bot to make sure everything works properly before you start developing:
     ```bash
     python main.py
     ```

---

## 🌿 2. How to Contribute a New Cog / Feature

Always isolate your work in a dedicated branch. Never code directly on the `main` branch.

1. **Create a Feature Branch:**
   Use a clear and descriptive name for your branch (e.g., `feature/ticket-system`, `feature/music-cog`):
   ```bash
   git checkout -b feature/name-of-your-cog
   ```

2. **Develop Your Module:**
   Add your new Python file directly inside the `cogs/` folder. The bot will automatically load it on startup via the dynamic loader.

---

## 🧩 3. Cog Code Guidelines & Boilerplate

When adding a new Cog in the `cogs/` directory, please ensure:
- It inherits from `commands.Cog`.
- It includes an `async def setup(bot):` function at the bottom so the main file can load it dynamically.
- Code is clean, well-commented, and avoids hardcoded secrets (use configuration files/environment variables where appropriate).

### Standard Cog Boilerplate:
```python
import discord
from discord.ext import commands

class MyCustomCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} is online.")

    @commands.command(name="example", help="An example command")
    async def example_command(self, ctx):
        await ctx.send("Hello from your new Cog!")

async def setup(bot):
    await bot.add_cog(MyCustomCog(bot))
```

---

## 🚀 4. Submitting Your Work (Pull Request)

Once your code is written and tested successfully on your local bot:

1. **Commit your changes:**
   Write clear and descriptive commit messages (e.g., `feat: add music cog`, `fix: resolve issue with welcome message`):
   ```bash
   git add .
   git commit -m "feat: add [NameOfFeature] cog"
   ```

2. **Push to your fork:**
   ```bash
   git push origin feature/name-of-your-cog
   ```

3. **Open a Pull Request:**
   - Go to the original repository on GitHub (`https://github.com/F2y0n0n7/Simple-Discord-Bot`).
   - Click on the **Compare & pull request** button.
   - Fill out the description explaining what your Cog/feature does and how to test it.
   - Submit the Pull Request for review!

---

## 🐛 5. Reporting Bugs & Requesting Features

If you found a bug or have an idea for a cool new module but don't want to code it yourself right away:

- **Bug Reports:** Open an issue on GitHub, detailing the steps to reproduce the bug, expected behavior, and include any error logs from your console.
- **Feature Requests:** Open an issue with the tag `enhancement` to pitch your idea or request a specific new Cog before you start coding!

Thank you for helping make `Simple-Discord-Bot` better for everyone! 🎉