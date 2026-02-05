# FreeCell Discord Bot

This is a simple Discord bot that allows you to play FreeCell.

## How to Run the Bot

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Get Your Discord Bot Token:**
    - Go to the [Discord Developer Portal](https://discord.com/developers/applications).
    - Create a new application.
    - Go to the "Bot" tab and click "Add Bot".
    - Copy the token.

3.  **Update the Code:**
    - Open `discord_bot/main.py`.
    - Replace `"YOUR_DISCORD_TOKEN"` with your actual bot token.

4.  **Run the Bot:**
    ```bash
    python discord_bot/main.py
    ```

## How to Play

-   `$deal`: Starts a new game of FreeCell.
-   `$board`: Displays the current state of the game.
-   `$move <from> <to>`: Moves a card.
    -   `<from>` and `<to>` can be:
        -   `c<number>` for a cascade (e.g., `c1`).
        -   `f<number>` for a free cell (e.g., `f1`).
        -   `o<number>` for a foundation (e.g., `o1`).
    -   Example: `$move c1 f1` moves the top card of cascade 1 to free cell 1.
-   `$move <from> <card_index> <to>`: Moves a card from a specific index in a cascade.
    -   `<card_index>` is the index of the card in the cascade (0-based, from the top).
    -   Example: `$move c1 0 f1` moves the top card of cascade 1 to free cell 1.
