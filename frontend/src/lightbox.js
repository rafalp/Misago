export default class Lightbox {
  constructor() {
    this.element = null

    document.addEventListener("DOMContentLoaded", this._onDOMContentLoaded)
  }

  _onDOMContentLoaded = () => {
    this.element = document.getElementById("misago-lightbox-modal")
    if (this.element) {
      this._registerEvents()
    }
  }

  _registerEvents() {
    document.addEventListener("click", (event) => {
      const image = event.target.closest("[misago-lightbox-img]")
      if (!!image) {
        this.onImageClick(event, image)
      }
    })
  }

  onImageClick(event, image) {
    event.preventDefault()

    const root = image.closest("[misago-lightbox-root]")
    const images = this.getRootImages(root, image)

    this.updateLightbox(images)
    this.showLightbox()
  }

  getRootImages(root, image) {
    const images = []

    root.querySelectorAll("[misago-lightbox-img]").forEach((element) => {
      const context = element.closest("[misago-lightbox-img-context]")

      images.push({
        element,
        active: element === image,
        details: !!context ? context.querySelector("template") : null,
      })
    })

    return images
  }

  updateLightbox(images) {
    console.log(images)
  }

  showLightbox() {
    $(this.element).modal("show")
  }
}
