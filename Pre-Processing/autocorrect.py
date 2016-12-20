import textblob


def auto_correct_input(m_input):
    if len(m_input) is not 0:
        result = textblob.TextBlob(m_input)
        return str(result.correct())
    else:
        return None
