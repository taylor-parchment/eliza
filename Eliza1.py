import random
import re
import time

# all keywords and phrases to search for
desire = re.compile(r'(\W|^)(want|need|would like|desire|crave)(\W|$)', re.IGNORECASE)
greeting  = re.compile(r'(\W|^)(hello|hi|hey|good morning|good afternoon|good evening)(\W|$)', re.IGNORECASE)
feeling = re.compile(r'(\W|^)(i feel|i love|i hate|feeling)(\W|$)', re.IGNORECASE)
emotion = re.compile(r'(\W|^)(love|hate|happy|sad|upset|depressed|anxious|manic)(\W|$)', re.IGNORECASE)
family = re.compile(r'''(\W|^)
(dad|father|mom|mother|brother|sister|girlfriend|boyfriend|wife|husband|spouse|son|daughter|cousin)
(\W|$)''', re.IGNORECASE | re.VERBOSE)

first_person = re.compile(r'(\W|^)(i|i\'m|me|my|mine)(\W|$)', re.IGNORECASE)
second_person = re.compile(r'(\W|^)(you|you\'re|your|yours)(\W|$)', re.IGNORECASE)

regexes = [greeting, feeling, desire, emotion, family] # list of all regex categories

name = "unknown"


def typing():
    print("Typing...")
    time.sleep(random.random() * 3) # wait 0 - 3 seconds for Eliza to "type"


def get_name(): # ask for name and return a response to be printed
    global name
    name = input("What's your name?\n")
    typing()
    return random.choice([
        f'Okay, got it. Your name is "{name}".',
        f'Your name is "{name}". I\'ll keep that in mind.'
        ])


def get_random_response(): # last resort responses
    return random.choice([
        "Why do you say that?",
        "What do you mean?",
        "Explain.",
        "How do you feel about that?",
        "What makes you think of that?"
    ])


# parameters - category of first regex matched, input of user
# returns random response based on regex category
def get_response(regex, userin):
    global name
    match = regex.search(userin).group(2).lower()
    if regex == desire:
        reply = random.choice([
            f'Can you tell me why you say "{userin.capitalize()}"?',
            "What would you gain in achieving this?",
            "Are you certain you " + match + " this?"
        ])

    if regex == greeting:
        if name == "unknown":
            reply = f"{get_name()}\nHow do you feel {name}?"
        else:
            reply = random.choice([
                match.capitalize() + ', ' + name,
                "Yes, " + name + ", we've already introduced."
            ])

    if regex == feeling:
        if match == "i feel" or match == "feeling":
            reply = random.choice([
                "Tell me more about how you feel.",
                "Describe this feeling in more detail."
            ])
        if match == "i love":
            reply = random.choice([
                "Tell me more about what you love.",
                "What makes you feel love?"
            ])
        if match == "i hate":
            reply = random.choice([
                "Why do you feel hate?",
                "Tell me more about feeling hateful.",
                "What else do you hate?"
            ])

    if regex == emotion:
        reply = random.choice([
            f"Tell me about feeling {match}.",
            f"Do you feel {match} often?",
            f"Tell me about a time you felt {match}."
        ])

    if regex == family:
        reply = random.choice([
            f"Tell me about your relationship with your {match}.",
            f"Do you normally get along with your {match}?",
            f"Do you truly love your {match}?"
        ])

    return reply


def main():
    previous_inp = ''
    print('Type "exit" to quit.')
    userin = input("Hi, I'm your therapist, Bad Eliza.\n")
    while userin != 'exit':
        found_response = False
        test_str = userin.lower().strip(".,!?;: ")
        selection = []
        for regex in regexes: # look through regex list, add them to list of matches
            if regex.search(userin) is not None:
                selection.append(regex)
                found_response = True

        if greeting in selection: # prioritize greeting match, get response
            typing()
            print(get_response(greeting, userin))

        elif found_response: # otherwise, if there are multiple matches, pick a random one
            typing()
            print(get_response(random.choice(selection), userin))

        else: # if there were no matches

            if userin.strip() == "": # when user enters blank response
                print(random.choice([
                    "...",
                    "Yes?",
                    "I'm sorry?"]))

            # if the input uses more 2nd person pronouns than 1st person
            elif len(second_person.findall(userin)) > len(first_person.findall(userin)):
                typing()
                print(random.choice([
                    "Let's keep the conversation about you.",
                    "Why don't you tell me more about you.",
                    "I would rather talk about you.",
                    "We're not here to talk about me."
                ]))

            # if the user only enters yes or no, mention their last response if it wasn't also yes or no
            elif (test_str == 'yes' or test_str == 'no') and previous_inp != 'yes' and previous_inp != 'no':
                typing()
                print('"' + previous_inp + '", you said. Tell me more about that.')

            else: # get a last resort, random response
                typing()
                print(get_random_response())

        previous_inp = userin
        userin = input()


if __name__ == "__main__":
    main()