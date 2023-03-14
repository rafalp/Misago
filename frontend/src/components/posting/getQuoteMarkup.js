const getQuoteMarkup = (range) => {
  const metadata = getQuoteMetadata(range)
  let markup = convertNodesToMarkup(range.cloneContents().childNodes, [])
  let prefix = metadata ? `[quote="${metadata}"]\n` : "[quote]\n"
  let suffix = "\n[/quote]\n\n"

  const codeBlock = getQuoteCodeBlock(range)
  if (codeBlock) {
    prefix += codeBlock.syntax ? `[code=${codeBlock.syntax}]\n` : "[code]\n"
    suffix = "\n[/code]" + suffix
  } else if (isNodeInlineCodeBlock(range)) {
    markup = markup.trim()
    prefix += "`"
    suffix = "`" + suffix
  } else {
    markup = markup.trim()
  }

  return prefix + markup + suffix
}

export default getQuoteMarkup

const getQuoteMetadata = (range) => {
  const node = range.commonAncestorContainer
  if (isNodeElementWithQuoteMetadata(node)) {
    return getQuoteMetadataFromNode(node)
  }

  let p = node.parentNode
  while (p) {
    if (isNodeElementWithQuoteMetadata(p)) {
      return getQuoteMetadataFromNode(p)
    }
    p = p.parentNode
  }

  return ""
}

const isNodeElementWithQuoteMetadata = (node) => {
  if (node.nodeType !== Node.ELEMENT_NODE) return false
  if (node.nodeName === "ARTICLE") return true
  if (node.nodeName === "BLOCKQUOTE") {
    return node.dataset && node.dataset.block === "quote"
  }

  return false
}

const getQuoteMetadataFromNode = (element) => {
  if (element.dataset) {
    return element.dataset.author || null
  }
  return null
}

const getQuoteCodeBlock = (range) => {
  const node = range.commonAncestorContainer
  if (isNodeCodeBlock(node)) {
    return getNodeCodeBlockMeta(node)
  }

  let p = node.parentNode
  while (p) {
    if (isNodeCodeBlock(p)) {
      return getNodeCodeBlockMeta(p)
    }
    p = p.parentNode
  }

  return null
}

const isNodeCodeBlock = (node) => {
  return node.nodeName === "PRE"
}

const isNodeInlineCodeBlock = (range) => {
  const node = range.commonAncestorContainer
  if (node.nodeName === "CODE") {
    return true
  }

  let p = node.parentNode
  while (p) {
    if (isNodeElementWithQuoteMetadata(p)) {
      return false
    }

    if (p.nodeName === "CODE") {
      return true
    }

    p = p.parentNode
  }

  return false
}

const getNodeCodeBlockMeta = (node) => {
  if (!node.dataset) {
    return { syntax: null }
  }

  return { syntax: node.dataset.syntax || null }
}

const convertNodesToMarkup = (nodes, stack) => {
  let markup = ""
  for (let i = 0; i < nodes.length; i++) {
    const node = nodes[i]
    markup += convertNodeToMarkup(node, stack)
  }
  return markup
}

const SIMPLE_NODE_MAPPINGS = {
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

const convertNodeToMarkup = (node, stack) => {
  const dataset = node.dataset || {}

  if (node.nodeType === Node.TEXT_NODE) {
    return node.textContent || ""
  }

  if (node.nodeType === Node.ELEMENT_NODE) {
    if (dataset.quote) {
      return dataset.quote || ""
    }
    if (dataset.noquote === "1") return ""
  }

  if (
    node.nodeType === Node.ELEMENT_NODE &&
    dataset.quote &&
    dataset.quote.trim()
  ) {
    return ""
  }

  if (node.nodeName === "HR") {
    return "\n\n- - -"
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
    const href = node.href
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
    const src = node.src
    const alt = node.alt
    if (alt) {
      return `![${alt}](${src})`
    } else {
      return `!(${src})`
    }
  }

  if (node.nodeName === "DIV" || node.nodeName === "ASIDE") {
    const block = dataset.block && dataset.block.toUpperCase()
    if (block && SIMPLE_NODE_MAPPINGS[block]) {
      const [prefix, suffix] = SIMPLE_NODE_MAPPINGS[block]
      return (
        prefix +
        convertNodesToMarkup(node.childNodes, [...stack, block]) +
        suffix
      )
    } else {
      return convertNodesToMarkup(node.childNodes, stack)
    }
  }

  if (node.nodeName === "BLOCKQUOTE") {
    if (dataset.block === "spoiler") {
      const content = convertNodesToMarkup(node.childNodes, [
        ...stack,
        "SPOILER",
      ]).trim()

      if (!content) return ""

      let markup = "\n[spoiler]\n"
      markup += content
      markup += "\n[/spoiler]"
      return markup
    }

    const content = convertNodesToMarkup(node.childNodes, [
      ...stack,
      "QUOTE",
    ]).trim()

    if (!content) return ""

    const metadata = getQuoteMetadataFromNode(node)
    let markup = metadata ? `\n[quote=${metadata}]\n` : "\n\n[quote]\n"
    markup += content
    markup += "\n[/quote]"
    return markup
  }

  if (node.nodeName === "PRE") {
    const syntax = dataset.syntax || null
    const code = node.querySelector("code")
    const content = code ? code.innerText || "" : ""

    if (!content.trim()) return ""

    return "\n[code" + (syntax ? "=" + syntax : "") + "]" + content + "[/code]"
  }

  if (node.nodeName === "CODE") {
    return "`" + node.innerText + "`"
  }

  if (node.nodeName === "P") {
    return (
      "\n" + convertNodesToMarkup(node.childNodes, [...stack, node.nodeName])
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
      prefix += dataset.index ? dataset.index + ". " : "1. "
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
