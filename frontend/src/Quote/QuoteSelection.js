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
    const state = {
      nodes,
      node: null,
      document: [],
      stack: stack || [],
      pos: 0,
      posMax: nodes.length - 1,
    }

    while (state.pos <= state.posMax) {
      let match = false

      const node = nodes[state.pos]
      state.node = node

      for (let r = 0; r < rules.length; r++) {
        const rule = rules[r].func
        if (rule(this, state)) {
          match = true
          break
        }
      }

      state.pos += match ? 0 : 1
    }

    return state.document
  }

  wrapDocument(root, nodes, document) {
    if (document.length === 1 && document[0].type === "quote") {
      return document
    }

    return [
      {
        type: "quote",
        info: root.info,
        children: document,
      },
    ]
  }

  renderNodes(document) {
    const { rules } = this.renderer
    const state = {
      document,
      node: null,
      text: "",
      pos: 0,
      posMax: document.length - 1,
    }

    while (state.pos <= state.posMax) {
      let match = false

      const node = document[state.pos]
      state.node = node

      for (let r = 0; r < rules.length; r++) {
        const rule = rules[r].func
        if (rule(this, state)) {
          match = true
          break
        }
      }

      state.pos += match ? 0 : 1
    }

    return state.text
  }
}

export default QuoteSelection
