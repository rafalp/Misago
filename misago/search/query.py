from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Union


class TokenType(Enum):
    QUOTE = auto()
    WORD = auto()
    PHRASE = auto()
    NOT = auto()
    AND = auto()
    OR = auto()
    OPEN = auto()
    CLOSE = auto()


Token = tuple[TokenType, str | None]


SearchQuery = Union[
    "SearchQueryKeyword",
    "SearchQueryPhrase",
    "SearchQueryAnd",
    "SearchQueryOr",
    "SearchQueryNot",
]


@dataclass(frozen=True)
class SearchQueryKeyword:
    value: str


@dataclass(frozen=True)
class SearchQueryPhrase:
    value: str


@dataclass(frozen=True)
class SearchQueryAnd:
    value: list["SearchQuery"]


@dataclass(frozen=True)
class SearchQueryOr:
    value: list["SearchQuery"]


@dataclass(frozen=True)
class SearchQueryNot:
    value: "SearchQuery"


def parse_search_query(
    query: str,
) -> SearchQuery | None:
    tokens = tokenize_query(query)
    if not tokens:
        return None

    return parse_tokens(tokens, 0, len(tokens))


def tokenize_query(query: str) -> list[Token]:
    in_quote = False
    group = 0
    tokens = []

    has_text = False
    has_not = False
    has_and = False
    has_or = False

    for c in normalize_quotes(query):
        if c == "'":
            tokens.append((TokenType.QUOTE, None))
            in_quote = not in_quote
            if in_quote:
                tokens.append((TokenType.PHRASE, ""))
        elif in_quote:
            has_text = True
            tokens[-1] = (TokenType.PHRASE, tokens[-1][1] + c)
        elif c.isalnum():
            if not tokens or tokens[-1][0] != TokenType.WORD:
                has_text = True
                tokens.append((TokenType.WORD, c))
            else:
                tokens[-1] = (TokenType.WORD, tokens[-1][1] + c)
        elif c == "-":
            has_not = True
            tokens.append((TokenType.NOT, None))
        elif c == "|":
            has_or = True
            tokens.append((TokenType.OR, None))
        elif c == "(":
            tokens.append((TokenType.OPEN, None))
            group += 1
        elif c == ")":
            if group:
                tokens.append((TokenType.CLOSE, None))
                group -= 1
        else:
            has_and = True
            tokens.append((TokenType.AND, None))

    while group:
        tokens.append((TokenType.CLOSE, None))
        group -= 1

    if has_text:
        tokens = clean_text_tokens(tokens)
    else:
        return []  # Search query without text is nonsensical

    if has_and:
        tokens = remove_and_tokens(tokens)

    if has_not or has_or:
        tokens = remove_invalid_tokens(tokens)

    return tokens


def normalize_quotes(query: str) -> str:
    normalized_query: str = ""
    for c in query:
        if 0x2018 <= ord(c) <= 0x201F:
            normalized_query += "'"
        else:
            normalized_query += c
    return normalized_query


def clean_text_tokens(tokens: list[Token]) -> list[Token]:
    new_tokens = []

    for token in tokens:
        token_type, token_value = token
        if token_type == TokenType.QUOTE:
            continue
        elif token_type == TokenType.PHRASE:
            if stripped_value := token_value.strip():
                new_tokens.append((TokenType.PHRASE, stripped_value))

            elif new_tokens:
                previous_token = new_tokens[-1][0]
                if previous_token in (TokenType.NOT, TokenType.OR):
                    new_tokens.pop()

        else:
            new_tokens.append(token)

    return new_tokens


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


def remove_and_tokens(tokens: list[Token]) -> list[Token]:
    return list(filter(lambda token: token[0] != TokenType.AND, tokens))


def remove_invalid_tokens(tokens: list[Token]) -> list[Token]:
    new_tokens = []
    last_index = len(tokens) - 1

    for index, token in enumerate(tokens):
        token_type, _ = token
        if token_type == TokenType.NOT:
            if index == last_index:
                continue

            next_token = tokens[index + 1][0]
            if next_token not in (
                TokenType.OPEN,
                TokenType.WORD,
                TokenType.PHRASE,
            ):
                continue

        if token_type == TokenType.OR:
            if not new_tokens or index == last_index:
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

        new_tokens.append(token)

    return new_tokens


def parse_tokens(tokens: list[Token], start: int, stop: int) -> SearchQuery | None:
    if start == stop:
        return None

    if start + 1 == stop:
        return parse_single_token(tokens[start])

    groups: list[SearchQuery] = []
    current_group: list[SearchQuery] = []

    level = 0
    open_position = 0

    operator = False  # False = AND, True = OR
    is_or_lookback = False

    is_not = False

    while start < stop:
        token_type = tokens[start][0]

        if token_type == TokenType.OPEN:
            if not level:
                open_position = start + 1

            level += 1

        elif token_type == TokenType.CLOSE:
            level -= 1

            if not level:
                # If operator changed, wrap values parsed so far
                # in a new group and add it to results
                current_operator = is_or_lookback or is_or_lookahead(
                    tokens, start, stop
                )
                if current_operator != operator and current_group:
                    if len(current_group) == 1:
                        groups.append(current_group[0])
                    if operator:
                        groups.append(SearchQueryOr(value=current_group))
                    else:
                        groups.append(SearchQueryAnd(value=current_group))

                    current_group = []

                operator = current_operator
                is_or_lookback = False

                if value := parse_tokens(tokens, open_position, start):
                    if is_not:
                        value = SearchQueryNot(value=value)
                        is_not = False

                    current_group.append(value)

        elif level:
            pass  # NOOP

        elif token_type == TokenType.OR:
            is_or_lookback = True

        elif token_type == TokenType.NOT:
            is_not = True

        else:
            # If operator changed, wrap values parsed so far
            # in a new group and add it to results
            current_operator = is_or_lookback or is_or_lookahead(tokens, start, stop)
            if current_operator != operator and current_group:
                if len(current_group) == 1:
                    groups.append(current_group[0])
                elif operator:
                    groups.append(SearchQueryOr(value=current_group))
                else:
                    groups.append(SearchQueryAnd(value=current_group))

                current_group = []

            operator = current_operator
            is_or_lookback = False

            # Process new value
            if value := parse_single_token(tokens[start]):
                if is_not:
                    value = SearchQueryNot(value=value)
                    is_not = False

                current_group.append(value)

        start += 1

    if len(current_group) == 1:
        groups.append(current_group[0])
    elif current_group:
        if operator:
            groups.append(SearchQueryOr(value=current_group))
        else:
            groups.append(SearchQueryAnd(value=current_group))

    if len(groups) == 1:
        return groups[0]

    return SearchQueryAnd(value=groups)


def is_or_lookahead(tokens: list[Token], start: int, stop: int) -> bool:
    if start + 1 == stop:
        return False

    token_type = tokens[start + 1][0]
    return token_type == TokenType.OR


def parse_single_token(token: Token) -> SearchQuery | None:
    token_type, token_value = token

    if token_type == TokenType.WORD:
        return SearchQueryKeyword(value=token_value)

    if token_type == TokenType.PHRASE:
        return SearchQueryPhrase(value=token_value)

    return None
