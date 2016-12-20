from nltk.tokenize import word_tokenize


# exemple_text= "Hello Mr. Smith, how are you doing today? How do you think python is? " +\ "Artificial intelligence
# (AI) is intelligence exhibited by machines. In computer science, an ideal intelligent machine is a flexible
# rational agent that perceives its environment and takes actions that maximize its chance of success at some goal.
# Colloquially, the term artificial intelligence is applied when a machine mimics cognitive functions that humans
# associate with other human minds, such as learning and problem solving. As machines become increasingly capable,
# mental facilities once thought to require intelligence are removed from the definition. For example,
# optical character recognition is no longer perceived as an exemplar of artificial intelligence, having become a
# routine technology. Capabilities currently classified as AI include successfully understanding human speech,
# competing at a high level in strategic game systems (such as Chess and Go ), self-driving cars, and interpreting
# complex data. Some people also consider AI a danger to humanity if it progresses unabatedly. AI research is divided
#  into subfields that focus on specific problems or on specific approaches or on the use of a particular tool or
# towards satisfying particular applications."


def list_of_sent(paragraph: str) -> list:
    from nltk.tokenize import sent_tokenize
    return sent_tokenize(paragraph)

    # print("LISTA DE PROPOZITII:")
    # for line in list_of_sent(exemple_text): print (line)
