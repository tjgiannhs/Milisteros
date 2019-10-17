"""
Statement pre-processors.
"""

def seperate_sentences(statement):
    '''
    Adds a space after commas and dots to seperate sentences
    If this results in more than one spaces after them another pre-processor will clean them up later

    :param statement: the input statement, has values such as text
    :return: the statement with the modified text
    '''

    statement.text = statement.text.replace(",",", ")
    statement.text = statement.text.replace(".",". ")
    return statement

def capitalize(statement):
    '''
    Makes the first letter after dots capital
    Adds a dot at the end if no other punctuation exists already

    :param statement: the input statement, has values such as text
    :return: the statement with the modified text
    '''

    text = ""
    for protash in statement.text.split('.'):
        text = text + protash.strip().capitalize() +"."
    if text[-2]=="." or text[-2]=="!" or text[-2]=="?" or text[-2]==";":
        statement.text = text[:-1]
    else:
        statement.text = text
    return statement

def clean_apostrophes(statement):
    '''
    Removes apostrophes, both single and double
    Uses a different way to remove the double because replace wouldn't work correctly with them

    :param statement: the input statement, has values such as text
    :return: the statement with the modified text
    '''

    text = ""
    statement.text = statement.text.replace("'","")
    for protash in statement.text.split('"'):
        text = text+protash

    statement.text = text

    return statement