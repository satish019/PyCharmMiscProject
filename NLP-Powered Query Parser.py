import spacy
nlp = spacy.load('en_core_web_sm')
def parse_user_input(user_input):
    doc = nlp(user_input)
    keywords = [token.text.lower() for token in doc if token.is_alpha]

    if "supplier" in keywords:
        return "SELECT * FROM suppliers;"
    elif "product" in keywords:
        return "SELECT * FROM products;"
    else:
        return None