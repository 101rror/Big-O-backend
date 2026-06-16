from typing import Dict, List

SUPPORTED_LANGUAGES = ["c", "cpp", "python", "java", "javascript"]
LANGUAGE_LABELS = {
    "c": "C",
    "cpp": "C++",
    "python": "Python",
    "java": "Java",
    "javascript": "JavaScript",
}

LANGUAGE_INVALID_PATTERNS: Dict[str, List[str]] = {
    "c": [
        "std::",
        "cout",
        "cin",
        "vector<",
        "map<",
        "StringBuilder",
        "System.out",
        "console.",
        "def ",
        "function ",
        "import java",
        "public class",
        "console.log",
    ],
    "cpp": [
        "def ",
        "function ",
        "import java",
        "public class",
        "System.out",
        "console.",
        "console.log",
    ],
    "python": [
        "std::",
        "cout",
        "cin",
        "vector<",
        "map<",
        "#include",
        "using namespace",
        "System.out",
        "public class",
        "console.",
        "console.log",
        "import java",
    ],
    "java": [
        "std::",
        "cout",
        "cin",
        "vector<",
        "#include",
        "using namespace",
        "console.",
        "console.log",
        "def ",
        "function ",
        "import java\.lang",
    ],
    "javascript": [
        "std::",
        "cout",
        "cin",
        "vector<",
        "#include",
        "using namespace",
        "System.out",
        "public class",
        "def ",
        "function ",
        "import java",
    ],
}

PROMPT_BASE = (
    "You are a Big-O complexity analyzer.\n\n"
    "STRICT RULES:\n"
    "- Analyze ONLY in the requested programming language.\n"
    "- NEVER guess the language automatically.\n"
    "- NEVER mention other languages or unrelated standard library APIs.\n"
    "- Suggestions must be language-specific.\n"
    "- Output valid JSON only and nothing else.\n"
    "- Do not include markdown, code fences, or explanation outside JSON.\n\n"
    "Respond with a single JSON object matching the schema below.\n"
    "Schema:\n"
    "{\n"
    '  "timeComplexity": "...",\n'
    '  "spaceComplexity": "...",\n'
    '  "explanation": {\n'
    '    "time": "...",\n'
    '    "space": "..."\n'
    "  },\n"
    '  "suggestions": ["..."],\n'
    '  "confidence": 0.0\n'
    "}\n\n"
)

LANGUAGE_PROMPT_OVERRIDES: Dict[str, str] = {
    "c": (
        "For C code:\n"
        "- Analyze the code as plain C.\n"
        "- Do not use C++ syntax, STL, or std:: identifiers.\n"
        "- Keep suggestions tied to C features like pointers, arrays, loops, and memory usage.\n"
    ),
    "cpp": (
        "For C++ code:\n"
        "- Analyze the code as C++.\n"
        "- Use C++ terminology and standard library details when relevant.\n"
        "- Avoid referring to Java, Python, or JavaScript idioms.\n"
    ),
    "python": (
        "For Python code:\n"
        "- Analyze the code as Python.\n"
        "- Use Python-specific libraries, idioms, and syntax.\n"
        "- Avoid C/C++/Java/JavaScript keywords and libraries.\n"
    ),
    "java": (
        "For Java code:\n"
        "- Analyze the code as Java.\n"
        "- Use Java-specific classes, JVM considerations, and language idioms.\n"
        "- Avoid Python, C/C++, or JavaScript syntax and APIs.\n"
    ),
    "javascript": (
        "For JavaScript code:\n"
        "- Analyze the code as JavaScript.\n"
        "- Use JS idioms, browser/node conventions, and JavaScript-specific APIs.\n"
        "- Avoid Java, Python, and C/C++ syntax or standard library references.\n"
    ),
}


def build_prompt(language: str, code: str) -> str:
    language_name = LANGUAGE_LABELS.get(language, "Unknown")
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {language}")

    return (
        PROMPT_BASE
        + f"Programming Language: {language_name}\n\n"
        + LANGUAGE_PROMPT_OVERRIDES[language]
        + "Analyze this code exactly as written below.\n\n"
        + "Code:\n"
        + code.strip()
        + "\n"
    )


def validate_response(language: str, raw_text: str, parsed_response: dict) -> None:
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language for validation: {language}")

    invalid_tokens = LANGUAGE_INVALID_PATTERNS.get(language, [])
    normalized_text = raw_text or ""
    normalized_text += " " + str(parsed_response)

    lower_text = normalized_text.lower()
    for token in invalid_tokens:
        if token.lower() in lower_text:
            raise ValueError(
                f"Language validation failed for {LANGUAGE_LABELS[language]}: found forbidden token '{token}'."
            )
