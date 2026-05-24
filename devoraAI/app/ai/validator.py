def is_code_related(text: str) -> bool:
    """
    Checks if the user input contains programming-related keywords.
    """
    text_lower = text.lower()
    keywords = [
        # Languages
        "python", "javascript", "typescript", "java", "c++", "sql", "swift", 
        "rust", "go", "ruby", "dart", "haskell", "ocaml", "yaml", "bash",
        "php", "kotlin", "scala", "c#", "golang", "r", "perl", "lua",
        # Frameworks / Libraries
        "vue", "react", "angular", "fastapi", "django", "flask", "express",
        "node.js", "spring", "laravel", "pandas", "numpy", "tensorflow",
        # Web / Core Concepts
        "html", "css", "json", "xml", "csv", "regex", "api", "rest", "graphql",
        "oauth", "docker", "kubernetes", "git", "linux", "ubuntu",
        # Programming terminologies
        "function", "class", "variable", "array", "object", "database", 
        "query", "loop", "async", "await", "promise", "list", "dict", "string",
        "compile", "debug", "error", "exception", "bug", "syntax", "pointer",
        "algorithm", "sort", "search", "tree", "graph", "script", "code"
    ]
    
    # Check if any keyword exists as a word in the text
    # A simple substring check might trigger false positives on words like "class", "rest", "go", 
    # but for an AI chat context, we can check basic boundaries or just substrings.
    # Let's use simple tokenization to ensure words like "go" or "r" don't randomly match substrings.
    import re
    tokens = set(re.findall(r'\b\w+\b', text_lower))
    
    for kw in keywords:
        # If keyword is purely alphabetical, check token match
        if re.match(r'^\w+$', kw):
            if kw in tokens:
                return True
        else:
            # For keywords with special characters like c++, node.js
            if kw in text_lower:
                return True
                
    return False
