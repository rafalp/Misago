class ControlShadow {
  constructor() {
    this._shadow = null
  }

  getQueryBoundingClientRect(control, query) {
    const shadow = this._getShadowElement()

    const rectControl = control.getBoundingClientRect()
    shadow.style.width = `${rectControl.width}px`
    shadow.style.height = `${rectControl.height}px`

    shadow.setAttribute("class", control.getAttribute("class"))
    shadow.innerHTML = query.prefix || ""

    const marker = document.createElement("span")
    marker.innerHTML = query.value
    shadow.appendChild(marker)

    const rectShadow = shadow.getBoundingClientRect()
    const rectMarker = marker.getBoundingClientRect()

    return {
      bottom:
        rectControl.bottom -
        rectMarker.bottom -
        rectShadow.bottom +
        control.scrollTop,
      height: rectMarker.height,
      left: rectControl.left + rectMarker.left - rectShadow.left,
      right: rectControl.right - rectMarker.right - rectShadow.right,
      top:
        rectControl.top + rectMarker.top - rectShadow.top - control.scrollTop,
      width: rectMarker.width,
      x: rectControl.x + rectMarker.x - rectShadow.x,
      y: rectControl.y + rectMarker.y - rectShadow.y,
    }
  }

  _getShadowElement() {
    if (this._shadow) {
      return this._shadow
    }

    const shadow = this._createShadowElement()
    document.body.appendChild(shadow)
    this._shadow = shadow
    return shadow
  }

  _createShadowElement() {
    const shadow = document.createElement("pre")
    shadow.ariaHidden = true
    shadow.style.position = "absolute"
    shadow.style.top = 0
    shadow.style.left = "-9999px"
    shadow.style.opacity = 0
    shadow.style.zIndex = -999
    return shadow
  }
}

const shadow = new ControlShadow()

export default shadow
