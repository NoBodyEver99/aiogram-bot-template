# Aiogram Bot Template

![License](https://img.shields.io/github/license/NoBodyEver99/aiogram-bot-template)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![GitHub last commit](https://img.shields.io/github/last-commit/NoBodyEver99/aiogram-bot-template)

## Description

This project is a template for creating bots on the Telegram platform using the [aiogram](https://github.com/aiogram/aiogram) framework. It includes a fully working administration panel with functions of statistics, mailing, channel management for mandatory subscription and UTM tags. The database is created automatically if it doesn't exist and user data is updated in the database if the user changes it in Telegram.

## Features

- Asynchronous bot using aiogram
- Database support using Tortoise ORM and asyncpg
- Database migrations using Aerich
- Redis for caching and data storage
- Logging using Loguru
- Execution acceleration using uvloop
- Configuration support via .env file
- Fully working admin panel:
  - Statistics
  - Newsletter
  - Channel management for mandatory subscription
  - UTM tags

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/NoBodyEver99/aiogram-bot-template.git
   cd aiogram-bot-template
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate # for Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create .env and configure environment variables, use .env.example as a reference:
   ```bash
   cp .env.example .env
   ```

## Usage

1. initialize Aerich:
   ```bash
   aerich init -t config.TORTOISE_ORM
   ```
2. Create the first migration and apply it:
   ```bash
   aerich init-db
   ```

3. Run the bot:
   ```bash
   python start.py
   ```

## Project structure

- bot/: The directory with the main bot code.
- .env.example: Configuration file.
- db/: Directory with database initialization and models.
- migrations/: Directory with database migrations.
- newsletter/: Directory with newsletter functionality.
- requirements.txt: List of project dependencies.
- start.py: Script to start the bot.

## Support

If you have any questions or problems with the project, please create an issue on [GitHub](https://github.com/NoBodyEver99/aiogram-bot-template/issues).

## License

This project is licensed under the terms of the MIT license. See the LICENSE file for details.
