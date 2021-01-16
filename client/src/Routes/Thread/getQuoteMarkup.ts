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
  if (node.nodeName === "ARTICLE") return true
  if (node.nodeName === "BLOCKQUOTE") {
    const element = node as HTMLQuoteElement
    return element.dataset?.block === "quote"
  }

  return false
}

const getQuoteMetadataFromNode = (element: HTMLElement): string => {
  let metdata = ""
  if (element.dataset.author) {
    metdata += element.dataset.author
    if (element.dataset.post) {
      metdata += ":" + element.dataset.post
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
    markup += convertNodeToMarkup(node, stack)
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
  SUB: ["[sub]", "[/sub]"],
  SUP: ["[sup]", "[/sup]"],
}

const convertNodeToMarkup = (
  node: ChildNode,
  stack: Array<string>
): string => {
  if (node.nodeType === Node.TEXT_NODE) {
    return node.textContent || ""
  }

  if (node.nodeType === Node.ELEMENT_NODE) {
    if ((node as HTMLElement).dataset?.quote) {
      return (node as HTMLElement).dataset?.quote || ""
    }
    if ((node as HTMLElement).dataset?.noquote === "1") return ""
  }

  if (
    node.nodeType === Node.ELEMENT_NODE &&
    (node as HTMLElement).dataset?.quote?.trim()
  ) {
    return ""
  }

  if (node.nodeName === "HR") {
    return "\n\n- - -"
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

  if (node.nodeName === "DIV") {
    return convertNodesToMarkup(node.childNodes, stack)
  }

  if (node.nodeName === "BLOCKQUOTE") {
    const element = node as HTMLQuoteElement
    if (element.dataset?.block === "quote") {
      const content = convertNodesToMarkup(node.childNodes, [
        ...stack,
        "QUOTE",
      ]).trim()

      if (!content) return ""

      const metadata = getQuoteMetadataFromNode(element)
      let markup = metadata ? `\n\n[quote=${metadata}]\n` : "\n\n[quote]\n"
      markup += content
      markup += "\n[/quote]"
      return markup
    }

    if (element.dataset?.block === "spoiler") {
      const content = convertNodesToMarkup(node.childNodes, [
        ...stack,
        "SPOILER",
      ]).trim()

      if (!content) return ""

      let markup = "\n\n[spoiler]\n"
      markup += content
      markup += "\n[/spoiler]"
      return markup
    }
  }

  if (node.nodeName === "PRE") {
    const element = node as HTMLPreElement
    const syntax = element.dataset?.syntax || null
    const content = element.querySelector("code")?.innerText || ""

    if (!content.trim()) return ""

    return (
      "\n\n[code" + (syntax ? "=" + syntax : "") + "]" + content + "[/code]"
    )
  }

  if (node.nodeName === "CODE") {
    return (
      "`" +
      convertNodesToMarkup(node.childNodes, [...stack, node.nodeName]) +
      "`"
    )
  }

  if (node.nodeName === "P") {
    return (
      "\n\n" + convertNodesToMarkup(node.childNodes, [...stack, node.nodeName])
    )
  }

  if (node.nodeName === "UL" || node.nodeName === "OL") {
    const level = stack.filter((item) => item === "OL" || item === "UL").length
    const prefix = level === 0 ? "\n" : ""
    return (
      prefix + convertNodesToMarkup(node.childNodes, [...stack, node.nodeName])
    )
  }

  if (node.nodeName === "LI") {
    let prefix = ""
    const level = stack.filter((item) => item === "OL" || item === "UL").length
    for (let i = 1; i < level; i++) {
      prefix += "    "
    }

    const ordered = stack[stack.length - 1] === "OL"
    if (ordered) {
      const element = node as HTMLLIElement
      prefix += element.dataset?.index ? element.dataset.index + ". " : "1. "
    } else {
      prefix += "- "
    }

    const content = convertNodesToMarkup(node.childNodes, [
      ...stack,
      node.nodeName,
    ])
    if (!content.trim()) return ""

    return "\n" + prefix + content
  }

  if (node.nodeName === "SPAN") {
    return convertNodesToMarkup(node.childNodes, stack)
  }

  return ""
}
