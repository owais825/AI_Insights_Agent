def validate_result(result):
    if not isinstance(result, list):
        raise ValueError("Result must be a list")

    if len(result) == 0:
        print("Warning: Query returned empty result")