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

  getPosition(target, range) {
    this.shadow.setAttribute("class", target.getAttribute("class"))

    const rangeRect = range.getBoundingClientRect()
    this.shadow.style.width = `${rangeRect.width}px`

    if (this.padding === null) {
      const padding = window
        .getComputedStyle(target)
        .getPropertyValue("padding-top")
      this.padding = parseFloat(padding.substring(0, padding.length - 2))
    }

    const clone = range.cloneContents()
    this.shadow.replaceChildren(...clone.childNodes)

    const tether = this.findTether(this.shadow.childNodes)
    if (!tether) {
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

    return {
      getBoundingClientRect() {
        return rect
      },
    }
  }

  findTether(nodes) {
    const { rules } = this.tether
    for (let i = 0; i < rules.length; i++) {
      const { func } = rules[i]
      const target = func(nodes)
      if (target) {
        return target
      }
    }

    return null
  }
}

export default QuoteCursorPosition
