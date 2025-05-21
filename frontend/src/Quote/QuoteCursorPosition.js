class QuoteCursorPosition {
  constructor(tether) {
    this.tether = tether

    this.shadow = this.createShadow()
    this.padding = null
  }

  createShadow() {
    const shadow = document.createElement("div")
    shadow.ariaHidden = true
    shadow.style.position = "absolute"
    shadow.style.top = 0
    shadow.style.left = "-9999px"
    shadow.style.opacity = 0
    shadow.style.zIndex = -999

    document.body.appendChild(shadow)

    return shadow
  }

  getPosition(root, range) {
    const { element, ancestor } = root

    this.shadow.setAttribute("class", element.getAttribute("class"))

    const rangeRect = range.getBoundingClientRect()
    this.shadow.style.width = `${rangeRect.width}px`

    if (this.padding === null) {
      const padding = window
        .getComputedStyle(element)
        .getPropertyValue("padding-top")
      this.padding = parseFloat(padding.substring(0, padding.length - 2))
    }

    const clone = range.cloneContents()
    this.shadow.replaceChildren(...clone.childNodes)

    const tether = this.findTether(this.shadow.childNodes)
    if (!tether) {
      this.shadow.replaceChildren()
      return null
    }

    const shadowRect = this.shadow.getBoundingClientRect()
    const tetherRect = tether.getBoundingClientRect()
    const tetherOffset = {
      x: tetherRect.x - shadowRect.x + tetherRect.width,
      y: tetherRect.y - shadowRect.y + tetherRect.height - this.padding,
    }

    const rect = {
      top: rangeRect.y + tetherOffset.y,
      bottom: rangeRect.y + tetherOffset.y + 1,
      left: rangeRect.x + tetherOffset.x,
      right: rangeRect.x + tetherOffset.x + 1,
      height: 1,
      width: 1,
      x: rangeRect.x + tetherOffset.x,
      y: rangeRect.y + tetherOffset.y,
    }

    this.shadow.replaceChildren()

    return {
      getBoundingClientRect() {
        return rect
      },
    }
  }

  findTether(nodes) {
    let result = null

    const { rules } = this.tether
    for (let i = 0; i < nodes.length; i++) {
      const node = nodes[i]

      for (let i = 0; i < rules.length; i++) {
        const { func } = rules[i]
        result = func(this, node) || result
      }
    }

    return result
  }
}

export default QuoteCursorPosition
