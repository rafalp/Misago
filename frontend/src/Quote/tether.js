function attachment(cursor, node) {
  if (node.nodeName !== "DIV" && node.nodeName !== "SPAN") {
    return null
  }

  if (!node.hasAttribute("misago-attachment")) {
    return null
  }

  return node
}

function youtube(cursor, node) {
  if (node.nodeName !== "DIV") {
    return null
  }

  if (!node.hasAttribute("misago-youtube")) {
    return null
  }

  return node
}

function header(cursor, node) {
  if (["H1", "H2", "H3", "H4", "H5", "H6"].indexOf(node.nodeName) === -1) {
    return null
  }

  return cursor.findTether(node.childNodes)
}

function quote(cursor, node) {
  if (node.nodeName !== "ASIDE") {
    return null
  }

  const blockquote = node.querySelector("blockquote[misago-quote]")
  if (!blockquote) {
    return null
  }

  return cursor.findTether(blockquote.childNodes)
}

function spoiler(cursor, node) {
  if (node.nodeName !== "DETAILS") {
    return null
  }

  const body = node.querySelector("div[misago-spoiler]")
  if (!body) {
    return null
  }

  return cursor.findTether(body.childNodes)
}

function code(cursor, node) {
  if (!(node.nodeName === "DIV" || node.nodeName === "PRE")) {
    return null
  }

  const code = node.querySelector("code[misago-code]")
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

function image(cursor, node) {
  if (node.nodeName !== "IMG") {
    return null
  }

  return node
}

function text(_, node) {
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
  { name: "image", func: image },
  { name: "text", func: text },
]
