def validate_sql(query: str):
    # Basic safety check (you can expand later)
    forbidden = ["DROP", "DELETE", "UPDATE", "INSERT"]
    
    for word in forbidden:
        if word in query.upper():
            raise ValueError(f"Unsafe SQL detected: {word}")