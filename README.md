# Ninja Game

## About

This is a simple platformer game made with Pygame. You play as a Ninja and need to defeat enemies to progress through the levels.

The main purpose of this project was to get hands-on practice and build foundational knowledge about game development, including common game mechanics, math, and features. Here are some of the implemented features:

- **Player Movement**: Left/right movement, jumping, wall sliding, and dashing mechanics
- **Enemy AI**: Basic enemy behavior with patrol patterns and projectile shooting
- **Combat System**: Dash attack to eliminate enemies, enemy projectiles that can damage the player
- **Physics System**: Custom collision detection and gravity
- **Level Design**: Multiple levels with platforms and decorative elements
- **Level Editor**: Custom-built tile-based editor for creating and modifying levels
- **Visual Effects**:
  - Particle systems for leaves and impacts
  - Spark effects for combat actions
  - Screen shake on hits
  - Smooth camera following system
  - Parallax scrolling clouds for depth
- **Audio**: Sound effects for jumping, dashing, shooting, and hits, plus background music and ambience
- **Animations**: Sprite animations for player and enemies using sprites
- **Level Progression**: Smooth transitions between levels with circle wipe effect
- **Game States**: Death and respawn system, level completion detection

## Installation

The project uses `uv` for dependency management. To set up the project, you'll need to install `uv` first. You can find the installation instructions [here](https://docs.astral.sh/uv/getting-started/installation/).

Once `uv` is installed, you can set up the project by running the following command in your terminal:

```bash
uv sync
```

This command will create a virtual environment and install all the required dependencies for the project.

## Running the project

To run the game:

1. First, activate the virtual environment created by `uv`:
    - Windows example:

    ```bash
    .venv\Scripts\activate
    ```

2. Then, you can run either the game or the level editor using the following commands:

### For the Game

```bash
python game.py
```

### For the Level Editor

```bash
python editor.py
```

## Building Executables

To build standalone executables for the game and level editor, you can use `PyInstaller`. The `PyInstaller` is already included in the project's dependencies. To build the executables, you need to be on the platform you want to build for. Like if you want to build for Windows, you need to run the build command on a Windows machine.

1. First, activate the virtual environment created by `uv`:
    - Windows example:

    ```bash
    .venv\Scripts\activate
    ```

2. Then, run the following commands to build the executables:
    - Windows example:

    ```bash
    python -m PyInstaller game.py --noconsole --add-data data:./data
    ```

3. The built executables will be located in the `dist` folder within the project directory.

NOTE: The `--add-data data:./data` flag is used to include the game assets located in the `data` folder, since PyInstaller does not include non-Python files by default.

For any other clarifications about using PyInstaller, please refer to the [PyInstaller documentation](https://pyinstaller.org/en/stable/).
