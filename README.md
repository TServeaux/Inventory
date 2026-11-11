# Inventory

A desktop and Android application for managing a **stock of electronic components** (resistors, LEDs, integrated circuits...), written in **Python** with **[Flet](https://flet.dev)**.

Components are organized by category, each category having its own icon and color. Stock can be added or removed in a few clicks, and everything is saved automatically.

## Features

- **Stock list** grouped by category, sorted by name, with a category filter.
- **Add a component**: name, category, quantity, description.
- **Custom categories**: create your own directly from the form, with an icon (resistor, capacitor, diode, chip...) and a color.
- **Detail page** for each component, with a quantity field and **Add** / **Remove** buttons.
- **Validation**: unique names, valid quantities, and no removing more than what is in stock.
- **Auto-save** after every change.

## Installation

Requirements: **Python 3.12 or newer** (the project is developed with Python 3.14 and Flet 1.1).

```bash
git clone <repository-url>
cd Inventory

python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
```

## Usage

From the project folder:

```bash
python src/main.py
```

The stock is empty on first launch. To get started:

1. Click **＋** (bottom right).
2. Open **Create a category**, type a name, pick an icon and a color, then confirm with **＋**.
3. Fill in the form and click **Save**.
4. On the home page, click a component to add or remove stock.

## Building the Android app (APK)

```bash
python -m flet.cli build apk
```

The APK is created in `build/apk/`. Copy it to your phone and open it to install it (Android will ask you to allow installing apps from unknown sources).

The first build automatically downloads Flutter, Java and the Android SDK (several GB): it can take a while. The next builds are much faster.

## Project structure

```
pyproject.toml              Project settings (name, version, dependencies, build options)
src/
  main.py                   Entry point
  assets/icons/             Category icons (SVG files from Tabler Icons)
  core/
    userInterface.py        Routing between pages, creates the stock
    stock.py                Stock class: data and business rules
    icons.py                Available icons and colors
    views/
      home.py               Home page (stock list)
      newComponent.py       Add-component form
      componentDetail.py    Component details and stock movements
  utils/
    save.py                 Save class: reading / writing files
```

## Architecture

The code is split into three layers, each with a single responsibility:

```
Views (Home, NewComponent, ComponentDetail)   display and input
        │  call Stock methods
        ▼
Stock                                         business rules
        │  requests a save after every change
        ▼
Save                                          JSON file
```

- **Views** never modify the data themselves. They call `Stock` and display the result or the error message.
- **`Stock`** holds all the rules. When an operation is rejected, it raises a `StockError` whose message is shown to the user. The rules therefore apply everywhere, whichever page makes the request.
- **`Save`** only knows about files. It first writes to a temporary file, then replaces the old one in a single operation, so an interruption during the write cannot corrupt the save file.

## Data format

The data is stored in an `Inventory` folder inside the documents folder given by the system:

- **Windows**: `Documents\Inventory\`
- **Android**: a private folder of the app, kept when the app is updated (deleted if it is uninstalled).

`inventory.json`:

```json
{
  "categories": [
    { "name": "Resistors", "icon": "circuit-resistor", "color": "orange" },
    { "name": "LEDs", "icon": "bulb", "color": "red" }
  ],
  "components": [
    {
      "name": "Red LED 5mm",
      "category": "LEDs",
      "quantity": 42,
      "description": "Diffused, 20 mA"
    }
  ]
}
```

- `name` is the component's **identifier**: it must be unique, ignoring case and leading/trailing spaces.
- `icon` is the name of an SVG file in `src/assets/icons/` (without `.svg`), and `color` a name from the palette in `src/core/icons.py`.

> Back up the `Inventory` folder yourself if your stock matters to you.

## Current limitations and roadmap

- Components and categories cannot be **edited** or **deleted** yet (including the icon and color of a category).
- The computer and the phone each have **their own stock**: there is no synchronization between them.
- JSON storage is suited to a single user. Using several devices at the same time would require a database such as SQLite.

## Credits

Icons by [Tabler Icons](https://tabler.io/icons), MIT license (see `src/assets/icons/LICENSE`).

## Author

Tao Serveaux
