import spacy
# Load the Romanian model
nlp = spacy.load("ro_core_news_sm")

def title_to_alias(input_text):
    title_underscores = input_text.lower().replace("-", "_").replace(" ", "_")
    parts = title_underscores.split('_', 5)
    # If we have less than 6 parts, it means there weren't 5 underscores, return the original string
    if len(parts) < 6:
        return title_underscores
    # Join the parts back together with underscores
    return '_'.join(parts[:5])



# Define a function to correct splits using spaCy
def correct_splits(text):
    # Process the text using spaCy
    doc = nlp(text)
    corrected_text = ""
    previous_token = None
    for token in doc:
        # If the previous token ends with a hyphen, and the current token is not punctuation
        if previous_token and previous_token.text.endswith('-') and not token.is_punct:
            corrected_text = corrected_text.rstrip(previous_token.text + ' ')
            corrected_text += previous_token.text.rstrip('-') + token.text + ' '
        else:
            corrected_text += token.text_with_ws
        previous_token = token
    return corrected_text
