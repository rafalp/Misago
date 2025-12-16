import COMPARISON from "./comparisons"
import EXPRESSION from "./expressions"
import parseTemplateCondition from "./parser"

function evaluateTemplateCondition(condition, context) {
  const expression = parseTemplateCondition(condition)
  return !!evaluateExpression(expression, context)
}

function evaluateExpression(expression, context) {
  if (expression.expression === EXPRESSION.VALUE) {
    return expression.value
  } else if (expression.expression === EXPRESSION.VARIABLE) {
    return context[expression.name]
  } else if (expression.expression === EXPRESSION.DEEP_VARIABLE) {
    return evaluateDeepContextVariable(expression.path, context)
  } else if (expression.expression === EXPRESSION.CONDITION) {
    return evaluateConditionExpression(expression, context)
  } else if (expression.expression === EXPRESSION.NOT) {
    return !evaluateExpression(expression.value, context)
  } else if (expression.expression === EXPRESSION.AND) {
    return evaluateAndExpression(expression, context)
  } else if (expression.expression === EXPRESSION.OR) {
    return evaluateOrExpression(expression, context)
  } else {
    console.error("unknown expression", expression)
    return false
  }
}

function evaluateDeepContextVariable(path, context) {
  let result = context
  for (let i = 0; i < path.length; i++) {
    result = result[path[i]]
    if (typeof result === "undefined") {
      return undefined
    }
  }
  return result
}

function evaluateConditionExpression(expression, context) {
  const left = evaluateExpression(expression.left, context)
  const right = evaluateExpression(expression.right, context)

  if (expression.condition === COMPARISON.EQUAL) {
    return left == right
  } else if (expression.condition === COMPARISON.STRICT_EQUAL) {
    return left === right
  } else if (expression.condition === COMPARISON.NOT_EQUAL) {
    return left != right
  } else if (expression.condition === COMPARISON.STRICT_NOT_EQUAL) {
    return left !== right
  } else if (expression.condition === COMPARISON.GREATER_THAN) {
    return left > right
  } else if (expression.condition === COMPARISON.GREATER_THAN_EQUAL) {
    return left >= right
  } else if (expression.condition === COMPARISON.LESS_THAN) {
    return left < right
  } else if (expression.condition === COMPARISON.LESS_THAN_EQUAL) {
    return left <= right
  }
}

function evaluateAndExpression(expression, context) {
  const left = evaluateExpression(expression.left, context)
  const right = evaluateExpression(expression.right, context)
  return left && right
}

function evaluateOrExpression(expression, context) {
  const left = evaluateExpression(expression.left, context)
  const right = evaluateExpression(expression.right, context)
  return left || right
}

export default evaluateTemplateCondition
