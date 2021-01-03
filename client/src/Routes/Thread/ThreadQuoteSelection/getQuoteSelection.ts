const getQuoteSelection = (container: HTMLDivElement) => {
  if (typeof window.getSelection === "undefined") return

  // Validate that selection is of valid type and has one range
  const selection = window.getSelection()
  if (!selection) return
  if (selection.type !== "Range") return
  if (selection.rangeCount !== 1) return

  // Validate that selection is within the container and post's article
  const range = selection.getRangeAt(0)
  if (!isRangeContained(range, container)) return
  if (!isPostContained(range)) return
  if (!isAnyTextSelected(range.cloneContents())) return

  return range
}

const isRangeContained = (range: Range, container: Node) => {
  const node = range.commonAncestorContainer
  if (node === container) return true

  let p = node.parentNode
  while (p) {
    if (p === container) return true
    p = p.parentNode
  }

  return false
}

const isPostContained = (range: Range) => {
  const element = range.commonAncestorContainer as HTMLElement
  if (element.nodeName === "ARTICLE") return true
  if (element.dataset?.noquote === "1") return false
  let p = element.parentNode as HTMLElement
  while (p) {
    if (p.dataset?.noquote === "1") return false
    if (p.nodeName === "ARTICLE") return true
    p = p.parentNode as HTMLElement
  }
  return false
}

const isAnyTextSelected = (node: DocumentFragment | Node): boolean => {
  for (let i = 0; i < node.childNodes.length; i++) {
    const child = node.childNodes[i]
    if (child.nodeType === Node.TEXT_NODE) {
      if (child.textContent && child.textContent.trim().length > 0) return true
    }
    if (child.nodeName === "IMG") return true
    if (isAnyTextSelected(child)) return true
  }

  return false
}

export default getQuoteSelection
