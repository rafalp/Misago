import COMPARISON from "./comparisons"
import TOKEN from "./tokens"

function tokenizeTemplateCondition(condition) {
  const rules = RULES.length
  const state = {
    tokens: [],
    condition: condition,
    start: 0,
    end: condition.length,
  }

  while (state.start < state.end) {
    let match = false

    for (let i = 0; i < rules; i++) {
      const rule = RULES[i]
      if (rule(state)) {
        match = true
        break
      }
    }

    if (!match) {
      return console.error(
        "error parsing '" +
          condition +
          "' at " +
          state.start +
          ": unexpected '" +
          state.condition[state.start] +
          "'"
      )
    }
  }

  return state.tokens.filter(function removeSpaces(item) {
    return item.token !== TOKEN.SPACE
  })
}

function nameRule(state) {
  if (!state.condition[state.start].match(/[_a-z]/i)) {
    return false
  }

  const match = state.condition
    .substring(state.start, state.end)
    .match(/^[_a-z0-9]+(\.[_a-z][_a-z0-9]*)*/i)

  if (!match) {
    return false
  }

  const name = match[0]

  if (name === "true" || name === "false") {
    state.tokens.push({
      token: TOKEN.BOOL,
      start: state.start,
      end: state.start + name.length,
      value: name === "true",
    })
  } else if (name === "null") {
    state.tokens.push({
      token: TOKEN.NULL,
      start: state.start,
      end: state.start + name.length,
    })
  } else {
    state.tokens.push({
      token: TOKEN.NAME,
      start: state.start,
      end: state.start + name.length,
      name,
    })
  }
  state.start += name.length

  return true
}

function integerRule(state) {
  const match = state.condition
    .substring(state.start, state.end)
    .match(/^(0|([1-9][0-9]*))/)

  if (!match) {
    return false
  }

  const number = match[0]

  state.tokens.push({
    token: TOKEN.NUMBER,
    start: state.start,
    end: state.start + number.length,
    number: parseInt(number),
  })
  state.start += number.length

  return true
}

function floatRule(state) {
  const match = state.condition
    .substring(state.start, state.end)
    .match(/^(0|([1-9][0-9]*)).[0-9]*/i)

  if (!match) {
    return false
  }

  const number = match[0]

  state.tokens.push({
    token: TOKEN.NUMBER,
    start: state.start,
    end: state.start + number.length,
    number: parseFloat(number),
  })
  state.start += number.length

  return true
}

function strictEqualRule(state) {
  if (state.start + 2 >= state.end) {
    return false
  }

  if (state.condition.substring(state.start, state.start + 3) !== "===") {
    return false
  }

  state.tokens.push({
    token: TOKEN.COMPARISON,
    start: state.start,
    end: state.start + 3,
    comparison: COMPARISON.STRICT_EQUAL,
  })
  state.start += 3

  return true
}

function equalRule(state) {
  if (state.start + 1 >= state.end) {
    return false
  }

  if (state.condition.substring(state.start, state.start + 2) !== "==") {
    return false
  }

  state.tokens.push({
    token: TOKEN.COMPARISON,
    start: state.start,
    end: state.start + 2,
    comparison: COMPARISON.EQUAL,
  })
  state.start += 2

  return true
}

function strictNotEqualRule(state) {
  if (state.start + 2 >= state.end) {
    return false
  }
  if (state.condition.substring(state.start, state.start + 3) !== "!==") {
    return false
  }

  state.tokens.push({
    token: TOKEN.COMPARISON,
    start: state.start,
    end: state.start + 3,
    comparison: COMPARISON.STRICT_NOT_EQUAL,
  })
  state.start += 3

  return true
}

function notEqualRule(state) {
  if (state.start + 1 >= state.end) {
    return false
  }

  if (state.condition.substring(state.start, state.start + 2) !== "!=") {
    return false
  }

  state.tokens.push({
    token: TOKEN.COMPARISON,
    start: state.start,
    end: state.start + 2,
    comparison: COMPARISON.NOT_EQUAL,
  })
  state.start += 2

  return true
}

function greaterThanEqualRule(state) {
  if (state.start + 1 >= state.end) {
    return false
  }

  if (state.condition.substring(state.start, state.start + 2) !== ">=") {
    return false
  }

  state.tokens.push({
    token: TOKEN.COMPARISON,
    start: state.start,
    end: state.start + 2,
    comparison: COMPARISON.GREATER_THAN_EQUAL,
  })
  state.start += 2

  return true
}

function greaterThanRule(state) {
  if (state.condition[state.start] !== ">") {
    return false
  }

  state.tokens.push({
    token: TOKEN.COMPARISON,
    start: state.start,
    end: state.start + 1,
    comparison: COMPARISON.GREATER_THAN,
  })
  state.start += 1

  return true
}

function lessThanEqualRule(state) {
  if (state.start + 1 >= state.end) {
    return false
  }

  if (state.condition.substring(state.start, state.start + 2) !== "<=") {
    return false
  }

  state.tokens.push({
    token: TOKEN.COMPARISON,
    start: state.start,
    end: state.start + 2,
    comparison: COMPARISON.LESS_THAN_EQUAL,
  })
  state.start += 2

  return true
}

function lessThanRule(state) {
  if (state.condition[state.start] !== "<") {
    return false
  }

  state.tokens.push({
    token: TOKEN.COMPARISON,
    start: state.start,
    end: state.start + 1,
    comparison: COMPARISON.LESS_THAN,
  })
  state.start += 1

  return true
}

function notRule(state) {
  if (state.condition[state.start] !== "!") {
    return false
  }

  state.tokens.push({
    token: TOKEN.NOT,
    start: state.start,
    end: state.start + 1,
  })
  state.start += 1

  return true
}

function andRule(state) {
  if (state.start + 1 >= state.end) {
    return false
  }

  if (state.condition.substring(state.start, state.start + 2) !== "&&") {
    return false
  }

  state.tokens.push({
    token: TOKEN.AND,
    start: state.start,
    end: state.start + 2,
  })
  state.start += 2

  return true
}

function orRule(state) {
  if (state.start + 1 >= state.end) {
    return false
  }

  if (state.condition.substring(state.start, state.start + 2) !== "||") {
    return false
  }

  state.tokens.push({
    token: TOKEN.OR,
    start: state.start,
    end: state.start + 2,
  })
  state.start += 2

  return true
}

function spaceRule(state) {
  if (state.condition[state.start] !== " ") {
    return false
  }

  const lastToken = state.tokens ? state.tokens[state.tokens.length - 1] : null
  if (lastToken && lastToken.token === TOKEN.SPACE) {
    lastToken.end += 1
  } else {
    state.tokens.push({
      token: TOKEN.SPACE,
      start: state.start,
      end: state.start + 1,
    })
  }

  state.start += 1

  return true
}

const RULES = [
  nameRule,
  floatRule,
  integerRule,
  strictEqualRule,
  equalRule,
  strictNotEqualRule,
  notEqualRule,
  notRule,
  greaterThanEqualRule,
  greaterThanRule,
  lessThanEqualRule,
  lessThanRule,
  andRule,
  orRule,
  spaceRule,
]

export default tokenizeTemplateCondition
