import frappe

def capitalize(sentence):
    return (' ').join(map(lambda word: word[0].upper() + word[1:], sentence.split(' ')))


def validate(doc, method):
    doc.customer_name = capitalize(doc.customer_name)
    print(doc.customer_name)