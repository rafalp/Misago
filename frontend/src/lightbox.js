export default class Lightbox {
  constructor() {
    this.modal = null
    this.pager = null
    this.details = null
    this.zoom = null
    this.download = null
    this.link = null
    this.container = null
    this.caption = null

    this.state = null

    document.addEventListener("DOMContentLoaded", this._onDOMContentLoaded)
  }

  _onDOMContentLoaded = () => {
    this.modal = document.getElementById("misago-lightbox-modal")
    if (this.modal) {
      this.pager = this.modal.querySelector("[misago-lightbox-pager]")
      this.details = this.modal.querySelector("[misago-lightbox-details]")
      this.zoom = this.modal.querySelector("[misago-lightbox-zoom]")
      this.download = this.modal.querySelector("[misago-lightbox-download]")
      this.link = this.modal.querySelector("[misago-lightbox-link]")
      this.container = this.modal.querySelector("[misago-lightbox-container]")
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

    this.container
      .querySelector("[misago-lightbox-previous]")
      .addEventListener("click", () => {
        this.state.index = (this.state.index || this.state.total) - 1
        this.state.media = this.state.items[this.state.index]
        this.updateLightbox()
      })

    this.container
      .querySelector("[misago-lightbox-next]")
      .addEventListener("click", () => {
        this.state.index += 1
        if (this.state.index === this.state.total) {
          this.state.index = 0
        }

        this.state.media = this.state.items[this.state.index]
        this.updateLightbox()
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
    const items = this.getRootImages(root, image)
    const index = items.map(({ active }) => active).indexOf(true)

    return {
      items,
      media: items[index],
      index: index,
      total: items.length,
    }
  }

  getRootImages(root, image) {
    const images = []

    root.querySelectorAll("[misago-lightbox-img]").forEach((element) => {
      const context = element.closest("[misago-lightbox-context]")
      const link = element.closest("a")

      images.push({
        element,
        active: element === image,
        caption: !!context ? context.querySelector("template") : null,
        details: !!context
          ? context.getAttribute("misago-lightbox-details")
          : null,
        download: !!context
          ? context.getAttribute("misago-lightbox-download")
          : null,
        link: !context && link,
        url: !!context
          ? context.getAttribute("misago-lightbox-url")
          : element.getAttribute("src"),
      })
    })

    return images
  }

  updateLightbox() {
    this.updateLightboxPager()
    this.updateLightboxOptions()
    this.updateLightboxButtons()
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

  updateLightboxOptions() {
    const { media } = this.state

    this.updateLightboxOption(this.details, media.details)
    this.updateLightboxOption(this.download, media.download && media.url)
    this.updateLightboxOption(this.link, media.link && media.link.href)
    this.updateLightboxOption(this.zoom, media.url)
  }

  updateLightboxOption(element, value) {
    if (value) {
      element.setAttribute("href", value)
      element.classList.remove("d-none")
    } else {
      element.classList.add("d-none")
    }
  }

  updateLightboxButtons() {
    const { state, container } = this
    container.querySelectorAll("button").forEach(function (button) {
      if (state.total) {
        button.classList.remove("d-none")
      } else {
        button.classList.add("d-none")
      }
    })
  }

  updateLightboxItem() {
    const { state, container } = this
    const { media } = state

    const img = document.createElement("img")
    img.setAttribute("src", media.url)
    img.setAttribute("alt", "")
    img.setAttribute("misago-lightbox-item", "")

    container.querySelector("[misago-lightbox-item]").replaceWith(img)
  }

  updateLightboxCaption() {
    const { state, caption } = this
    const { media } = state

    if (media.caption) {
      caption.replaceChildren(media.caption.content.cloneNode(true))
    } else {
      if (media.link) {
        const a = document.createElement("a")
        const href = media.link.getAttribute("href")
        a.setAttribute("href", href)
        a.setAttribute("target", "_blank")
        a.textContent = this.cleanDisplayUrl(href)
        caption.replaceChildren(a)
      } else {
        caption.textContent = this.cleanDisplayUrl(
          media.element.getAttribute("src")
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
