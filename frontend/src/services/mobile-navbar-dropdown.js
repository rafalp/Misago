import mount from "misago/utils/mount-component"

export class MobileNavbarDropdown {
  init(element) {
    this._element = element
    this._component = null
  }

  show(component) {
    if (this._component === component) {
      this.hide()
    } else {
      this._component = component
      mount(component, this._element.id)
      $(this._element).addClass("open")
    }
  }

  showConnected(name, component) {
    if (this._component === name) {
      this.hide()
    } else {
      this._component = name
      mount(component, this._element.id, true)
      $(this._element).addClass("open")
    }
  }

  hide() {
    $(this._element).removeClass("open")
    this._component = null
  }
}

export default new MobileNavbarDropdown()
