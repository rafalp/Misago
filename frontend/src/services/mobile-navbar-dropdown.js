import renderComponent from "../utils/renderComponent"

export class MobileNavbarDropdown {
  init(element, root) {
    this._element = element
    this._root = root
    this._component = null
  }

  show(component) {
    if (this._component === component) {
      this.hide()
    } else {
      this._component = component
      renderComponent(component, this._root)
      $(this._element).addClass("open")
    }
  }

  showConnected(name, component) {
    if (this._component === name) {
      this.hide()
    } else {
      this._component = name
      renderComponent(component, this._root)
      $(this._element).addClass("open")
    }
  }

  hide() {
    $(this._element).removeClass("open")
    this._root.unmount()
    this._component = null
  }
}

export default new MobileNavbarDropdown()
