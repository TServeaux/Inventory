# Inventory

A desktop application for managing a **stock of electronic components** (resistors, LEDs, integrated circuits...), written in **Python** with **[Flet](https://flet.dev)**.

Components are organized by category, each with a picture, a quantity and a description. Stock can be added or removed in a few clicks, and everything is saved automatically.

## Features

- **Stock list** grouped by category, sorted by name, with a category filter.
- **Add a component**: name, category, picture, quantity, description.
- **Custom categories**: create your own directly from the form.
- **Detail page** for each component, with a quantity field and **Add** / **Remove** buttons.
- **Validation**: unique names, valid quantities, and no removing more than what is in stock.
- **Auto-save** after every change. Pictures are copied into the data folder.

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
python main.py
```

The stock is empty on first launch. To get started:

1. Click **＋** (bottom right).
2. Create a category in the **New category** field, then confirm with **＋**.
3. Fill in the form and click **Save**.
4. On the home page, click a component to add or remove stock.

## Project structure

```
main.py                     Entry point
src/
  core/
    userInterface.py        Routing between pages, creates the stock
    stock.py                Stock class: data and business rules
    views/
      home.py               Home page (stock list)
      newComponent.py       Add-component form
      componentDetail.py    Component details and stock movements
  utils/
    save.py                 Save class: reading / writing files
data/                       User data (created automatically, not versioned)
  inventory.json
  pictures/
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
Save                                          files (JSON + pictures)
```

- **Views** never modify the data themselves. They call `Stock` and display the result or the error message.
- **`Stock`** holds all the rules. When an operation is rejected, it raises a `StockError` whose message is shown to the user. The rules therefore apply everywhere, whichever page makes the request.
- **`Save`** only knows about files. It first writes to a temporary file, then replaces the old one in a single operation, so an interruption during the write cannot corrupt the save file.

## Data format

`data/inventory.json`:

```json
{
  "categories": ["Resistors", "LEDs"],
  "components": [
    {
      "name": "Red LED 5mm",
      "category": "LEDs",
      "picture": "3f2a9c...e1.jpg",
      "quantity": 42,
      "description": "Diffused, 20 mA"
    }
  ]
}
```

- `name` is the component's **identifier**: it must be unique, ignoring case and leading/trailing spaces.
- `picture` is the name of the copy in `data/pictures/`, or `null` if there is no picture.

> The `data/` folder is excluded from git. Back it up yourself if your stock matters to you.

## Current limitations and roadmap

- Components and categories cannot be **edited** or **deleted** yet.
- No **web / mobile** version yet: picture selection will need to be adapted.
- JSON storage is suited to a single user. Using several devices at the same time would require a database such as SQLite.

## Author

Tao Serveaux
