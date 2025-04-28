function youtube(selection, state) {
  const { document, node } = state

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

  state.pos += 1
  return true
}

function header(selection, state) {
  const { document, node, stack } = state

  if (["H1", "H2", "H3", "H4", "H5", "H6"].indexOf(node.nodeName) === -1) {
    return false
  }

  const children = selection.extractNodes(
    node.childNodes,
    stack.concat(["header"])
  )

  if (!children.length) {
    state.pos += 1
    return true
  }

  const level = parseInt(node.nodeName.substring(1))

  document.push({
    type: "header",
    level,
    children,
  })

  state.pos += 1
  return true
}

function quote(selection, state) {
  const { document, node, stack } = state

  if (node.nodeName !== "ASIDE") {
    return false
  }

  const blockquote = node.querySelector("blockquote[misago-quote]")
  if (!blockquote) {
    return false
  }

  const info = blockquote.getAttribute("misago-quote")

  const children = selection.extractNodes(
    blockquote.childNodes,
    stack.concat(["quote"])
  )

  if (!children.length) {
    state.pos += 1
    return true
  }

  document.push({
    type: "quote",
    info,
    children,
  })

  state.pos += 1
  return true
}

function paragraph(selection, state) {
  const { document, node, stack } = state

  if (node.nodeName !== "P") {
    return false
  }

  const children = selection.extractNodes(
    node.childNodes,
    stack.concat(["paragraph"])
  )

  if (!children.length) {
    state.pos += 1
    return true
  }

  document.push({
    type: "paragraph",
    children,
  })

  state.pos += 1
  return true
}

function image(selection, state) {
  const { document, node } = state

  if (node.nodeName !== "IMG") {
    return false
  }

  const url = (node.getAttribute("src") || "").trim()
  const alt = (node.getAttribute("alt") || "").trim() || null
  const title = (node.getAttribute("title") || "").trim() || null

  if (!url) {
    return false
  }

  document.push({
    type: "image",
    url,
    alt,
    title,
  })

  state.pos += 1
  return true
}

function mention(selection, state) {
  const { document, node } = state

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

  state.pos += 1
  return true
}

function link(selection, state) {
  const { document, node, stack } = state

  if (node.nodeName !== "A") {
    return false
  }

  document.push({
    type: "link",
    href: node.getAttribute("href"),
    auto: (node.getAttribute("misago-autolink") || "").toLowerCase() == "true",
    children: selection.extractNodes(node.childNodes, stack.concat(["link"])),
  })

  state.pos += 1
  return true
}

function strong_text(selection, state) {
  const { document, node, stack } = state

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

  state.pos += 1
  return true
}

function emphasis_text(selection, state) {
  const { document, node, stack } = state

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

  state.pos += 1
  return true
}

function bold_text(selection, state) {
  const { document, node, stack } = state

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

  state.pos += 1
  return true
}

function italic_text(selection, state) {
  const { document, node, stack } = state

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

  state.pos += 1
  return true
}

function underline_text(selection, state) {
  const { document, node, stack } = state

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

  state.pos += 1
  return true
}

function strikethrough_text(selection, state) {
  const { document, node, stack } = state

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

  state.pos += 1
  return true
}

function inline_code(selection, state) {
  const { document, node, stack } = state

  if (node.nodeName !== "CODE") {
    return false
  }

  document.push({
    type: "inline_code",
    content: node.textContent,
  })

  state.pos += 1
  return true
}

function softbreak(selection, state) {
  const { document, node, stack } = state

  if (node.nodeName !== "BR") {
    return false
  }

  document.push({
    type: "softbreak",
  })

  state.pos += 1
  return true
}

function text(selection, state) {
  const { document, node, stack } = state

  if (node.nodeType !== Node.TEXT_NODE) {
    return false
  }

  if (node.textContent === "\n") {
    state.pos += 1
    return true
  }

  document.push({
    type: "text",
    content: node.textContent,
  })

  state.pos += 1
  return true
}

export default [
  { name: "youtube", func: youtube },
  { name: "header", func: header },
  { name: "quote", func: quote },
  { name: "paragraph", func: paragraph },
  { name: "image", func: image },
  { name: "mention", func: mention },
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
