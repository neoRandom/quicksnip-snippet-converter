# QuickSnip Snippet Converter
Converts a code snippet into a formatted JSON used on the QuickSnip open-source project.

## Summary
- [Usage](#usage)
- [Formatting](#formatting)
- [QuickSnip](#quicksnip)
- [License](#license)

## Usage

#### Requirements
- Python ( >= 3.9 ig; >=3.12 recommended )
- Linux (recommended)
- Python Virtual Environment (recommended)

#### Commands

- `pip install -r requirements.txt`
- `cd src`
- `python ./converter.py <file path> <language (optional)>`

## Formatting

#### Input

Base structure:
``` python
<category: str>
<title: str>
<description: str>
<tags: list[str]>
<author: str>

<code: list[str]>
```

Python example:
``` python
# SQLite Database
# Examples
# Simple Examples
# python, hello world, beginner friendly, prevents accidental execution when importing
# neoRandom

if __name__ == "__main__":
    print("Hello, world")
```

JavaScript example:
``` javascript
// Fundamentals
// Examples
// Simple Examples
// java, javascript, just kiddin they are not the same
// neoRandom

console.log("Hello, world!")
```

#### Output:

Python example (`python.json`):
``` json
[
  {
    "categoryName": "SQLite Database",
    "snippets": [
      {
        "title": "Examples",
        "description": "Simple Examples",
        "code": [
          "if __name__ == \"__main__\":",
          "    print(\"Hello, world\")",
          ""
        ],
        "tags": [
          "python",
          "hello world",
          "beginner friendly",
          "prevents accidental execution when importing"
        ],
        "author": "neoRandom"
      }
    ]
  }
]
```

> Note: The only thing that change from language to language is the output file name (`python.json` to Python, `javascript.json` to JavaScript etc.).

## QuickSnip

I have no relation to the project, I just liked it.

[Click here to check it out](https://github.com/dostonnabotov/quicksnip)

## License

This project is currently under a MIT [LICENSE](LICENSE)
