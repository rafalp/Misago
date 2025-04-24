function header(selection, state) {
  const { node } = state

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
  state.pos += 1

  return true
}

function youtube(selection, state) {
  const { node } = state

  if (node.type !== "youtube") {
    return false
  }

  if (state.text) {
    state.text += "\n\n"
  }

  state.text += node.url
  state.pos += 1

  return true
}

function paragraph(selection, state) {
  const { node } = state

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
  state.pos += 1

  return true
}

function link(selection, state) {
  const { node } = state

  if (node.type !== "link") {
    return false
  }

  const { auto, children, href } = node
  const text = selection.renderNodes(children)

  if (auto) {
    state.text += "<" + escapeAutolink(href) + ">"
  } else {
    state.text += "[url=" + escapeLinkHref(href) + "]" + text + "[/url]"
  }

  state.pos += 1

  return true
}

function escapeLinkHref(href) {
  return href.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")
}

function escapeAutolink(href) {
  return href.replace("\\", "\\\\").replace("<", "\\<").replace(">", "\\>")
}

function strong_text(selection, state) {
  const { node } = state

  if (node.type !== "strong") {
    return false
  }

  const text = selection.renderNodes(node.children)
  if (!text) {
    return false
  }

  const delimiter = text.indexOf("*") === -1 ? "**" : "__"
  state.text += delimiter + text + delimiter
  state.pos += 1

  return true
}

function emphasis_text(selection, state) {
  const { node } = state

  if (node.type !== "emphasis") {
    return false
  }

  const text = selection.renderNodes(node.children)
  if (!text) {
    return false
  }

  const delimiter = text.indexOf("*") === -1 ? "*" : "_"
  state.text += delimiter + text + delimiter
  state.pos += 1

  return true
}

function bold_text(selection, state) {
  const { node } = state

  if (node.type !== "bold") {
    return false
  }

  const text = selection.renderNodes(node.children)
  if (!text) {
    return false
  }

  state.text += "[b]" + text + "[/b]"
  state.pos += 1

  return true
}

function italic_text(selection, state) {
  const { node } = state

  if (node.type !== "italic") {
    return false
  }

  const text = selection.renderNodes(node.children)
  if (!text) {
    return false
  }

  state.text += "[i]" + text + "[/i]"
  state.pos += 1

  return true
}

function underline_text(selection, state) {
  const { node } = state

  if (node.type !== "underline") {
    return false
  }

  const text = selection.renderNodes(node.children)
  if (!text) {
    return false
  }

  state.text += "[u]" + text + "[/u]"
  state.pos += 1

  return true
}

function strikethrough_text(selection, state) {
  const { node } = state

  if (node.type !== "strikethrough") {
    return false
  }

  const text = selection.renderNodes(node.children)
  if (!text) {
    return false
  }

  state.text += "[s]" + text + "[/s]"
  state.pos += 1

  return true
}

function inline_code(selection, state) {
  const { node } = state

  if (node.type !== "inline_code") {
    return false
  }

  const { content } = node
  if (!content) {
    return false
  }

  state.text += "`" + content.replace("\\", "\\\\").replace("`", "\\`") + "`"
  state.pos += 1

  return true
}

function softbreak(selection, state) {
  const { node } = state

  if (node.type !== "softbreak") {
    return false
  }

  // Softbreak render is noop
  state.pos += 1
  return true
}

function text(selection, state) {
  const { node } = state

  if (node.type !== "text") {
    return false
  }

  state.text += node.content
  state.pos += 1

  return true
}

export default [
  { name: "header", func: header },
  { name: "youtube", func: youtube },
  { name: "paragraph", func: paragraph },
  { name: "link", func: link },
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
