class QuoteCursorPosition {
  constructor(tether) {
    this.tether = tether

    this.shadow = this.createShadow()

    this.offsetY = null
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

  getPosition(target, orgRange) {
    this.shadow.replaceChildren()
    this.shadow.setAttribute("class", target.getAttribute("class"))

    const orgRangeRect = orgRange.getBoundingClientRect()
    this.shadow.style.width = `${orgRangeRect.width}px`

    if (this.offsetY === null) {
      const padding = window
        .getComputedStyle(target)
        .getPropertyValue("padding-top")
      this.offsetY = parseFloat(padding.substring(0, padding.length - 2))
    }

    const range = orgRange.cloneRange()
    range.setStart(target.childNodes[0], 0)
    const rangeChildNodes = range.cloneContents().childNodes

    const marker = document.createElement("span")
    const marketTarget = this.findMarkerTargetNode(rangeChildNodes)

    if (marketTarget) {
      marketTarget.appendChild(marker)
      this.shadow.replaceChildren(...rangeChildNodes)
    } else {
      this.shadow.replaceChildren(...rangeChildNodes)
      this.shadow.appendChild(marker)
    }

    const targetRect = target.getBoundingClientRect()
    const rangeRect = range.getBoundingClientRect()
    const shadowRect = this.shadow.getBoundingClientRect()
    const markerRect = marker.getBoundingClientRect()
    const markerX = markerRect.x - shadowRect.x

    const rect = {
      bottom: targetRect.top + rangeRect.height + this.offsetY,
      height: rangeRect.height,
      left: targetRect.left + markerX - 1,
      right: targetRect.left + markerX + 1,
      top: targetRect.top + this.offsetY,
      width: 2,
      x: targetRect.x + markerX - 1,
      y: targetRect.y,
    }

    return {
      getBoundingClientRect() {
        return rect
      },
    }
  }

  findMarkerTargetNode(nodes) {
    const node = nodes[nodes.length - 1]
    if (node.nodeType === Node.TEXT_NODE) {
      return null
    } else if (node.childNodes && node.childNodes.length) {
      return this.findMarkerTargetNode(node.childNodes) || node
    }
    return node
  }
}

export default QuoteCursorPosition
