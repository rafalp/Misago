import shadow from "./ControlShadow"

class AnchorInput {
  constructor(element) {
    this.element = element
  }

  getTarget = (query) => {
    const rect = shadow.getQueryBoundingClientRect(this.element, query)

    return {
      getBoundingClientRect() {
        return rect
      },
    }
  }
}

export default AnchorInput
