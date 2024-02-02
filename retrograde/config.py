# Configuration
SAVE_TO_FILE = True

# Print timing
PRINT_TIMING = True

# Advice
GENERATE_ADVICE = True

# News
ALPHAVANTAGE_API = "V3UO2MUD5E7I896L"
NEWS_ITEM_LIMIT = 50

# AI

# TODO:MOVE API to .env FILE
OPENAI_API="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"
CHATGPT_VERSIONS = {"3.5": "gpt-3.5-turbo", "4": "gpt-4"}
CHATGPT_VERSION = CHATGPT_VERSIONS['4']
ADVICE_PROMPT_OPTIONS = [
            "I am sending you a copy of my portfolio. Asses my current investment strategy based on global stock market on the given date. Take to account the holding of each stock given by value.",
            "Describe in 30 words the nature of the global stock market on the given date.",
            "If there is a way to improve the portfolio give feedback. If you think there is no Otherwise some fact the market trends of the asset held in the portfolio.",
            "Give me some random piece of investment advice relevant to my portfolio. Value the portion of the investment based on their values."
        ]
ADVICE_PROMPT = ADVICE_PROMPT_OPTIONS[0]
ADVICE_WORD_LIMIT = 40