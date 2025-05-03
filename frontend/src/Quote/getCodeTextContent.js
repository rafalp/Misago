export default function getCodeTextContent(node) {
  console.log(node.textContent)
  let text = ""
  for (let i = 0; i < node.children.length; i++) {
    const child = node.children[i]
    if (child.nodeType === Node.TEXT_NODE) {
      text += child.textContent
    } else if (child.nodeName === "SPAN") {
      console.log(child, child.children)
      text += child.textContent
    }
  }
  return text
}
