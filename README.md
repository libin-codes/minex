
![OS support](https://img.shields.io/badge/OS-macOS%20Linux%20Windows-red)



███╗░░░███╗██╗███╗░░██╗███████╗██╗░░██╗
████╗░████║██║████╗░██║██╔════╝╚██╗██╔╝
██╔████╔██║██║██╔██╗██║█████╗░░░╚███╔╝░
██║╚██╔╝██║██║██║╚████║██╔══╝░░░██╔██╗░
██║░╚═╝░██║██║██║░╚███║███████╗██╔╝╚██╗
╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝


# MINEX

An aesthetic terminal-based Minesweeper game that supports **mouse clicks for gameplay**!

![Minesweeper TUI Demo](demo.gif)

## Features
- **Mouse support**: reveal, flag and chord using mouse
- 🎮 **Multiple Game Modes**: Easy, Medium, Expert, and Custom levels
- 🎨 **Themes**: Choose from 5 unique themes (Default, Winter, Desert, Space, Cyberpunk)
- 🎵 **Sound Effects**: Toggle sound on/off for an immersive experience

- 📊 **Game Statistics**: Track your win streak, best time, and win rate
- ⚙️ **Customization**: Configure chording method (disabled, left-click, middle-click, right-click)
- 💾 **Persistent Settings**: Your preferences are saved between sessions

## Installation

### Option 1: Standalone Executable

Download the latest executable from the [releases page](https://github.com/your-username/minesweeper-tui/releases).

```bash
# Run directly
minex     
````

### Option 2: Install with pipx (Recommended)

```bash
# Install pipx if you don't have it
pip install pipx
pipx install minex

# Run the game
minex
```

### Option 3: Install from source

```bash
# Clone the repository
git clone https://github.com/your-username/minesweeper-tui.git
cd minesweeper-tui

# Install dependencies
pip install -e .

# Run the game
mines
```
         |

## Screenshots

![Default Theme](screenshots/default.png)
![Winter Theme](screenshots/winter.png)
![Custom Board](screenshots/custom.png)

## Video Demo

[Watch the gameplay demonstration video](https://youtu.be/your-video-id)

## Built With

- [Python](https://www.python.org/)
- [Textual](https://textual.textualize.io/) - TUI Framework
- [Pygame](https://www.pygame.org/) - Audio Support

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Created by [libin-codes](https://github.com/your-username)
- All the Minesweeper enthusiasts out there 💣
