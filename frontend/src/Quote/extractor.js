function header(selection, node, { document, stack }) {
  if (["H1", "H2", "H3", "H4", "H5", "H6"].indexOf(node.nodeName) === -1) {
    return false
  }

  const children = selection.extractNodes(
    node.childNodes,
    stack.concat(["header"])
  )

  if (!children.length) {
    return true
  }

  const level = parseInt(node.nodeName.substring(1))

  document.push({
    type: "header",
    level,
    children,
  })

  return true
}

function youtube(selection, node, { document, stack }) {
  if (node.nodeName !== "IFRAME") {
    return false
  }

  const url = node.getAttribute("misago-youtube")
  if (!url) {
    return false
  }

  document.push({
    type: "youtube",
    url,
  })

  return true
}

function paragraph(selection, node, { document, stack }) {
  if (node.nodeName !== "P") {
    return false
  }

  const children = selection.extractNodes(
    node.childNodes,
    stack.concat(["paragraph"])
  )

  if (!children.length) {
    return true
  }

  document.push({
    type: "paragraph",
    children,
  })

  return true
}

function mention(selection, node, { document }) {
  if (!(node.nodeName === "A" || node.nodeName === "SPAN")) {
    return false
  }

  if (!node.getAttribute("misago-mention")) {
    return false
  }

  document.push({
    type: "text",
    content: node.textContent,
  })

  return true
}

function link(selection, node, { document, stack }) {
  if (node.nodeName !== "A") {
    return false
  }

  document.push({
    type: "link",
    href: node.getAttribute("href"),
    children: selection.extractNodes(node.childNodes, stack.concat(["link"])),
  })

  return true
}

function strong_text(selection, node, { document, stack }) {
  if (node.nodeName !== "STRONG") {
    return false
  }

  document.push({
    type: "strong",
    children: selection.extractNodes(
      node.childNodes,
      stack.concat(["strong_text"])
    ),
  })

  return true
}

function emphasis_text(selection, node, { document, stack }) {
  if (node.nodeName !== "EM") {
    return false
  }

  document.push({
    type: "emphasis",
    children: selection.extractNodes(
      node.childNodes,
      stack.concat(["emphasis_text"])
    ),
  })

  return true
}

function bold_text(selection, node, { document, stack }) {
  if (node.nodeName !== "B") {
    return false
  }

  document.push({
    type: "bold",
    children: selection.extractNodes(
      node.childNodes,
      stack.concat(["bold_text"])
    ),
  })

  return true
}

function italic_text(selection, node, { document, stack }) {
  if (node.nodeName !== "I") {
    return false
  }

  document.push({
    type: "italic",
    children: selection.extractNodes(
      node.childNodes,
      stack.concat(["italic_text"])
    ),
  })

  return true
}

function underline_text(selection, node, { document, stack }) {
  if (node.nodeName !== "U") {
    return false
  }

  document.push({
    type: "underline",
    children: selection.extractNodes(
      node.childNodes,
      stack.concat(["underline_text"])
    ),
  })

  return true
}

function strikethrough_text(selection, node, { document, stack }) {
  if (node.nodeName !== "DEL") {
    return false
  }

  document.push({
    type: "strikethrough",
    children: selection.extractNodes(
      node.childNodes,
      stack.concat(["strikethrough_text"])
    ),
  })

  return true
}

function text(selection, node, { document }) {
  if (node.nodeType !== Node.TEXT_NODE) {
    return false
  }

  if (node.textContent === "\n") {
    return true
  }

  document.push({
    type: "text",
    content: node.textContent,
  })

  return true
}

export default [
  { name: "header", func: header },
  { name: "youtube", func: youtube },
  { name: "paragraph", func: paragraph },
  { name: "mention", func: mention },
  { name: "link", func: link },
  { name: "strong_text", func: strong_text },
  { name: "emphasis_text", func: emphasis_text },
  { name: "bold_text", func: bold_text },
  { name: "italic_text", func: italic_text },
  { name: "underline_text", func: underline_text },
  { name: "strikethrough_text", func: strikethrough_text },
  { name: "text", func: text },
]
