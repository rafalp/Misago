import parseTemplateCondition from "./parser"

function evaluateTemplateCondition(condition, context) {
  const expression = parseTemplateCondition(condition, context)
  return false
}

export default evaluateTemplateCondition
