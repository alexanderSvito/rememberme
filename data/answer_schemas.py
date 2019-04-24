GUESSER_START_SCHEME = """{BEGIN_MSG}, {FIRST_ROUND_MSG}:
> {{round}}"""

TRANSLATION_SCHEME = """{translations}"""

NEXT_CONJ_ROUND_SCHEME = """
{FORM_MSG} - _{{term}}_
{TRANSLATION_MSG} - {{translations}}
> *{{conj}}* ({{round}})"""

CONJ_START_SCHEME = "{BEGIN_MSG}, {FIRST_ROUND_MSG}:" + NEXT_CONJ_ROUND_SCHEME

SAME_WORD_SCHEME = "{PAIR_MSG}: {{anchor}} - {{response}} {SAME_WORD_MSG}"

CREATED_SCHEME = "{PAIR_MSG}: {{anchor}} - {{response}} {CREATED_MSG}!"

EDITED_SCHEME = "{PAIR_MSG}: {{anchor}} - {{response}} {EDITED_MSG}!"

DELETED_SCHEME = "{PAIR_MSG}: {{anchor}} - {{response}} {DELETED_MSG}!"

CORRECT_SCHEME = "{CORRECT_MSG}!"

WRONG_SCHEME = "{WRONG_MSG}: {{correction}}"

GAME_OVER_SCHEME = """{GAME_OVER_MSG}
{GUESSED_COUNT_MSG}: {{correct_count}}
{ERROR_RATE_MSG}: _{{error_rate}}_"""

NEXT_ROUND_SCHEME = """{NEXT_ROUND_MSG}: 
> {{round}}"""

START_SCHEME = "{WELCOME_MSG}, {GENERAL_INFO_MSG}"
