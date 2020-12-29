const getQuoteMarkup = (range: Range) => {
  const metadata = getQuoteMetadata(range)
  let markup = metadata ? `[quote=${metadata}]\n` : "[quote]\n"
  markup += convertNodesToMarkup(range.cloneContents().childNodes, []).trim()
  markup += "\n[/quote]"
  return markup
}

export default getQuoteMarkup

const getQuoteMetadata = (range: Range): string => {
  const node = range.commonAncestorContainer
  if (isNodeElementWithQuoteMetadata(node)) {
    return getQuoteMetadataFromNode(node as HTMLElement)
  }

  let p = node.parentNode
  while (p) {
    if (isNodeElementWithQuoteMetadata(p)) {
      return getQuoteMetadataFromNode(p as HTMLElement)
    }
    p = p.parentNode
  }

  return ""
}

const isNodeElementWithQuoteMetadata = (node: Node): boolean => {
  if (node.nodeType !== Node.ELEMENT_NODE) return false
  return node.nodeName === "ARTICLE" || node.nodeName === "BLOCKQUOTE"
}

const getQuoteMetadataFromNode = (element: HTMLElement): string => {
  let metdata = ""
  if (element.dataset.author) {
    metdata += element.dataset.author
    if (element.dataset.post) {
      metdata += ";" + element.dataset.post
    }
  }
  return metdata
}

const convertNodesToMarkup = (
  nodes: NodeListOf<ChildNode>,
  stack: Array<string>
): string => {
  let markup = ""
  for (let i = 0; i < nodes.length; i++) {
    const node = nodes[i]
    markup += convertNodeToMarkup(node, [...stack, node.nodeName])
  }
  return markup
}

const SIMPLE_NODE_MAPPINGS: Record<string, [string, string]> = {
  H1: ["\n\n# ", ""],
  H2: ["\n\n## ", ""],
  H3: ["\n\n### ", ""],
  H4: ["\n\n#### ", ""],
  H5: ["\n\n##### ", ""],
  H6: ["\n\n###### ", ""],
  STRONG: ["**", "**"],
  EM: ["*", "*"],
  DEL: ["~~", "~~"],
  B: ["[b]", "[/b]"],
  U: ["[u]", "[/u]"],
  I: ["[i]", "[/i]"],
}

const convertNodeToMarkup = (
  node: ChildNode,
  stack: Array<string>
): string => {
  if (node.nodeType === Node.TEXT_NODE) {
    return node.textContent || ""
  }

  if (
    node.nodeType === Node.ELEMENT_NODE &&
    (node as HTMLElement).dataset?.noquote === "1"
  ) {
    return ""
  }

  if (node.nodeName === "HR") {
    return "- - -"
  }

  if (node.nodeName === "BR") {
    return "\n"
  }

  if (SIMPLE_NODE_MAPPINGS[node.nodeName]) {
    const [prefix, suffix] = SIMPLE_NODE_MAPPINGS[node.nodeName]
    return (
      prefix +
      convertNodesToMarkup(node.childNodes, [...stack, node.nodeName]) +
      suffix
    )
  }

  if (node.nodeName === "A") {
    const element = node as HTMLAnchorElement
    const href = element.href
    const text = convertNodesToMarkup(node.childNodes, [
      ...stack,
      node.nodeName,
    ])
    if (text) {
      return `[${text}](${href})`
    } else {
      return `!(${href})`
    }
  }

  if (node.nodeName === "IMG") {
    const element = node as HTMLImageElement
    const src = element.src
    const alt = element.alt
    if (alt) {
      return `![${alt}](${src})`
    } else {
      return `!(${src})`
    }
  }

  if (node.nodeName === "P") {
    return (
      "\n\n" + convertNodesToMarkup(node.childNodes, [...stack, node.nodeName])
    )
  }

  return ""
}
