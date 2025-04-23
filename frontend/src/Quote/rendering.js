function paragraph(selection, node, state) {
  if (node.type !== "paragraph") {
    return false
  }

  const text = selection.renderNodes(node.children).trim()
  if (!text) {
    return false
  }

  state.text += "\n" + text + "\n"
  return true
}

function text(selection, node, state) {
  if (node.type !== "text") {
    return false
  }

  state.text += node.content
  return true
}

export default [
  { name: "paragraph", func: paragraph },
  { name: "text", func: text },
]
