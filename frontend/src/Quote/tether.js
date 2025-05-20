function text(nodes) {
  if (!nodes.length) {
    return null
  }

  let result = null

  for (let i = 0; i < nodes.length; i++) {
    const node = nodes[i]
    if (node.nodeType === Node.TEXT_NODE) {
      const text = node.textContent.trimEnd()
      if (text) {
        const range = document.createRange()
        range.selectNode(node)
        range.setStart(node, text.length)
        range.setEnd(node, text.length)
        result = range
      }
    } else if (typeof node.childNodes !== "undefined") {
      if (!node.hasAttribute("misago-selection-boundary")) {
        result = text(node.childNodes) || result
      }
    }
  }

  return result
}

export default [{ name: "text", func: text }]
