from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union


class TokenType(Enum):
    BREAK = 0
    QUOTE = 1
    WORD = 2
    PHRASE = 3
    OR = 4
    NOT = 5
    OPEN = 6
    CLOSE = 7


Token = tuple[TokenType, str | None]


def parse_search_query(
    query: str,
) -> Optional[
    Union[
        "SearchQueryKeyword",
        "SearchQueryPhrase",
        "SearchQueryAnd",
        "SearchQueryOr",
        "SearchQueryNot",
    ]
]:
    query = normalize_quotes(query)
    tokens = tokenize_query(query)
    return parse_tokens(tokens)


def normalize_quotes(query: str) -> str:
    normalized_query: str = ""
    for c in query:
        if 0x2018 <= ord(c) <= 0x201F:
            normalized_query += "'"
        else:
            normalized_query += c
    return normalized_query


def tokenize_query(query: str) -> list[Token]:
    in_value = False
    tokens = []
    for c in query:
        if c == "'":
            tokens.append((TokenType.QUOTE, None))
            in_value = not in_value
            if in_value:
                tokens.append((TokenType.PHRASE, ""))
        elif in_value:
            tokens[-1] = (TokenType.PHRASE, tokens[-1][1] + c)
        elif c.isalnum():
            if not tokens or tokens[-1][0] != TokenType.WORD:
                tokens.append((TokenType.WORD, c))
            else:
                tokens[-1] = (TokenType.WORD, tokens[-1][1] + c)
        elif c == "|":
            tokens.append((TokenType.OR, None))
        elif c == "-":
            tokens.append((TokenType.NOT, None))
        elif c == "(":
            tokens.append((TokenType.OPEN, None))
        elif c == ")":
            tokens.append((TokenType.CLOSE, None))
        else:
            tokens.append((TokenType.BREAK, None))

    tokens = remove_break_tokens(tokens)
    tokens = clean_value_tokens(tokens)
    tokens = clean_open_close_tokens(tokens)
    tokens = remove_invalid_tokens(tokens)

    return tokens


def remove_break_tokens(tokens: list[Token]) -> list[Token]:
    return list(filter(lambda token: token[0] != TokenType.BREAK, tokens))


def clean_open_close_tokens(tokens: list[Token]) -> list[Token]:
    new_tokens = []

    level = 0
    group_tokens = []

    for token in tokens:
        token_type, _ = token
        if token_type == TokenType.OPEN:
            level += 1
        if token_type == TokenType.CLOSE:
            if level:
                level -= 1
            else:
                continue

        if level:
            group_tokens.append(token)
        elif group_tokens:
            group_tokens.append(token)
            new_tokens += group_tokens
            group_tokens = []
        else:
            new_tokens.append(token)

    if group_tokens:
        # If there are unclosed groups, we will use "closest non-overlapping pair" strategy
        new_tokens += group_tokens[1:]

    return new_tokens


def remove_invalid_tokens(tokens: list[Token]) -> list[Token]:
    new_tokens = []
    max_index = len(tokens) - 1

    for index, token in enumerate(tokens):
        token_type, _ = token
        if token_type == TokenType.OR:
            if not new_tokens or index == max_index:
                continue

            previous_token = new_tokens[-1][0]
            next_token = tokens[index + 1][0]
            if previous_token not in (
                TokenType.CLOSE,
                TokenType.WORD,
                TokenType.PHRASE,
            ):
                continue
            if next_token not in (
                TokenType.OPEN,
                TokenType.NOT,
                TokenType.WORD,
                TokenType.PHRASE,
            ):
                continue

        if token_type == TokenType.NOT:
            if index == max_index:
                continue

            next_token = tokens[index + 1][0]
            if next_token not in (
                TokenType.OPEN,
                TokenType.WORD,
                TokenType.PHRASE,
            ):
                continue

        new_tokens.append(token)

    return new_tokens


def clean_value_tokens(tokens: list[Token]) -> list[Token]:
    new_tokens = []

    for token in tokens:
        token_type, token_value = token
        if token_type == TokenType.QUOTE:
            continue
        elif token_type == TokenType.PHRASE:
            if stripped_value := token_value.strip():
                new_tokens.append((TokenType.PHRASE, stripped_value))
        else:
            new_tokens.append(token)

    return new_tokens


def parse_tokens(tokens: list):
    tokens = parse_token_groups(tokens)

    if len(tokens) == 1:
        return parse_single_token(tokens[0])

    new_tokens = []
    prefix = []

    for token in tokens:
        if isinstance(token, tuple) and token[0] in (TokenType.NOT, TokenType.OR):
            prefix.append(token[0])
            continue

        if new_tokens:
            previous_token = new_tokens[-1]
        else:
            previous_token = None

        if isinstance(token, tuple):
            token = parse_single_token(token) or token

        if isinstance(token, SearchQueryGroup):
            token = token.value

            if prefix and prefix[-1] == TokenType.NOT:
                prefix.pop()
                token = SearchQueryNot(value=token)

        if isinstance(token, (SearchQueryKeyword, SearchQueryPhrase)):
            if prefix and prefix[-1] == TokenType.NOT:
                prefix.pop()
                token = SearchQueryNot(value=token)

            if not new_tokens:
                new_tokens.append(token)

            elif prefix and prefix[-1] == TokenType.OR:
                prefix.clear()

                if isinstance(previous_token, (SearchQueryKeyword, SearchQueryPhrase)):
                    new_tokens[-1] = SearchQueryOr(value=[new_tokens[-1], token])

                elif isinstance(previous_token, SearchQueryAnd):
                    previous_token.value[-1] = SearchQueryOr(
                        value=[previous_token.value[-1], token]
                    )

                elif isinstance(previous_token, SearchQueryOr):
                    new_tokens[-1].value.append(token)

            else:
                if isinstance(previous_token, (SearchQueryKeyword, SearchQueryPhrase)):
                    new_tokens[-1] = SearchQueryAnd(value=[new_tokens[-1], token])

                elif isinstance(new_tokens[-1], SearchQueryAnd):
                    new_tokens[-1].value.append(token)

                elif isinstance(previous_token, SearchQueryOr):
                    new_tokens[-1] = SearchQueryAnd(value=[new_tokens[-1], token])

        elif isinstance(token, SearchQueryAnd):
            if prefix and prefix[-1] == TokenType.OR:
                prefix.clear()
                new_tokens[-1] = SearchQueryOr(value=[new_tokens[-1], token])

            elif isinstance(previous_token, SearchQueryAnd):
                previous_token.value += token.value

            else:
                new_tokens.append(token)

        elif isinstance(token, SearchQueryOr):
            if isinstance(previous_token, SearchQueryOr):
                previous_token.value += token.value

            elif prefix and prefix[-1] == TokenType.OR:
                prefix.clear()
                new_tokens[-1] = SearchQueryOr(value=[new_tokens[-1], token])

            else:
                new_tokens.append(token)

        elif isinstance(token, SearchQueryNot):
            if prefix and prefix[-1] == TokenType.OR:
                prefix.clear()
                new_tokens[-1] = SearchQueryOr(value=[new_tokens[-1], token])

            elif isinstance(previous_token, SearchQueryAnd):
                previous_token.value.append(token)

            else:
                new_tokens[-1] = SearchQueryAnd(value=[new_tokens[-1], token])

        else:
            new_tokens.append(token)

    if len(new_tokens) == 1:
        return new_tokens[0]

    return new_tokens or None


def parse_single_token(
    token: Token,
) -> Optional[Union["SearchQueryKeyword", "SearchQueryPhrase"]]:
    token_type, token_value = token

    if token_type == TokenType.WORD:
        return SearchQueryKeyword(value=token_value)

    if token_type == TokenType.PHRASE:
        return SearchQueryPhrase(value=token_value)

    return None


def parse_token_groups(tokens: list[Token]) -> list:
    new_tokens = []

    level = 0
    group_tokens = []

    for token in tokens:
        token_type, _ = token
        if token_type == TokenType.OPEN:
            level += 1
        if token_type == TokenType.CLOSE:
            level -= 1

        if level:
            group_tokens.append(token)
        elif group_tokens:
            if new_token := parse_tokens(group_tokens[1:]):
                new_tokens.append(SearchQueryGroup(value=new_token))
            group_tokens = []
        else:
            new_tokens.append(token)

    return new_tokens


@dataclass(frozen=True)
class SearchQueryKeyword:
    value: str


@dataclass(frozen=True)
class SearchQueryPhrase:
    value: str


@dataclass(frozen=True)
class SearchQueryAnd:
    value: list


@dataclass(frozen=True)
class SearchQueryOr:
    value: list


@dataclass(frozen=True)
class SearchQueryGroup:
    value: Union[
        SearchQueryKeyword,
        SearchQueryPhrase,
        SearchQueryAnd,
        SearchQueryOr,
    ]


@dataclass(frozen=True)
class SearchQueryNot:
    value: Union[
        SearchQueryKeyword,
        SearchQueryPhrase,
        SearchQueryAnd,
        SearchQueryOr,
    ]
