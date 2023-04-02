import renderComponent from "../utils/renderComponent"

export class Modal {
  init(element, root) {
    this._element = element
    this._root = root

    this._modal = $(element).modal({ show: false })

    this._modal.on("hidden.bs.modal", () => {
      this._root.unmount()
    })
  }

  show(component) {
    renderComponent(component, this._root)
    this._modal.modal("show")
  }

  hide() {
    this._modal.modal("hide")
  }
}

export default new Modal()
