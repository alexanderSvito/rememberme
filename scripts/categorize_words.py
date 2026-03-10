#!/usr/bin/env python3
"""
Categorize the scraped en-fr.json words into themed packs.
Uses keyword heuristics to assign categories, with a priority system
so the most useful everyday categories come first.
"""
import json
import re
import os

with open('en-fr.json') as f:
    words = json.load(f)

# Category definitions: (name, priority, keyword_patterns)
# Lower priority number = shown first to the user
CATEGORIES = [
    ("greetings", 1, [
        r"hello", r"goodbye", r"good morning", r"good evening", r"good night",
        r"how are you", r"my name is", r"nice to meet", r"see you", r"hi\b",
        r"bye\b", r"salut", r"bonjour", r"please", r"thank", r"sorry",
        r"excuse me", r"you're welcome", r"enchant",
    ]),
    ("numbers", 1, [
        r"^one$", r"^two$", r"^three$", r"^four$", r"^five$", r"^six$",
        r"^seven$", r"^eight$", r"^nine$", r"^ten$", r"^eleven$", r"^twelve$",
        r"thirteen", r"fourteen", r"fifteen", r"sixteen", r"seventeen",
        r"eighteen", r"nineteen", r"twenty", r"thirty", r"forty", r"fifty",
        r"sixty", r"seventy", r"eighty", r"ninety", r"hundred", r"thousand",
        r"million", r"^zero$", r"first$", r"second$", r"third$",
    ]),
    ("family", 2, [
        r"family", r"father", r"mother", r"brother", r"sister", r"son\b",
        r"daughter", r"husband", r"wife", r"parent", r"baby", r"child",
        r"grandm", r"grandf", r"grandp", r"uncle", r"aunt", r"nephew",
        r"niece", r"cousin", r"sibling", r"in-law", r"step-", r"half-",
    ]),
    ("food_drink", 2, [
        r"bread", r"cheese", r"meat", r"chicken", r"fish\b", r"rice",
        r"pasta", r"soup", r"salad", r"cake", r"fruit", r"vegetable",
        r"apple", r"banana", r"orange(?!.*color)", r"tomato", r"potato",
        r"onion", r"carrot", r"pepper\b", r"salt\b", r"sugar\b",
        r"butter", r"milk", r"coffee", r"tea\b", r"water\b", r"wine",
        r"beer", r"juice", r"egg\b", r"steak", r"beef", r"pork",
        r"lamb\b", r"mutton", r"sausage", r"veal", r"duck\b",
        r"rabbit\b", r"lemonade", r"latte", r"cappuccino", r"sparkling",
        r"still water", r"tap water", r"snail", r"oyster", r"prawn",
        r"shrimp", r"lobster", r"mussel", r"crab", r"salmon", r"tuna",
        r"strawberr", r"raspberr", r"cherr", r"peach", r"pear\b",
        r"grape", r"lemon", r"melon", r"pineapple", r"plum",
        r"mushroom", r"lettuce", r"cucumber", r"bean", r"pea\b",
        r"corn\b", r"garlic", r"herb", r"spice", r"flour",
        r"dessert", r"ice cream", r"chocolate", r"biscuit", r"pastry",
        r"croissant", r"jam\b", r"honey", r"cream\b", r"yoghurt",
        r"cereal", r"breakfast", r"lunch", r"dinner", r"meal",
        r"snack", r"starter", r"main course", r"dish\b",
        r"a drink", r"a carafe", r"a jug",
    ]),
    ("colors", 2, [
        r"green\b", r"blue\b", r"white\b", r"red\b", r"black\b",
        r"pink\b", r"grey\b", r"purple\b", r"yellow\b", r"brown\b",
        r"orange\b.*(?:color|colour)", r"^orange$",
    ]),
    ("time_calendar", 2, [
        r"monday", r"tuesday", r"wednesday", r"thursday", r"friday",
        r"saturday", r"sunday", r"january", r"february", r"march",
        r"april", r"may\b", r"june", r"july", r"august", r"september",
        r"october", r"november", r"december", r"morning", r"afternoon",
        r"evening", r"night\b", r"today", r"tomorrow", r"yesterday",
        r"week\b", r"month\b", r"year\b", r"hour\b", r"minute\b",
        r"second\b.*time", r"season", r"spring\b", r"summer\b",
        r"autumn", r"winter\b", r"midnight", r"noon\b", r"midday",
        r"after\b", r"before\b", r"then\b", r"next\b", r"finally\b",
        r"o'clock", r"half past", r"quarter",
    ]),
    ("common_verbs", 3, [
        r"^to\s", r"to be\b", r"to have\b", r"to do\b", r"to go\b",
        r"to come\b", r"to say\b", r"to make\b", r"to take\b",
        r"to give\b", r"to know\b", r"to want\b", r"to see\b",
        r"to eat\b", r"to drink\b", r"to sleep\b", r"to read\b",
        r"to write\b", r"to speak\b", r"to listen\b", r"to watch\b",
        r"to buy\b", r"to sell\b", r"to work\b", r"to play\b",
        r"to live\b", r"to like\b", r"to love\b", r"to hate\b",
        r"to think\b", r"to believe\b", r"to understand\b",
        r"to learn\b", r"to teach\b", r"to study\b",
        r"to open\b", r"to close\b", r"to start\b", r"to finish\b",
        r"to wait\b", r"to find\b", r"to look\b", r"to put\b",
        r"to run\b", r"to walk\b", r"to sit\b", r"to stand\b",
    ]),
    ("body_health", 3, [
        r"head\b", r"hand\b", r"arm\b", r"leg\b", r"foot\b", r"feet\b",
        r"eye\b", r"ear\b", r"nose\b", r"mouth\b", r"tooth", r"teeth",
        r"hair\b", r"face\b", r"neck\b", r"back\b.*body", r"stomach",
        r"heart\b", r"finger", r"knee\b", r"shoulder", r"chest\b",
        r"throat\b", r"lip\b", r"tongue\b", r"skin\b", r"bone\b",
        r"blood\b", r"doctor", r"hospital", r"medicine", r"ill\b",
        r"sick\b", r"pain\b", r"headache", r"fever", r"cold\b.*illness",
        r"cough", r"flu\b", r"allerg", r"pharmacy", r"chemist",
        r"appointment", r"prescription",
    ]),
    ("house_home", 3, [
        r"house\b", r"flat\b", r"apartment", r"room\b", r"kitchen",
        r"bedroom", r"bathroom", r"living room", r"dining room",
        r"garden\b", r"garage\b", r"door\b", r"window\b", r"wall\b",
        r"floor\b", r"roof\b", r"stair", r"furniture", r"table\b",
        r"chair\b", r"bed\b", r"sofa\b", r"cupboard", r"wardrobe",
        r"shelf", r"lamp\b", r"mirror\b", r"carpet\b", r"curtain",
        r"fridge", r"oven\b", r"washing machine", r"dishwasher",
        r"microwave", r"towel\b", r"soap\b", r"shampoo",
    ]),
    ("clothes", 3, [
        r"shirt\b", r"trousers", r"dress\b", r"skirt\b", r"jacket\b",
        r"coat\b", r"hat\b", r"shoe\b", r"boot\b", r"sock\b",
        r"glove", r"scarf\b", r"belt\b", r"tie\b", r"jumper",
        r"sweater", r"cardigan", r"jeans\b", r"shorts\b", r"suit\b",
        r"uniform\b", r"pyjama", r"underwear", r"underpant", r"sandal",
        r"cap\b", r"waistcoat", r"sleeve",
    ]),
    ("school_education", 3, [
        r"school\b", r"class\b", r"lesson\b", r"teacher\b", r"student",
        r"pupil\b", r"homework", r"exam\b", r"test\b.*school",
        r"notebook\b", r"book\b", r"pen\b", r"pencil\b", r"ruler\b",
        r"rubber\b", r"eraser\b", r"pencil case", r"sharpener",
        r"highlighter", r"felt pen", r"subject\b", r"maths\b",
        r"algebra", r"geometry", r"science\b", r"chemistry",
        r"physics\b", r"biology", r"history\b", r"geography",
        r"philosophy", r"music\b", r"art\b", r"language",
        r"school bag", r"board\b.*school", r"binder", r"fountain pen",
        r"break.*recess", r"tipp-ex",
    ]),
    ("travel_transport", 4, [
        r"car\b", r"bus\b", r"train\b", r"plane\b", r"boat\b",
        r"ship\b", r"bicycle", r"bike\b", r"taxi\b", r"metro\b",
        r"underground", r"station\b", r"airport\b", r"ticket\b",
        r"passport\b", r"luggage", r"suitcase", r"hotel\b",
        r"reception\b", r"key\b.*hotel", r"full board", r"half board",
        r"lift\b", r"map\b", r"journey", r"trip\b", r"travel",
        r"flight\b", r"platform\b", r"departure", r"arrival",
        r"motorway", r"highway", r"road\b", r"bridge\b",
        r"coast\b", r"lighthouse", r"beach\b", r"sand\b",
        r"sun cream", r"bucket\b", r"spade\b",
    ]),
    ("town_places", 4, [
        r"town\b", r"city\b", r"village\b", r"shop\b", r"store\b",
        r"market\b", r"supermarket", r"bakery", r"butcher",
        r"restaurant\b", r"café\b", r"cinema\b", r"theatre\b",
        r"museum\b", r"library\b", r"church\b", r"hospital\b",
        r"park\b", r"castle\b", r"gallery\b", r"office\b",
        r"bank\b", r"post office", r"police\b", r"fire station",
        r"swimming pool", r"shopping centre", r"centre-ville",
        r"tourist office",
    ]),
    ("sports_hobbies", 4, [
        r"football", r"soccer", r"basketball", r"tennis\b", r"rugby",
        r"swimming\b", r"cycling", r"running\b", r"golf\b",
        r"badminton", r"table.tennis", r"ping.pong", r"cricket\b",
        r"hockey\b", r"gymnastics", r"boxing\b", r"archery",
        r"fencing\b", r"climbing\b", r"horse riding", r"judo\b",
        r"skiing\b", r"skating\b", r"surfing\b", r"sailing\b",
        r"fishing\b.*sport", r"hobby", r"game\b", r"sport\b",
        r"team\b", r"match\b", r"player\b", r"coach\b",
    ]),
    ("technology", 4, [
        r"computer\b", r"laptop\b", r"screen\b", r"keyboard\b",
        r"mouse mat", r"headphone", r"speaker\b", r"earphone",
        r"usb\b", r"printer\b", r"to print\b", r"internet\b",
        r"website\b", r"email\b", r"phone\b", r"mobile\b",
        r"tablet\b", r"app\b", r"download", r"upload",
        r"password", r"wifi\b", r"bluetooth", r"charger",
        r"log in", r"sign in", r"landline",
    ]),
    ("emotions_personality", 4, [
        r"happy\b", r"sad\b", r"angry\b", r"tired\b", r"afraid\b",
        r"scared\b", r"surprised\b", r"excited\b", r"bored\b",
        r"worried\b", r"nervous\b", r"proud\b", r"jealous\b",
        r"shy\b", r"kind\b", r"generous\b", r"brave\b", r"lazy\b",
        r"honest\b", r"patient\b", r"polite\b", r"rude\b",
        r"funny\b", r"serious\b", r"clever\b", r"stupid\b",
        r"love\b", r"fear\b", r"pleasure\b", r"horror\b",
        r"surprise\b", r"tiredness", r"laugh\b", r"unhappy",
        r"tiring\b", r"to feel\b", r"to hope\b", r"to hate\b",
        r"to prefer\b", r"to shout\b",
    ]),
    ("nationalities_countries", 5, [
        r"german\b", r"french\b", r"italian\b", r"spanish\b",
        r"english\b", r"british\b", r"american\b", r"chinese\b",
        r"japanese\b", r"russian\b", r"scottish\b", r"irish\b",
        r"welsh\b", r"dutch\b", r"belgian\b", r"swiss\b",
        r"canadian\b", r"australian\b", r"african\b", r"asian\b",
        r"european\b", r"moroccan\b", r"algerian\b", r"tunisian\b",
        r"senegalese\b", r"cameroonian\b", r"ivorian\b",
        r"france\b", r"germany\b", r"spain\b", r"italy\b",
        r"england\b", r"ireland\b", r"scotland\b", r"wales\b",
        r"netherlands\b", r"belgium\b", r"switzerland\b",
        r"canada\b", r"australia\b", r"china\b", r"japan\b",
        r"russia\b", r"morocco\b", r"algeria\b", r"tunisia\b",
        r"senegal\b", r"cameroon\b", r"ivory coast",
        r"ukraine\b", r"ukrainian\b", r"polish\b", r"poland\b",
        r"portuguese\b", r"portugal\b", r"greek\b", r"greece\b",
        r"turkish\b", r"turkey\b.*country", r"india\b", r"indian\b",
    ]),
    ("jobs_professions", 5, [
        r"doctor\b", r"nurse\b", r"teacher\b", r"lawyer\b",
        r"engineer\b", r"police", r"firefighter", r"soldier\b",
        r"pilot\b", r"driver\b", r"chef\b", r"waiter\b",
        r"waitress\b", r"actor\b", r"actress\b", r"singer\b",
        r"musician\b", r"artist\b", r"writer\b", r"journalist\b",
        r"dentist\b", r"vet\b", r"farmer\b", r"baker\b",
        r"butcher\b.*person", r"plumber\b", r"electrician\b",
        r"mechanic\b", r"accountant\b", r"secretary\b",
        r"manager\b", r"director\b", r"novelist\b", r"cartoonist",
        r"applicant", r"career\b", r"job\b", r"profession\b",
        r"salary\b", r"employee\b", r"employer\b",
    ]),
    ("weather_nature", 5, [
        r"weather\b", r"sun\b", r"rain\b", r"snow\b", r"wind\b",
        r"cloud\b", r"storm\b", r"fog\b", r"ice\b", r"hot\b",
        r"cold\b", r"warm\b", r"cool\b", r"temperature\b",
        r"forecast\b", r"thunder\b", r"lightning\b", r"rainbow\b",
        r"tree\b", r"flower\b", r"grass\b", r"forest\b",
        r"mountain\b", r"river\b", r"lake\b", r"sea\b",
        r"ocean\b", r"island\b", r"field\b", r"hill\b",
        r"valley\b", r"desert\b", r"jungle\b",
        r"freezing\b", r"chapped\b", r"pruney\b",
    ]),
]

def categorize(en_key):
    """Return (category_name, priority) or None."""
    lower = en_key.lower()
    for cat_name, priority, patterns in CATEGORIES:
        for pat in patterns:
            if re.search(pat, lower, re.IGNORECASE):
                return cat_name, priority
    return None

# Categorize all words
packs = {}
uncategorized = {}

for en, fr in words.items():
    result = categorize(en)
    if result:
        cat_name, priority = result
        if cat_name not in packs:
            packs[cat_name] = {"priority": priority, "words": {}}
        packs[cat_name]["words"][en] = fr
    else:
        uncategorized[en] = fr

# Split uncategorized into chunks of ~50 as "mixed_N" packs
mixed_items = list(uncategorized.items())
mixed_packs = {}
for i in range(0, len(mixed_items), 50):
    chunk = dict(mixed_items[i:i+50])
    pack_num = (i // 50) + 1
    mixed_packs[f"mixed_{pack_num:02d}"] = {"priority": 6, "words": chunk}

packs.update(mixed_packs)

# Write packs
os.makedirs('data/packs', exist_ok=True)

# Remove old Polish packs
for f in os.listdir('data/packs'):
    if f.endswith('.pl.json'):
        os.remove(os.path.join('data/packs', f))

# Write new French packs
manifest = {}
for name, data in sorted(packs.items(), key=lambda x: (x[1]["priority"], x[0])):
    filename = f"{name}.fr.json"
    filepath = os.path.join('data', 'packs', filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data["words"], f, indent=2, ensure_ascii=False)
    manifest[name] = {
        "priority": data["priority"],
        "count": len(data["words"]),
        "file": filename
    }
    print(f"  {name}: {len(data['words'])} words (priority {data['priority']})")

# Write manifest
with open(os.path.join('data', 'packs', 'manifest.json'), 'w') as f:
    json.dump(manifest, f, indent=2)

print(f"\nTotal categorized: {sum(len(p['words']) for p in packs.values())}")
print(f"In themed packs: {sum(len(p['words']) for n,p in packs.items() if not n.startswith('mixed_'))}")
print(f"In mixed packs: {sum(len(p['words']) for n,p in packs.items() if n.startswith('mixed_'))}")
