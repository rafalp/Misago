class AnchorElement {
  constructor(element) {
    this.element = element
  }

  getTarget = (_query) => {
    return {
      getBoundingClientRect: () => {
        return this.element.getBoundingClientRect()
      },
    }
  }
}

export default AnchorElement
