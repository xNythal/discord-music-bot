# 🎧 DiscordMusicBot — Modular, Secure, and Showcase-Ready

This repository demonstrates a production-level Discord bot for music playback, designed as a proof-of-skill project. It emphasizes modular architecture, secure configuration handling, and flexible setup to support customization and scalability.

---

## 🚀 Features

- 🎵 **Music Playback** — Stream high-quality audio using FFmpeg
- 🔐 **Secure Token Handling** — Secrets managed via environment variables
- 📂 **Modular Codebase** — Commands split into cogs for maintainability
- ⚙️ **Customizable Configs** — Role names, embed messages, and permissions adjustable
- 🧪 **Dev-Friendly Structure** — Easy to extend with utilities, moderation tools, or AI commands

---

## 📁 Folder Layout

```
DiscordMusicBot/
│
├── cogs/              # Bot features as extensions
│   └── music.py       # Music playback functionality
│   └── developer.py   # Developer-only tools
│
├── constants/         # Configs and message formatting
│   └── config.py
│   └── messages.py
│
├── data/              # Role persistence (e.g. DJ roles)
│   └── dj_roles.txt
│
├── utils.py           # Helper functions
├── main.py            # Bot entry point
├── requirements.txt   # Dependencies
├── .env.example       # Sample environment variables
├── .gitignore         # Git ignore rules
```

---

## ⚙️ Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/discord-music-bot.git
cd discord-music-bot
```

### 2. Install Required Packages
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file at the root of the project (use `.env.example` as a reference):

```env
DISCORD_TOKEN=your_bot_token_here
```

> 🔐 **Note**: `.env` is excluded from version control via `.gitignore`.

### 4. Configure Bot Behavior

Customize `constants/config.py`:

```python
COMMAND_PREFIX = "!"
LOG_FILE_PATH = "logs/log1.txt"
```

Update default messages in `constants/messages.py`:

```python
PAUSE_MESSAGE = "⏸️ Playback is paused."
STOP_MESSAGE = "🛑 Music stopped."
```

### 5. Run the Bot
```bash
python main.py
```

---

## 🪪 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). You’re free to fork, modify, or contribute.

---

## 📣 Attribution

Developed by [xNythal](https://github.com/xNythal) as a skills showcase.  
Designed for educational and demonstration purposes.  
Not affiliated with Discord Inc.