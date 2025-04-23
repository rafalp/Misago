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
  { name: "paragraph", func: paragraph },
  { name: "mention", func: mention },
  { name: "link", func: link },
  { name: "bold_text", func: bold_text },
  { name: "italic_text", func: italic_text },
  { name: "underline_text", func: underline_text },
  { name: "strikethrough_text", func: strikethrough_text },
  { name: "text", func: text },
]
