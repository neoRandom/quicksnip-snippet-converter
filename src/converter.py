""" Structure:

From:
<category: str>
<title: str>
<description: str>
<tags: list[str]>
<author: str>

<code: list[str]>

To:
{
    "categoryName": <category: str>,
    "snippets": [
        {
            "title": <title: str>,
            "description": <description: str>,
            "code": <code: list[str]>,
            "tags": <tags: list[str]>,
            "author": <author: str>
        }
    ]
}

Notes:
- Identify the programming language by the file extension


To do:
- Split the code into multiple files
- Support more than one snippet per category (like getting a dir name instead of file name)

"""

from pydantic import BaseModel, RootModel
import sys
import os


DEFAULT_LANGUAGE = "python"
RECOGNIZED_LANGUAGES = {
    "py": "python",
    "js": "javascript"
}
INDENT_SIZE = 2


class Snippet(BaseModel):
    title: str
    description: str
    code: list[str]
    tags: list[str]
    author: str

class Category(BaseModel):
    categoryName: str
    snippets: list[Snippet]

class JSONModel(RootModel):
    root: list[Category]


def get_code_lang(file_path: str):
    if file_path.count("/") == 0:
        file_path = "./" + file_path
    
    file_name = file_path.split("/")[-1]

    if file_path.count(".") == 0:
        return None
    
    file_extension = file_name.split(".")[-1]

    return RECOGNIZED_LANGUAGES.get(file_extension, None)


def get_file_content(file_path: str):
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise FileNotFoundError(f"Error: File `{file_path}` not found")
    
    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"Error: File `{file_path}` is not readable")
    
    with open(file_path, "r", encoding="UTF-8") as file:
        content = file.read()

    return content


def format_metadata(line: str):
    return line.replace("//", "", 1).replace("#", "", 1).strip()

def parse_code(code: str, *, category: Category | None = None):
    code_lines = code.split("\n")

    if len(code_lines) < 7:
        raise SyntaxError("Error: Invalid code syntax.\nIt needs to have at least 7 lines (5 metadata, 1 empty line and at least 1 LOC)")
    
    # Set up the basic info
    # 0 - Category; 1 - Title; 2 - Description; 3 - Tags (separed by comma); 4 - Author
    snippet = Snippet.model_construct()
    snippet.title = format_metadata(code_lines[1])
    snippet.description = format_metadata(code_lines[2])
    snippet.code = []
    snippet.tags = [tag.strip() for tag in format_metadata(code_lines[3]).split(",")]  # Split by the commas and strip each element
    snippet.author = format_metadata(code_lines[4])

    # Get the lines of code (considering empty lines and comments)
    for line in code_lines[6:]:
        snippet.code.append(line)

    # Put the snippet inside a category
    if category is None:
        category = Category.model_construct()
        category.categoryName = format_metadata(code_lines[0])
        category.snippets = []

    category.snippets.append(snippet)

    return category


def save_category_to_json(category_object: Category, *, lang: str):
    json_content: JSONModel
    dump_content: str = ""
    output_filename = f"{lang}.json"

    # Get the root model (list of categories)
    if os.path.exists(output_filename) and os.path.isfile(output_filename):
        with open(output_filename, "r", encoding="UTF-8") as json_file:
            json_content = JSONModel.model_validate_json(json_file.read())

        # Verify if there is already a category with the same name
        for category in json_content.root:
            if category.categoryName != category_object.categoryName:
                continue

            # Add the snippets
            for snippet in category_object.snippets:
                category.snippets.append(snippet)

            break  # <- Skip the else
        else:
            json_content.root.append(category_object)
        
    else:
        json_content = JSONModel.model_construct([category_object])

    # Convert the object into JSON and then save it
    dump_content = json_content.model_dump_json(indent=INDENT_SIZE)

    with open(output_filename, "w", encoding="UTF-8") as json_file:
        json_file.write(dump_content)


def run():
    if len(sys.argv) < 2:
        print(f"Usage:\n{sys.argv[0]} <file path> <language (optional)>")
        return

    # Get the file content
    try:
        content = get_file_content(sys.argv[1])
    except Exception as e:
        print(e)
        return
    
    # Get the language
    code_lang = get_code_lang(sys.argv[1])

    if code_lang is None:
        if len(sys.argv) < 3:
            print("Warning: Programming language not defined. Using default (Python)")
            code_lang = DEFAULT_LANGUAGE
        else:
            code_lang = sys.argv[2]

    # Convert the file content into a JSON-Convertable object (pydantic BaseModel child class)
    try:
        converted_code_category = parse_code(content)
    except Exception as e:
        print(e)
        return
    
    # Save the object as json
    try:
        save_category_to_json(converted_code_category, lang=code_lang.lower())
    except Exception as e:
        print(e)


if __name__ == "__main__":
    run()
