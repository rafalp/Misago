class QuoteSelection {
  constructor(extractor, renderer, postprocess) {
    this.extractor = extractor
    this.renderer = renderer
    this.postprocess = postprocess
  }

  getQuote(root) {
    let result = this.extractNodes(root.childNodes)
    result = this.postprocessNodes(root, result)
    if (result.length === 0) {
      return ""
    }
    return this.renderNodes(result).trim()
  }

  extractNodes(nodes, stack) {
    const state = {
      nodes,
      node: null,
      result: [],
      stack: stack || [],
      pos: 0,
      posMax: nodes.length - 1,
    }

    const { rules } = this.extractor
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

    return state.result
  }

  postprocessNodes(root, nodes) {
    let result = nodes

    const { rules } = this.postprocess
    for (let i = 0; i < rules.length; i++) {
      result = rules[i].func(this, root, result)
    }

    return result
  }

  renderNodes(nodes) {
    const state = {
      nodes,
      node: null,
      text: "",
      pos: 0,
      posMax: nodes.length - 1,
    }

    const { rules } = this.renderer
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

    return state.text
  }
}

export default QuoteSelection
