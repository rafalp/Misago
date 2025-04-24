function header(selection, node, state) {
  if (node.type !== "header") {
    return false
  }

  const text = selection.renderNodes(node.children).trim()
  if (!text) {
    return false
  }

  if (state.text) {
    state.text += "\n\n\n"
  }

  const prefix = "#".repeat(node.level)
  state.text += prefix + " " + text

  return true
}

function youtube(selection, node, state) {
  if (node.type !== "youtube") {
    return false
  }

  if (state.text) {
    state.text += "\n\n"
  }

  state.text += node.url

  return true
}

function paragraph(selection, node, state) {
  if (node.type !== "paragraph") {
    return false
  }

  const text = selection.renderNodes(node.children).trim()
  if (!text) {
    return false
  }

  if (state.text) {
    state.text += "\n\n"
  }

  state.text += text

  return true
}

function strong_text(selection, node, state) {
  if (node.type !== "strong") {
    return false
  }

  const text = selection.renderNodes(node.children)
  if (!text) {
    return false
  }

  const delimiter = text.indexOf("*") === -1 ? "**" : "__"
  state.text += delimiter + text + delimiter

  return true
}

function emphasis_text(selection, node, state) {
  if (node.type !== "emphasis") {
    return false
  }

  const text = selection.renderNodes(node.children)
  if (!text) {
    return false
  }

  const delimiter = text.indexOf("*") === -1 ? "*" : "_"
  state.text += delimiter + text + delimiter

  return true
}

function bold_text(selection, node, state) {
  if (node.type !== "bold") {
    return false
  }

  const text = selection.renderNodes(node.children)
  if (!text) {
    return false
  }

  state.text += "[b]" + text + "[/b]"

  return true
}

function italic_text(selection, node, state) {
  if (node.type !== "italic") {
    return false
  }

  const text = selection.renderNodes(node.children)
  if (!text) {
    return false
  }

  state.text += "[i]" + text + "[/i]"

  return true
}

function underline_text(selection, node, state) {
  if (node.type !== "underline") {
    return false
  }

  const text = selection.renderNodes(node.children)
  if (!text) {
    return false
  }

  state.text += "[u]" + text + "[/u]"

  return true
}

function strikethrough_text(selection, node, state) {
  if (node.type !== "strikethrough") {
    return false
  }

  const text = selection.renderNodes(node.children)
  if (!text) {
    return false
  }

  state.text += "[s]" + text + "[/s]"

  return true
}

function inline_code(selection, node, state) {
  if (node.type !== "inline_code") {
    return false
  }

  const { content } = node
  if (!content) {
    return false
  }

  state.text += "`" + content.replace("\\", "\\\\").replace("`", "\\`") + "`"

  return true
}

function softbreak(selection, node, state) {
  if (node.type !== "softbreak") {
    return false
  }

  // Softbreak render is noop
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
  { name: "header", func: header },
  { name: "youtube", func: youtube },
  { name: "paragraph", func: paragraph },
  { name: "strong_text", func: strong_text },
  { name: "emphasis_text", func: emphasis_text },
  { name: "bold_text", func: bold_text },
  { name: "italic_text", func: italic_text },
  { name: "underline_text", func: underline_text },
  { name: "strikethrough_text", func: strikethrough_text },
  { name: "inline_code", func: inline_code },
  { name: "softbreak", func: softbreak },
  { name: "text", func: text },
]
