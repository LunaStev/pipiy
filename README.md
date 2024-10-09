# Pipiy

`pipiy` is a tool for managing pip packages using WSON formatted requirements files, similar to Gradle or Maven.

## Installation

Clone the repository and install it:

```bash
pip install .
```

```wson
{
    module = [
        numpy = "1.24.0",
        discord.py = "2.2.2"
    ]
}
```