class QuoteSelection {
  constructor(extractor, renderer) {
    this.extractor = extractor
    this.renderer = renderer
  }

  getQuote(root, nodes) {
    let document = this.extractNodes(nodes)
    document = this.wrapDocument(root, nodes, document)
    console.log(document)
    console.log(this.renderNodes(document).trim())
    return this.renderNodes(document).trim()
  }

  extractNodes(nodes, stack) {
    const { rules } = this.extractor
    const state = { document: [], stack: stack || [] }

    for (let i = 0; i < nodes.length; i++) {
      const node = nodes[i]
      console.log(node)
      for (let r = 0; r < rules.length; r++) {
        const rule = rules[r].func
        if (rule(this, node, state)) {
          break
        }
      }
    }

    return state.document
  }

  wrapDocument(root, nodes, document) {
    return document
  }

  renderNodes(document) {
    const { rules } = this.renderer
    const state = { text: "" }

    for (let i = 0; i < document.length; i++) {
      const node = document[i]
      for (let r = 0; r < rules.length; r++) {
        const rule = rules[r].func
        if (rule(this, node, state)) {
          break
        }
      }
    }

    return state.text
  }
}

export default QuoteSelection
