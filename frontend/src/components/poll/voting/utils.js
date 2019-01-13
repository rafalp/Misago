export function getChoiceFromHash(choices, hash) {
  for (const i in choices) {
    const choice = choices[i]
    if (choice.hash === hash) {
      return choice
    }
  }

  return null
}

export function getChoicesLeft(poll, choices) {
  let selection = []
  for (const i in choices) {
    const choice = choices[i]
    if (choice.selected) {
      selection.push(choice)
    }
  }

  return poll.allowed_choices - selection.length
}
