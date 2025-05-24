function attachment(cursor, node) {
  if (node.nodeName !== "DIV" && node.nodeName !== "SPAN") {
    return null
  }

  if (!node.hasAttribute("misago-rich-text-attachment")) {
    return null
  }

  return node
}

function youtube(cursor, node) {
  if (node.nodeName !== "DIV") {
    return null
  }

  if (!node.hasAttribute("misago-rich-text-youtube")) {
    return null
  }

  return node
}

const HEADER_NODES = {
  H1: true,
  H2: true,
  H3: true,
  H4: true,
  H5: true,
  H6: true,
}

function header(cursor, node) {
  if (!HEADER_NODES[node.nodeName]) {
    return null
  }

  return cursor.findTether(node.childNodes)
}

function quote(cursor, node) {
  if (node.nodeName !== "ASIDE") {
    return null
  }

  const blockquote = node.querySelector("blockquote[misago-rich-text-quote]")
  if (!blockquote) {
    return null
  }

  return cursor.findTether(blockquote.childNodes)
}

function spoiler(cursor, node) {
  if (node.nodeName !== "DETAILS") {
    return null
  }

  const body = node.querySelector("div[misago-rich-text-spoiler]")
  if (!body) {
    return null
  }

  return cursor.findTether(body.childNodes)
}

function code(cursor, node) {
  if (!(node.nodeName === "DIV" || node.nodeName === "PRE")) {
    return null
  }

  const code = node.querySelector("code[misago-rich-text-code]")
  if (!code) {
    return null
  }

  const result = code.childNodes[code.childNodes.length - 1]
  if (result.nodeName === "SPAN") {
    return cursor.findTether(result.childNodes)
  }

  return cursor.findTether(code.childNodes)
}

function paragraph(cursor, node) {
  if (node.nodeName !== "P") {
    return null
  }

  return cursor.findTether(node.childNodes)
}

const TABLE_NODES = {
  TABLE: true,
  THEAD: true,
  TBODY: true,
  TR: true,
  TH: true,
  TD: true,
}

function table(cursor, node) {
  if (
    node.nodeName === "DIV" &&
    node.getAttribute("misago-rich-text") === "table-container"
  ) {
    return cursor.findTether(node.childNodes)
  }

  if (!node.nodeName || !TABLE_NODES[node.nodeName]) {
    return null
  }

  return cursor.findTether(node.childNodes)
}

const LIST_NODES = {
  OL: true,
  UL: true,
  LI: true,
}

function list(cursor, node) {
  if (!node.nodeName || !LIST_NODES[node.nodeName]) {
    return null
  }

  return cursor.findTether(node.childNodes)
}

function hr(cursor, node) {
  if (node.nodeName !== "HR") {
    return null
  }

  return node
}

function image(cursor, node) {
  if (node.nodeName !== "IMG") {
    return null
  }

  return node
}

function link(cursor, node) {
  if (node.nodeName !== "A") {
    return null
  }

  return cursor.findTether(node.childNodes)
}

function strong_text(cursor, node) {
  if (node.nodeName !== "STRONG") {
    return null
  }

  return cursor.findTether(node.childNodes)
}

function emphasis_text(cursor, node) {
  if (node.nodeName !== "EM") {
    return null
  }

  return cursor.findTether(node.childNodes)
}

function bold_text(cursor, node) {
  if (node.nodeName !== "B") {
    return null
  }

  return cursor.findTether(node.childNodes)
}

function italic_text(cursor, node) {
  if (node.nodeName !== "I") {
    return null
  }

  return cursor.findTether(node.childNodes)
}

function underline_text(cursor, node) {
  if (node.nodeName !== "U") {
    return null
  }

  return cursor.findTether(node.childNodes)
}

function strikethrough_text(cursor, node) {
  if (node.nodeName !== "DEL") {
    return null
  }

  return cursor.findTether(node.childNodes)
}

function inline_code(cursor, node) {
  if (node.nodeName !== "CODE") {
    return null
  }

  return cursor.findTether(node.childNodes)
}

function text(cursor, node) {
  if (node.nodeType !== Node.TEXT_NODE) {
    return null
  }

  const text = node.textContent.trimEnd()
  if (!text) {
    return null
  }

  const range = document.createRange()
  range.selectNode(node)
  range.setStart(node, text.length)
  range.setEnd(node, text.length)

  return range
}

export default [
  { name: "attachment", func: attachment },
  { name: "youtube", func: youtube },
  { name: "header", func: header },
  { name: "quote", func: quote },
  { name: "spoiler", func: spoiler },
  { name: "code", func: code },
  { name: "paragraph", func: paragraph },
  { name: "table", func: table },
  { name: "list", func: list },
  { name: "hr", func: hr },
  { name: "image", func: image },
  { name: "link", func: link },
  { name: "strong_text", func: strong_text },
  { name: "emphasis_text", func: emphasis_text },
  { name: "bold_text", func: bold_text },
  { name: "italic_text", func: italic_text },
  { name: "underline_text", func: underline_text },
  { name: "strikethrough_text", func: strikethrough_text },
  { name: "inline_code", func: inline_code },
  { name: "text", func: text },
]
