from random import randint

# constants
MIDDLE_FINGER_GORILLA_URL = "http://3.bp.blogspot.com/-s3eobLzuVm0/Twxkz6yOe_I/AAAAAAAACHg/wxDw-nWa_eU/s1600/Funny+Gorilla5.jpg"
SHOCKED_MONKEY_URL = "https://s-media-cache-ak0.pinimg.com/736x/86/53/41/8653410a1ee96e3ac9bb22b4ed08c556.jpg"
LAUGHING_GORILLA_URL = "https://tigerlilytoph.files.wordpress.com/2012/01/laughing-gorilla.jpg"
LAUGHING_GORILLA_URL2 = "http://www.onlygod365.com/wp-content/uploads/2013/02/LaughingGorilla1.jpg"
LAUGHING_GORILLA_URL3 = "http://static.squarespace.com/static/51806e5ae4b0809658b411ef/t/51bd2aa9e4b0cc528082c718/1371351722080/HAHA-Gorilla.jpg?format=500w"
LAUGHING_GORILLA_URL4 = "http://myfunnypics.org/main.php?g2_view=core.DownloadItem&g2_itemId=736&g2_serialNumber=2"
LAUGHING_GORILLA_URL5 = "http://www.zooborns.com/.a/6a010535647bf3970b01310f6b78be970c-600wi"
LAUGHING_GORILLA_URL6 = "https://pbs.twimg.com/media/CIWeyDEUwAAs_AO.jpg"
LOVE_GORILLA_URL = "https://arigorillatrekking.files.wordpress.com/2014/02/gorilal-love.jpg"
THUMBS_UP_GORILLA = "http://gorillaloveproject.org/files/files/gorilla.jpg"
NO_PROBLEM_GORILLA = "http://www.animalsbase.com/wp-content/uploads/2015/10/Powerful-Gorilla-Lifts-Fist-Looks-At-Photographer.jpg"

LAUGHING_GORILLAS = [LAUGHING_GORILLA_URL, LAUGHING_GORILLA_URL2, LAUGHING_GORILLA_URL3, LAUGHING_GORILLA_URL4, LAUGHING_GORILLA_URL5, LAUGHING_GORILLA_URL6]

JOKE_QUESTIONS = ["What do you call an angry monkey?",
                  "What do you call a monkey that sells potato chips?",
                  "Where do monkeys go to drink?",
                  "Why do monkeys like bananas?",
                  "Where should a monkey go when he loses his tail?",
                  "Why should you never fight with a monkey?",
                  "Where do chimps get their gossip?",
                  "What do you call a baby monkey?"]

JOKE_ANSWERS = ["Furious George.",
                "A chipmunk.",
                "The monkey bars.",
                "Because they have appeal.",
                "To a retailer!",
                "They use gorilla warfare.",
                "Through the ape vine.",
                "A chimp off the old block."]

HARAMBOT = "Harambot 🍌"
HARAMBOT_DEV = "Harambot-Dev"

def is_message_a_greeting(message):
    msg = message.content.lower()
    if "hi" in msg or "hello" in msg or "hey" in msg or "sup " in msg or "whats up" in msg or "yo " in msg or "what's up" in msg:
        return True
    else:
        return False

def is_message_a_thank_you(message):
    msg = message.content.lower()
    if "thanks" in msg or "thank you" in msg or "thank ya" in msg or "ty" == msg or "ty " in msg or "thx" in msg:
        return True
    else:
        return False

def did_mention_harambot(client, message):
    s = ""
    for m in message.mentions:
        if m.name == HARAMBOT:
            return True
    return False


async def tell_joke(client, message):
    rand = randint(0,len(JOKE_QUESTIONS)-1)
    await client.send_message(message.channel, ":monkey: " + JOKE_QUESTIONS[rand] + " :monkey:") # need random number

    def add_check(msg):
        print(msg.content in JOKE_ANSWERS[rand].lower())
        return msg.content in JOKE_ANSWERS[rand].lower() and len(msg.content) > 0.5 * len(JOKE_ANSWERS[rand])

    msg = await client.wait_for_message(timeout=8, author=message.author, check=add_check)

    if msg is None:
        await client.send_message(message.channel, ":monkey_face: " + JOKE_ANSWERS[rand] + " :monkey_face:\n\n" + LAUGHING_GORILLAS[randint(0,len(LAUGHING_GORILLAS)-1)])
    else:
        await client.send_message(message.channel, ":banana: Correct! + 50 EP, " + message.author.name + " :banana:\n\n" + THUMBS_UP_GORILLA)
