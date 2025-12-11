import tokenizeTemplateCondition from "./tokenizer"

function parseTemplateCondition(condition, context) {
  const tokens = tokenizeTemplateCondition(condition)
  console.log(tokens)
  if (!tokens) {
    return
  }

  const expression = []
  return expression
}

export default parseTemplateCondition
