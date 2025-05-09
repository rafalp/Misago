class QuoteCursorPosition {
  constructor() {
    this.shadow = document.createElement("div")
    this.shadow.ariaHidden = true
    this.shadow.style.position = "absolute"
    this.shadow.style.top = 0
    this.shadow.style.left = "-9999px"
    this.shadow.style.opacity = 0
    this.shadow.style.zIndex = -999
    document.body.appendChild(this.shadow)
  }

  getPosition(target, orgRange) {
    this.shadow.replaceChildren()
    this.shadow.setAttribute("class", target.getAttribute("class"))

    const targetRect = target.getBoundingClientRect()
    this.shadow.style.width = `${targetRect.width}px`
    this.shadow.style.height = `${targetRect.height}px`

    const range = orgRange.cloneRange()
    range.setStart(target.childNodes[0], 0)
    this.shadow.replaceChildren(...range.cloneContents().childNodes)

    const marker = document.createElement("span")
    this.shadow.querySelector("p:last-child").appendChild(marker)

    const rangeRect = range.getBoundingClientRect()
    const shadowRect = this.shadow.getBoundingClientRect()
    const markerRect = marker.getBoundingClientRect()
    const markerPosition = markerRect.x - shadowRect.x

    const rect = {
      bottom: targetRect.top + rangeRect.height,
      height: rangeRect.height,
      left: targetRect.left + markerPosition - 1,
      right: targetRect.left + markerPosition + 1,
      top: targetRect.top + 10,
      width: 2,
      x: targetRect.x + markerPosition - 1,
      y: targetRect.y + 10,
    }

    return {
      getBoundingClientRect() {
        return rect
      },
    }
  }
}

export default QuoteCursorPosition
