def title_to_alias(input_text):
    title_underscores = input_text.lower().replace("-", "_").replace(" ", "_")
    parts = title_underscores.split('_', 5)
    # If we have less than 6 parts, it means there weren't 5 underscores, return the original string
    if len(parts) < 6:
        return title_underscores
    # Join the parts back together with underscores
    return '_'.join(parts[:5])
