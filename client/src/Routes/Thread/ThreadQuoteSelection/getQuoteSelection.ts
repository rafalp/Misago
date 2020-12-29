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
  if (!isAnyTextSelected(range)) return

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
  const element = range.commonAncestorContainer
  if (element.nodeName === "ARTICLE") return true
  let p = element.parentNode
  while (p) {
    if (p.nodeName === "ARTICLE") return true
    p = p.parentNode
  }
  return false
}

const isAnyTextSelected = (range: Range) => {
  return range.toString().trim().length > 0
}

export default getQuoteSelection
