import {
  escapeAutolink,
  escapeBBCodeArg,
  escapeBBCodeContents,
  escapeInlineCode,
  escapeMarkdownLink,
  escapeMarkdownLinkText,
  escapeMarkdownLinkTitle,
} from "./escape"

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
    state.text += "\n\n"
  }

  const prefix = "#".repeat(node.level)
  state.text += prefix + " " + text
  state.pos += 1

  return true
}

function quote(selection, state) {
  const { node } = state

  if (node.type !== "quote") {
    return false
  }

  const text = selection.renderNodes(node.children).trim()
  if (!text) {
    return false
  }

  if (state.text) {
    state.text += "\n\n"
  }

  const { info } = node

  state.text += "[quote" + (info ? "=" + escapeBBCodeArg(info) : "") + "]\n"
  state.text += text
  state.text += "\n[/quote]"
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

function image(selection, state) {
  const { node } = state

  if (node.type !== "image") {
    return false
  }

  const { url, alt, title } = node

  if (alt || title) {
    state.text += "!"
    if (alt) {
      state.text += "[" + escapeMarkdownLinkText(alt) + "]"
    }
    state.text += "(" + escapeMarkdownLink(url)
    if (title) {
      state.text += ' "' + escapeMarkdownLinkTitle(title) + '"'
    }
    state.text += ")"
  } else {
    state.text += "[img]" + escapeBBCodeContents(url) + "[/img]"
  }

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
    state.text += "[url=" + escapeBBCodeArg(href) + "]" + text + "[/url]"
  }

  state.pos += 1

  return true
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

  const delimiter = text.indexOf("_") === -1 ? "__" : "**"
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

  const delimiter = text.indexOf("_") === -1 ? "_" : "**"
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

  state.text += "`" + escapeInlineCode(content) + "`"
  state.pos += 1

  return true
}

function softbreak(selection, state) {
  const { node } = state

  if (node.type !== "softbreak") {
    return false
  }

  state.text += "\n"

  state.pos += 1
  return true
}

function text(selection, state) {
  const { node } = state

  if (node.type !== "text") {
    return false
  }

  // We rely on 'softbreak' rule for explicit line breaks
  state.text += node.content.replaceAll("\n", "")
  state.pos += 1

  return true
}

export default [
  { name: "youtube", func: youtube },
  { name: "header", func: header },
  { name: "quote", func: quote },
  { name: "paragraph", func: paragraph },
  { name: "image", func: image },
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
