import TOKEN from "./tokens"

function validateTokens(tokens, condition) {
  const rules = RULES.length
  const state = {
    condition,
    tokens,
    start: 0,
    end: tokens.length,
  }

  while (state.start < state.end) {
    for (let i = 0; i < rules; i++) {
      const rule = RULES[i]
      if (!rule(state)) {
        return logValidationError(state)
      }
    }
    state.start += 1
  }

  return state.tokens
}

function logValidationError(state) {
  const position = state.tokens[state.start].start
  const character = state.condition[position]

  console.error(
    `error parsing '${state.condition}' at ${position}: unexpected '${character}'`
  )
  return false
}

function repeatsRule(state) {
  if (state.start === 0 || state.tokens[state.start].token === TOKEN.NOT) {
    return true
  }

  if (state.tokens[state.start].token !== state.tokens[state.start - 1].token) {
    return true
  }

  return false
}

const VALUE_TOKEN = {
  [TOKEN.NAME]: true,
  [TOKEN.NUMBER]: true,
  [TOKEN.BOOL]: true,
  [TOKEN.NULL]: true,
  [TOKEN.NOT]: true,
}

function repeatValueRule(state) {
  if (state.start === 0 || !VALUE_TOKEN[state.tokens[state.start].token]) {
    return true
  }

  const previousToken = state.tokens[state.start - 1].token
  return previousToken === TOKEN.NOT || !VALUE_TOKEN[previousToken]
}

function comparisonRule(state) {
  if (state.tokens[state.start].token != TOKEN.COMPARISON) {
    return true
  }

  if (state.start === 0 || state.start + 1 === state.end) {
    return false
  }

  const previousToken = state.tokens[state.start - 1].token
  const nextToken = state.tokens[state.start + 1].token

  if (!VALUE_TOKEN[previousToken] || !VALUE_TOKEN[nextToken]) {
    return false
  }

  return true
}

function notRule(state) {
  if (state.tokens[state.start].token !== TOKEN.NOT) {
    return true
  }

  if (state.start + 1 === state.end) {
    return false
  }

  const nextToken = state.tokens[state.start + 1].token
  if (!VALUE_TOKEN[nextToken]) {
    return false
  }

  return true
}

function andOrRule(state) {
  if (
    state.tokens[state.start].token !== TOKEN.AND &&
    state.tokens[state.start].token !== TOKEN.OR
  ) {
    return true
  }

  if (state.start === 0 || state.start + 1 === state.end) {
    return false
  }

  const previousToken = state.tokens[state.start - 1].token
  const nextToken = state.tokens[state.start + 1].token

  if (!VALUE_TOKEN[previousToken] || !VALUE_TOKEN[nextToken]) {
    return false
  }

  return true
}

const RULES = [repeatsRule, repeatValueRule, comparisonRule, notRule, andOrRule]

export default validateTokens
