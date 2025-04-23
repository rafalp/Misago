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
  { name: "text", func: text },
]
