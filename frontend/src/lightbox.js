import { updateTimestamps } from "./timestamps"

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
    this.template = null

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

      this.template = document.getElementById("lightbox-image-caption")

      this._registerEvents()
    }
  }

  _registerEvents() {
    document.addEventListener("click", (event) => {
      const image = event.target.closest("img[misago-lightbox-media]")
      if (!!image) {
        this.onImageClick(event, image)
      } else {
        const button = event.target.closest("[misago-lightbox-button]")
        if (!!button) {
          this.onMediaButtonClick(event, button)
        }
      }
    })

    this.modal.querySelector("[data-dismiss]").addEventListener("click", () => {
      this.onHideLightbox()
    })

    this.modal
      .querySelector("[misago-lightbox-previous]")
      .addEventListener("click", () => {
        this.state.index = (this.state.index || this.state.total) - 1
        this.state.media = this.state.items[this.state.index]
        this.updateLightbox()
      })

    this.modal
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

  onMediaButtonClick(event, button) {
    event.preventDefault()

    const root = button.closest("[misago-lightbox-root]")
    const media = button
      .closest("[misago-lightbox-context]")
      .querySelector("[misago-lightbox-media]")
    this.state = this.getInitialState(root, media)

    this.updateLightbox()
    this.showLightbox()
  }

  getInitialState(root, media) {
    const items = this.getRootMedia(root, media)
    const index = items.map(({ active }) => active).indexOf(true)

    return {
      items,
      media: items[index],
      index: index,
      total: items.length,
    }
  }

  getRootMedia(root, media) {
    const items = []
    root.querySelectorAll("[misago-lightbox-media]").forEach((element) => {
      const context = element.closest("[misago-lightbox-context]")
      const link = element.closest("a")

      items.push({
        element,
        active: element === media,
        video: element.tagName === "VIDEO",
        image: element.tagName === "IMG",
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

    return items
  }

  updateLightbox() {
    this.updateLightboxPager()
    this.updateLightboxOptions()
    this.updateLightboxNav()
    this.updateLightboxContainer()
    this.updateLightboxCaption()
  }

  updateLightboxPager() {
    const { state, pager } = this
    if (state.total > 1) {
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

  updateLightboxNav() {
    const { state } = this
    this.modal
      .querySelectorAll("[misago-lightbox-previous], [misago-lightbox-next]")
      .forEach(function (button) {
        if (state.total > 1) {
          button.classList.remove("d-none")
        } else {
          button.classList.add("d-none")
        }
      })
  }

  updateLightboxContainer() {
    const { state, container } = this
    const { media } = state

    if (media.image) {
      this.updateLightboxContainerWithImage(container, media)
    } else if (media.video) {
      this.updateLightboxContainerWithVideo(container, media)
    }
  }

  updateLightboxContainerWithImage(container, media) {
    const img = document.createElement("img")
    img.setAttribute("src", media.url)
    img.setAttribute("alt", "")

    const a = document.createElement("a")
    a.setAttribute("href", media.url)
    a.setAttribute("target", "_blank")
    a.appendChild(img)

    container.replaceChildren(a)
  }

  updateLightboxContainerWithVideo(container, media) {
    const video = document.createElement("video")
    video.innerHTML = media.element.innerHTML
    video.setAttribute("controls", "true")
    video.setAttribute("preload", "metadata")
    container.replaceChildren(video)
  }

  updateLightboxCaption() {
    const { state, caption } = this
    const { media } = state

    if (media.caption) {
      const template = media.caption.content.cloneNode(true)
      updateTimestamps(template)
      caption.replaceChildren(template)
    } else {
      const template = this.template.content.cloneNode(true)
      const name = template.querySelector("[lightbox-image-caption-name]")
      const description = template.querySelector(
        "[lightbox-image-caption-description]"
      )

      name.removeAttribute("lightbox-image-caption-name")
      description.removeAttribute("lightbox-image-caption-description")

      const alt = (media.element.getAttribute("alt") || "").trim()
      const title = (media.element.getAttribute("title") || "").trim()
      const src = media.element.getAttribute("src")

      const nameText =
        title && alt
          ? title + " — " + alt
          : title || alt || this.cleanDisplayFilename(src)

      name.textContent = this.shortenLongString(nameText)
      if (name.textContent !== nameText) {
        name.setAttribute("title", nameText)
      }

      if (media.link) {
        const a = document.createElement("a")
        const href = media.link.getAttribute("href")
        a.setAttribute("href", href)
        a.setAttribute("target", "_blank")
        a.textContent = this.cleanDisplayUrl(href)
        description.appendChild(a)
      } else if (title || alt) {
        description.textContent = this.cleanDisplayUrl(src)
      } else {
        description.remove()
      }

      caption.replaceChildren(template)
    }
  }

  cleanDisplayFilename(href) {
    const slash = href.lastIndexOf("/")
    if (slash === -1) {
      return this.cleanDisplayUrl(href)
    }

    const filename = href.substring(slash + 1).trim()
    if (filename) {
      return this.shortenLongString(filename)
    }

    return this.cleanDisplayUrl(href)
  }

  cleanDisplayUrl(href) {
    let clean = href
    if (clean.startsWith("https://")) {
      clean = clean.substring(8)
    } else if (clean.startsWith("http://")) {
      clean = clean.substring(7)
    }
    return this.shortenLongString(clean)
  }

  shortenLongString(value) {
    if (value.length <= 80) {
      return value
    }

    const prefix = value.substring(0, 35)
    const suffix = value.substring(value.length - 40)
    return prefix + "..." + suffix
  }

  showLightbox() {
    document.querySelectorAll("video").forEach((video) => video.pause())
    $(this.modal).modal("show")
  }

  onHideLightbox() {
    this.modal.querySelectorAll("video").forEach((video) => video.pause())
  }
}
