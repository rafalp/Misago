export default class Lightbox {
  constructor() {
    this.modal = null
    this.pager = null
    this.details = null
    this.item = null
    this.caption = null

    this.state = null

    document.addEventListener("DOMContentLoaded", this._onDOMContentLoaded)
  }

  _onDOMContentLoaded = () => {
    this.modal = document.getElementById("misago-lightbox-modal")
    if (this.modal) {
      this.pager = this.modal.querySelector("[misago-lightbox-pager]")
      this.details = this.modal.querySelector("[misago-lightbox-details]")
      this.item = this.modal.querySelector("[misago-lightbox-item]")
      this.caption = this.modal.querySelector("[misago-lightbox-caption]")

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
    this.state = this.getInitialState(root, image)

    this.updateLightbox()
    this.showLightbox()
  }

  getInitialState(root, image) {
    const images = this.getRootImages(root, image)
    const index = images.map(({ active }) => active).indexOf(true)

    return {
      images,
      image: images[index],
      index: index,
      total: images.length,
    }
  }

  getRootImages(root, image) {
    const images = []

    root.querySelectorAll("[misago-lightbox-img]").forEach((element) => {
      const context = element.closest("[misago-lightbox-context]")

      images.push({
        element,
        active: element === image,
        caption: !!context ? context.querySelector("template") : null,
        details: !!context
          ? context.getAttribute("misago-lightbox-details")
          : null,
        link: element.closest("a"),
        url: !!context
          ? context.getAttribute("misago-lightbox-url")
          : element.getAttribute("src"),
      })
    })

    return images
  }

  updateLightbox() {
    this.updateLightboxPager()
    this.updateLightboxDetails()
    this.updateLightboxItem()
    this.updateLightboxCaption()
  }

  updateLightboxPager() {
    const { state, pager } = this
    if (state.total) {
      pager.textContent = pager
        .getAttribute("misago-lightbox-pager")
        .replace("%(total)s", state.total)
        .replace("%(index)s", state.index + 1)
      pager.classList.remove("d-none")
    } else {
      pager.textContent = ""
      pager.classList.add("d-none")
    }
  }

  updateLightboxDetails() {
    const { state, details } = this
    if (state.image.details) {
      details.setAttribute("href", state.image.details)
      details.classList.remove("d-none")
    } else {
      details.classList.add("d-none")
    }
  }

  updateLightboxItem() {
    const { state, item } = this
    const { image } = state

    const img = document.createElement("img")
    img.setAttribute("src", image.url)
    img.setAttribute("alt", "")
    item.replaceChildren(img)
  }

  updateLightboxCaption() {
    const { state, caption } = this
    const { image } = state

    if (image.caption) {
      caption.replaceChildren(image.caption.content.cloneNode(true))
    } else {
      if (image.link) {
        const a = document.createElement("a")
        const href = image.link.getAttribute("href")
        a.setAttribute("href", href)
        a.setAttribute("target", "_blank")
        a.textContent = this.cleanDisplayUrl(href)
        caption.replaceChildren(a)
      } else {
        caption.textContent = this.cleanDisplayUrl(
          image.element.getAttribute("src")
        )
      }
    }
  }

  cleanDisplayUrl(href) {
    if (href.startsWith("https://")) {
      return href.substring(8)
    } else if (href.startsWith("http://")) {
      return href.substring(7)
    }
    return href
  }

  showLightbox() {
    $(this.modal).modal("show")
  }
}
