def rule_based_check(text):
    flags = []

    red_flags = {
        "money": ["₹", "rs", "inr", "send money", "pay"],
        "urgency": ["urgent", "act now", "account block"],
        "bank": ["bank details", "otp", "card number"],
        "fee": ["processing fee", "transfer fee"]
    }

    text = text.lower()

    for category, words in red_flags.items():
        for word in words:
            if word in text:
                flags.append(category)
                break

    return list(set(flags))
