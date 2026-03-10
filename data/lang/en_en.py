PARSE_ERROR_MSG = 'Wrong command'
WELCOME_MSG = ['Hello', 'Hi', 'Nice to see you']
GUESSER_RULES = 'We are going to refresh some words now. Type the French translation for each English word.'
TRANSLATION_ERROR_MSG = 'There is no translation for this word'
BEGIN_MSG = "Let's start"
FIRST_ROUND_MSG = 'The first word is'
FORM_MSG = 'Form'
TRANSLATION_MSG = 'Translation'
NO_CONJUGATION_MSG = "I can't conjugate this word."
NO_WORDS_MSG = "You haven't added any words yet. Use /add [english] [french] or /addpack [name] to get started."
PAIR_MSG = 'Pair'
SAME_WORD_MSG = 'is the same word'
DATABASE_ERROR_MSG = "Cannot create pair. Maybe you've already added it?"
CREATED_MSG = 'created'
CORRECT_MSG = ['Correct', 'Good guess', 'Excellent', 'Bien joué']
WRONG_MSG = ['Wrong', 'Incorrect', 'There are mistakes']
GAME_OVER_MSG = ['Game over', "You've finished"]
GUESSED_COUNT_MSG = ['You guessed', 'Named correctly', 'Points earned']
ERROR_RATE_MSG = ['Average error rate', 'Error percentage']
NEXT_ROUND_MSG = ['Next word', 'Continuing']
EDITED_MSG = 'edited'
DELETED_MSG = 'deleted'
NOT_FOUND = 'There is no such pair'
UNKNOWN_MSG = "I didn't understand you. Use /help to see available commands."
REQUIRE_START_MSG = 'Use /start'
GENERAL_INFO_MSG = (
    "I help you learn French vocabulary.\n"
    "Use /listpacks to see word categories, "
    "/addpack [name] to load words, "
    "then /guess to practice."
)
HELP = """/start - start session.
/help - show this help.
/add [english] [french] - add a word pair. Use underscores for spaces: hello_world.
/edit [english] [french] - edit the french word in a pair.
/del [english] [french] - delete a pair.
/guess [count=10] - start vocabulary quiz.
/t [word] - translate a word (English to French).
/stop - stop current session.
/listpacks - list word packs sorted by usefulness.
/addpack [pack name] - load a word pack.
"""
GUESSER_START = 'Time to practice some French vocabulary'
CANCEL = 'Cancelled.'
LANGUAGE_SET = 'Language set.'
AMBIGUOUS_LANG = 'Cannot determine language.'
ADD_PACK_SUCCESS_MSG = 'Pack added successfully.'
PACK_NOT_FOUND_MSG = 'Pack not found. Use /listpacks to see available packs.'
