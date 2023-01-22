import csv
import json
import statistics

import datetime


#jun 19 21 -- nov 1 2022
#start at wordle 210
#feb 15 2022-- wordle 241, wordle & nyt wordle DIVERGE
wordle_answers = ["cigar", "rebut", "sissy", "humph", "awake", "blush", "focal", "evade", "naval", "serve", "heath", "dwarf", "model", "karma", "stink", "grade", "quiet", "bench", "abate", "feign", "major", "death", "fresh", "crust", "stool", "colon", "abase", "marry", "react", "batty", "pride", "floss", "helix", "croak", "staff", "paper", "unfed", "whelp", "trawl", "outdo", "adobe", "crazy", "sower", "repay", "digit", "crate", "cluck", "spike", "mimic", "pound", "maxim", "linen", "unmet", "flesh", "booby", "forth", "first", "stand", "belly", "ivory", "seedy", "print", "yearn", "drain", "bribe", "stout", "panel", "crass", "flume", "offal", "agree", "error", "swirl", "argue", "bleed", "delta", "flick", "totem", "wooer", "front", "shrub", "parry", "biome", "lapel", "start", "greet", "goner", "golem", "lusty", "loopy", "round", "audit", "lying", "gamma", "labor", "islet", "civic", "forge", "corny", "moult", "basic", "salad", "agate", "spicy", "spray", "essay", "fjord", "spend", "kebab", "guild", "aback", "motor", "alone", "hatch", "hyper", "thumb", "dowry", "ought", "belch", "dutch", "pilot", "tweed", "comet", "jaunt", "enema", "steed", "abyss", "growl", "fling", "dozen", "boozy", "erode", "world", "gouge", "click", "briar", "great", "altar", "pulpy", "blurt", "coast", "duchy", "groin", "fixer", "group", "rogue", "badly", "smart", "pithy", "gaudy", "chill", "heron", "vodka", "finer", "surer", "radio", "rouge", "perch", "retch", "wrote", "clock", "tilde", "store", "prove", "bring", "solve", "cheat", "grime", "exult", "usher", "epoch", "triad", "break", "rhino", "viral", "conic", "masse", "sonic", "vital", "trace", "using", "peach", "champ", "baton", "brake", "pluck", "craze", "gripe", "weary", "picky", "acute", "ferry", "aside", "tapir", "troll", "unify", "rebus", "boost", "truss", "siege", "tiger", "banal", "slump", "crank", "gorge", "query", "drink", "favor", "abbey", "tangy", "panic", "solar", "shire", "proxy", "point", "robot", "prick", "wince", "crimp", "knoll", "sugar", "whack", "mount", "perky", "could", "wrung", "light", "those", "moist", "shard", "pleat", "aloft", "skill", "elder", "frame", "humor", "pause", "ulcer", "ultra", "robin", "cynic", "aroma", "caulk", "shake", "dodge", "swill", "tacit", "other", "thorn", "trove", "bloke", "vivid", "spill", "chant", "choke", "rupee", "nasty", "mourn", "ahead", "brine", "cloth", "hoard", "sweet", "month", "lapse", "watch", "today", "focus", "smelt", "tease", "cater", "movie", "saute", "allow", "renew", "their", "slosh", "purge", "chest", "depot", "epoxy", "nymph", "found", "shall", "harry", "stove", "lowly", "snout", "trope", "fewer", "shawl", "natal", "comma", "foray", "scare", "stair", "black", "squad", "royal", "chunk", "mince", "shame", "cheek", "ample", "flair", "foyer", "cargo", "oxide", "plant", "olive", "inert", "askew", "heist", "shown", "zesty", "hasty", "trash", "fella", "larva", "forgo", "story", "hairy", "train", "homer", "badge", "midst", "canny", "fetus", "butch", "farce", "slung", "tipsy", "metal", "yield", "delve", "being", "scour", "glass", "gamer", "scrap", "money", "hinge", "album", "vouch", "asset", "tiara", "crept", "bayou", "atoll", "manor", "creak", "showy", "phase", "froth", "depth", "gloom", "flood", "trait", "girth", "piety", "payer", "goose", "float", "donor", "atone", "primo", "apron", "blown", "cacao", "loser", "input", "gloat", "awful", "brink", "smite", "beady", "rusty", "retro", "droll", "gawky", "hutch", "pinto", "gaily", "egret", "lilac", "sever", "field", "fluff", "hydro", "flack", "agape", "voice", "stead", "stalk", "berth", "madam", "night", "bland", "liver", "wedge", "augur", "roomy", "wacky", "flock", "angry", "bobby", "trite", "aphid", "tryst", "midge", "power", "elope", "cinch", "motto", "stomp", "upset", "bluff", "cramp", "quart", "coyly", "youth", "rhyme", "buggy", "alien", "smear", "unfit", "patty", "cling", "glean", "label", "hunky", "khaki", "poker", "gruel", "twice", "twang", "shrug", "treat", "unlit", "waste", "merit", "woven", "octal", "needy", "clown", "widow", "irony", "ruder", "gauze", "chief", "onset", "prize", "fungi", "charm", "gully", "inter", "whoop", "taunt", "leery", "class", "theme", "lofty", "tibia", "booze", "alpha", "thyme", "eclat", "doubt", "parer", "chute", "stick", "trice", "alike", "sooth", "recap", "saint", "liege", "glory", "grate", "admit", "brisk", "soggy", "usurp", "scald", "scorn", "leave", "twine", "sting", "bough", "marsh", "sloth", "dandy", "vigor", "howdy", "enjoy"]

def make_wordle_dates():
    res = {}
    i = 210
    day = datetime.datetime(2022, 1, 16)
    while i < 241:
        res[i] = datetime.date.strftime(day, "%Y-%m-%d")
        day = day + datetime.timedelta(days=1)
        i = i+1
    return res

dates = make_wordle_dates()

def passes_filter(row):
    #removes tweets without wordle board first
    tweet = row['tweet_text']
    if tweet[0:7] != "Wordle " and tweet[12:14] != "/6":
        return False
    elif row['tweet_date'] == "":
        return False
    elif int(row['wordle_id']) >= 241:
        return False

    return True


def create_tweet(row):
    tweet = {"text": '',
             "guesses": 0,
             "guess_matrix": []
            }
    text = row['tweet_text']
    guesses = int(text[11])
    guess_matrix = []
    row_i = 15+1 #first \n
    end_row = text.find("🟩🟩🟩🟩🟩")+5
    for i in range(6):
        guess_row = []
        if row_i < end_row:
            for i in range(5):
                box = text[row_i+i]
                if box == "⬛" or box == "⬜":
                    guess_row.append(0)
                elif box == "🟨":
                    guess_row.append(1)
                elif box == "🟩":
                    guess_row.append(2)
                else:
                    return None
        else:
            guess_row = [-1,-1,-1,-1,-1]

        guess_matrix.append(guess_row)
        row_i += 6

    tweet['text'] = text
    tweet['guesses'] = guesses
    tweet['guess_matrix'] = guess_matrix

    return tweet

info = {}
header = []
species = {}
with open('static/tweets.csv','r') as f:
    reader = csv.DictReader(f)

    header = reader.fieldnames

    for row in reader:
        if passes_filter(row):
            id = int(row['wordle_id'])
            tweet = create_tweet(row)
            if tweet:
                if id in info:
                    info[id]['tweets'].append(tweet['guesses'])
                    info[id]['dist'][tweet['guesses']-1] += 1
                else:
                    info[id] = {
                                'date': dates[id],
                                'tweets': [],
                                'dist':[0,0,0,0,0,0]
                                }
data = []
for id in info.keys():
    data.append({
        'id': id,
        'date': info[id]['date'],
        'answer': wordle_answers[id],
        'num_tweets': len(info[id]['tweets']),
        'mean': statistics.mean(info[id]['tweets']),
        'median': statistics.median(info[id]['tweets']),
        'mode': statistics.mode(info[id]['tweets']),
        'dist': info[id]['dist']
        # 'tweets': [tweet]
    })


    # new_fieldnames = header+['guesses','guess_matrix']
print(len(data))

# with open('combined-wordles.csv','w',newline="") as f:
with open('wordles_with_dist.json','w') as f:
    s_data = json.dump(data, f)
