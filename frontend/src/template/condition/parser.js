import EXPRESSION from "./expressions"
import tokenizeTemplateCondition from "./tokenizer"
import TOKEN from "./tokens"
import validateTokens from "./validator"

const CACHE = {}

function parseTemplateCondition(condition) {
  if (CACHE[condition]) {
    return CACHE[condition]
  }

  let tokens = tokenizeTemplateCondition(condition)
  if (!tokens) {
    CACHE[condition] = null
    return
  }

  tokens = validateTokens(tokens, condition)
  if (!tokens) {
    CACHE[condition] = null
    return
  }

  let expressions = insertLeafExpressions(tokens)
  expressions = insertNotExpressions(expressions)
  expressions = insertBranchingExpression(expressions)
  expressions = insertConditionalExpression(expressions)

  CACHE[condition] = expressions[0]
  return expressions[0]
}

function insertLeafExpressions(tokens) {
  return tokens.map(insertLeafExpression)
}

function insertLeafExpression(token) {
  if (token.token === TOKEN.NAME) {
    if (token.name.indexOf(".") > 0) {
      return {
        expression: EXPRESSION.DEEP_VARIABLE,
        path: token.name.split("."),
      }
    } else {
      return {
        expression: EXPRESSION.VARIABLE,
        name: token.name,
      }
    }
  } else if (token.token === TOKEN.NUMBER) {
    return {
      expression: EXPRESSION.VALUE,
      value: token.number,
    }
  } else if (token.token === TOKEN.BOOL) {
    return {
      expression: EXPRESSION.VALUE,
      value: token.value,
    }
  } else if (token.token === TOKEN.NULL) {
    return {
      expression: EXPRESSION.VALUE,
      value: null,
    }
  }

  return token
}

function insertNotExpressions(expressions) {
  let result = expressions
  while (hasNotTokens(result)) {
    result = replaceNotToken(result)
  }
  return result
}

function hasNotTokens(expressions) {
  return expressions.filter(function (token) {
    return token.token === TOKEN.NOT
  }).length
}

function replaceNotToken(expressions) {
  let start = 0
  const end = expressions.length
  const result = []

  while (start < end) {
    const token = expressions[start]
    if (
      token.token === TOKEN.NOT &&
      expressions[start + 1].token !== TOKEN.NOT
    ) {
      result.push({
        expression: EXPRESSION.NOT,
        value: expressions[start + 1],
      })
      start += 2
    } else {
      result.push(token)
      start += 1
    }
  }

  return result
}

function parseNestedTemplateCondition(expressions) {
  let expression = insertBranchingExpression(expressions)
  expression = insertConditionalExpression(expression)
  return expression[0]
}

function insertBranchingExpression(expressions) {
  const index = expressions.findIndex(function (item) {
    return item.token === TOKEN.AND || item.token === TOKEN.OR
  })

  if (index === -1) {
    return expressions
  }

  return [
    {
      expression:
        expressions[index].token === TOKEN.AND ? EXPRESSION.AND : EXPRESSION.OR,
      left: parseNestedTemplateCondition(expressions.slice(0, index)),
      right: parseNestedTemplateCondition(expressions.slice(index + 1)),
    },
  ]
}

function insertConditionalExpression(expressions) {
  const index = expressions.findIndex(function (item) {
    return item.token === TOKEN.COMPARISON
  })

  if (index === -1) {
    return expressions
  }

  return [
    {
      expression: EXPRESSION.CONDITION,
      condition: expressions[index].comparison,
      left: parseNestedTemplateCondition(expressions.slice(0, index)),
      right: parseNestedTemplateCondition(expressions.slice(index + 1)),
    },
  ]
}

export default parseTemplateCondition
