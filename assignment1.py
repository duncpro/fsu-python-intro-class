

# Produces a list of the "substrings" in `s` according to the following rules...
# (1) All "substrings" are composed of contiguous characters in the input string `s`.
# (2) An occurrence of a character in `s` will result in exactly one occurrence of that same character in
#     exactly one "substring" in the returned list. (Characters are never duplicated)
# (3) Tabs, spaces, and new line characters are delimiters. These characters represent a
#     boundary between the substrings in `s`. The characters occurring before and after such
#     a delimiter will be grouped into two separate substrings.
# (4) The aforementioned delimiters are always represented by substrings of length 1. Where the sole
#     character in the substring is the delimiter character.
# (5) An occurrence of an opening parenthesis in `s` will cause all subsequent delimiters to be ignored
#     (treated as normal characters) until the next occurrence of a closing parenthesis character.
#     For instance if `s` is "abc (d e f) ghi" this function will return ["abc", "(d e f)", "ghi"].
def tokenize(s):
    tokens = []
    token = ""
    is_group = False

    for i in range(0, len(s)):
        c = s[i]

        if c == '(':
            if is_group:
                raise Exception("Composition is undefined for grouping expressions")
            is_group = True

            # Force split before opening parenthesis
            if len(token) > 0:
                tokens.append(token)
            token = "("
            continue

        if c == ')':
            if not is_group:
                raise Exception("Bracket mismatch, expected an opening parenthesis prior to closing"
                                " parenthesis")
            is_group = False

            # Force split after closing parenthesis
            tokens.append(token + ")")
            token = ""
            continue

        if c in [' ', '\t', '\n'] and not is_group:
            if len(token) > 0:
                tokens.append(token)
            tokens.append(c)
            token = ""
        else:
            token += c

    if len(token) > 0:
        tokens.append(token)

    return tokens


# Produces a list of the indices of the template tokens in `s`.
# For instance if `s` is "they called him (@ proper noun) after his father" then this function returns [3].
def find_template_tokens(tokens):
    templates = []

    for i in range(0, len(tokens)):
        token = tokens[i]
        is_template_token = token.startswith("(@")
        if is_template_token:
            print("template: " + token)
            templates.append(i)

    return templates


# Produces a new string which is equivalent to `s` semantically but not in layout.
# Specifically, additional newline delimiters are inserted at the end of every occurrence of at least `n`
# contiguous non-newline characters.
def wrap_lines(s, n):
    wrapped_s = ""
    char_count = 0
    for i in range(0, len(s)):
        if s[i] == '\n':
            char_count = 0

        if char_count >= n and s[i] in [' ', '\t']:
            char_count = 0
            wrapped_s += '\n'
        else:
            char_count += 1
            wrapped_s += s[i]

    return wrapped_s


# Produces a new string which is equivalent to `s` semantically but not in layout.
# Specifically, all new line characters are replaced with horizontal spaces.
def nowrap(s):
    nowrapped_s = ""
    for c in s:
        if c == '\n':
            nowrapped_s += ' '
        else:
            nowrapped_s += c
    return nowrapped_s


def concat(tokens):
    s = []
    for token in tokens:
        s += token
    return s


# Produces a substring of the concatenation of the given tokens except the target token is replaced
# with a placeholder symbol (_______). This function produces a substring at least containing the target token,
# with a few prefix and suffix tokens for context.
def make_substitution_context_str(tokens, target):
    tokens = tokens.copy(); tokens[target] = "______"
    trimmed = ["..."]
    max_prefix_length = 10
    max_suffix_length = 10
    for i in range(max(0, target - max_prefix_length), min(target + 1 + max_suffix_length, len(tokens))):
        trimmed.append(tokens[i])
    trimmed.append("...")
    return nowrap(concat(trimmed))


example_madlib = ("This time every year I (@verb) all the time because I get really exciting thinking about holiday "
                  "(@plural noun)! That’s why I was sitting at the (@room of house): I was really hoping (@a relative)"
                  " would come by and give me at least (@a number) pieces of holiday (@food item)!")

def main(madlib_template):
    tokens = tokenize(madlib_template)
    templates = find_template_tokens(tokens)
    substitutions = []

    print("===== Madlib =====")
    print(wrap_lines(madlib_template, 50))

    for i in range(0, len(templates)):
        bullet = "\n#" + str(i + 1) + ":"
        print(bullet, make_substitution_context_str(tokens, templates[i]))
        form = tokens[templates[i]].removeprefix("(@").removesuffix(")")
        print("Now, choose a " + form + " to be substituted for the blank.")
        response = input("Substitution: ")
        substitutions.append(response)

    for i in range(0, len(templates)):
        tokens[templates[i]] = substitutions[i]

    print("Substitutions complete! Almost done.")
    print("How would you like the output to be presented?")
    print("1. With Automatic Line Wrapping")
    print("2. Without Automatic Line Wrapping (ideal for copy/paste)")

    output_mode = int(input("Selection (either 1 or 2): "))
    output_text = ""
    if output_mode == 1:
        output_text = wrap_lines(concat(tokens), 50)
    if output_mode == 2:
        output_text = nowrap(concat(tokens))
    print(output_text)


main(example_madlib)
