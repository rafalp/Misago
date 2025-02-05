import { appendCSRFTokenToForm } from "../csrf"
import getRandomString from "../getRandomString"
import renderTemplate from "../renderTemplate"
import { error } from "../snackbars"

export default class MarkupEditorUploader {
  constructor(editor, element) {
    this.editor = editor

    this.element = element
    this.textarea = editor.getTextarea(element)

    this.lists = {
      media: element.querySelector('[misago-editor-attachments="media"]'),
      other: element.querySelector('[misago-editor-attachments="other"]'),
    }

    this.templates = {
      media: document.getElementById("attachment-media-template"),
      mediaFooter: document.getElementById("attachment-media-footer-template"),
      other: document.getElementById("attachment-other-template"),
      otherUploaded: document.getElementById(
        "attachment-other-uploaded-template"
      ),
    }

    const attachmentsElement = element.querySelector(
      '[misago-editor="attachments"]'
    )
    this.field = {
      name: element.getAttribute("misago-editor-attachments-name"),
      element: attachmentsElement,
    }

    this.accept = {
      all: this._getAcceptedExtensions(
        attachmentsElement.getAttribute("misago-editor-accept-attachments")
      ),
      image: this._getAcceptedExtensions(
        attachmentsElement.getAttribute("misago-editor-accept-image")
      ),
      video: this._getAcceptedExtensions(
        attachmentsElement.getAttribute("misago-editor-accept-video")
      ),
    }

    this.uploadUrl = this._getUploadUrl(element)
    this.canUpload = !!this.uploadUrl && !!this.accept.all
  }

  _getUploadUrl(element) {
    return element.getAttribute("misago-editor-attachments-url") || null
  }

  _getAcceptedExtensions(extensions) {
    return extensions.split(",").map((item) => item.trim())
  }

  showPermissionDeniedError() {
    error(pgettext("markup editor upload", "You can't upload attachments"))
  }

  prompt(options) {
    const accept = options ? options.accept : "all"
    const insert = options ? options.insert : false

    const input = document.createElement("input")
    input.setAttribute("type", "file")
    input.setAttribute(
      "accept",
      (this.accept[accept] || this.accept.all).join(",")
    )
    input.setAttribute("multiple", true)
    input.classList.add("d-none")

    input.addEventListener("change", (event) => {
      const files = event.target.files
      if (files.length) {
        const { keys, files: uploads } = this.uploadFiles(files, this.textarea)

        if (insert) {
          const markup = []

          for (let i = 0; i < keys.length; i++) {
            const key = keys[i]
            const upload = uploads[i]
            markup.push("<attachment=" + upload.name + ":" + key + ">")
          }

          if (markup) {
            const selection = this.editor.getSelection(this.textarea)
            selection.insert(markup.join("\n"), { whitespace: "\n\n" })
          }
        }
      }
      input.remove()
    })

    this.element.appendChild(input)
    input.click()
  }

  _getAcceptAttributeStr(accept) {
    return (this.accept[accept] || this.accept.all).join(",")
  }

  uploadFiles(files, textarea) {
    const allowedFiles = []

    for (let i = 0; i < files.length; i++) {
      const file = files[i]
      if (this._isFileTypeAccepted(file)) {
        allowedFiles.push(file)
      } else {
        error(
          pgettext(
            "markup editor upload",
            "%(name)s: uploaded file type is not allowed."
          ).replace("%(name)s", file.name)
        )
      }
    }

    if (!allowedFiles) {
      return { keys: [], files: [] }
    }

    const keys = []
    const elements = {}

    const data = new FormData()
    appendCSRFTokenToForm(data)

    allowedFiles.forEach((file) => {
      const key = getRandomString(16)
      keys.push(key)
      data.append("keys", key)
      data.append("upload", file)

      elements[key] = this._createFileUI(file, key)
    })

    const request = new XMLHttpRequest()

    this._addOnLoadEventListener(request, keys, elements)
    this._addOnProgressEventListener(request, keys, elements)

    request.open("POST", this.uploadUrl)
    request.send(data)

    return { keys, files: allowedFiles }
  }

  _addOnLoadEventListener(request, keys, elements) {
    request.addEventListener("load", () => {
      if (
        request.readyState === XMLHttpRequest.DONE &&
        request.status === 200
      ) {
        try {
          const { attachments } = JSON.parse(request.response)

          this._replaceTextareaPlaceholders(this.textarea, keys, attachments)

          if (attachments) {
            attachments.forEach((attachment) => {
              try {
                this._updateFileUI(attachment, elements[attachment.key])
                this._createAttachmentIDField(attachment)
              } catch (error) {
                console.error(error)
              }
            })
          }

          keys.forEach((key) => (elements[key] = null))
        } catch (error) {
          console.error(error)
        }
      }
    })
  }

  _addOnProgressEventListener(request, keys, elements) {
    request.upload.addEventListener("progress", (event) => {
      if (event.lengthComputable) {
        const progress = Math.ceil((event.loaded * 100) / event.total)
        for (const key of keys) {
          const progressBar = elements[key].querySelector(".progress-bar")
          progressBar.setAttribute("aria-valuenow", progress)
          progressBar.style.width = progress + "%"
        }
      }
    })
  }

  _isFileTypeAccepted(file) {
    return this._isFileTypeInList(file, this.accept.all)
  }

  _isFileTypeImage(file) {
    return this._isFileTypeInList(file, this.accept.image)
  }

  _isFileTypeVideo(file) {
    return this._isFileTypeInList(file, this.accept.video)
  }

  _isFileTypeInList(file, list) {
    const name = file.name.toLowerCase()
    for (const extension of list) {
      if (name.substring(name.length - extension.length) === extension) {
        return true
      }
    }
    return false
  }

  _replaceTextareaPlaceholders(textarea, keys, attachments) {
    const results = {}

    keys.forEach((key) => (results[key] = null))
    if (attachments) {
      attachments.forEach(
        (attachment) => (results[attachment.key] = attachment)
      )
    }

    textarea.value = textarea.value.replace(
      /<attachment=(.+?)>/gi,
      function (match, p1) {
        if (p1.match(/:/g).length !== 1) {
          return match
        }

        let value = p1.trim()
        while (value.substring(0, 1) === '"') {
          value = value.substring(1)
        }
        while (value.substring(value.length - 1) === '"') {
          value = value.substring(0, value.length - 1)
        }

        const key = value.substring(value.indexOf(":") + 1).trim()
        if (key) {
          const attachment = results[key]
          if (attachment) {
            return "<attachment=" + attachment.name + ":" + attachment.id + ">"
          } else if (attachment === null) {
            return ""
          }
        }

        return match
      }
    )
  }

  _createFileUI(file, key) {
    const data = {
      key,
      file,
      name: file.name,
      isImage: false,
      isVideo: false,
    }

    if (this._isFileTypeImage(file)) {
      data.isImage = true
      this._createMediaFileUI(data)
    } else if (this._isFileTypeVideo(file)) {
      data.isVideo = true
      this._createMediaFileUI(data)
    } else {
      this._createOtherFileUI(data)
    }

    return this.element.querySelector(
      'ul li[misago-editor-upload-key="' + key + '"]'
    )
  }

  _createMediaFileUI(data) {
    const element = renderTemplate(this.templates.media, data)

    if (data.isImage) {
      const image = element.querySelector("[misago-tpl-image]")
      const buffer = new FileReader()
      buffer.onload = () => {
        image.style.backgroundImage = "url('" + buffer.result + "')"
      }
      buffer.readAsDataURL(data.file)
    } else if (data.isVideo) {
      const video = element.querySelector("video")
      const buffer = new FileReader()
      buffer.onload = () => {
        const source = document.createElement("source")
        source.setAttribute("src", buffer.result)
        source.setAttribute("type", data.file.type)

        video.append(source)
      }
      buffer.readAsDataURL(data.file)
    }

    this._addUIToAttachmentsList(this.lists.media, element)
  }

  _createOtherFileUI(data) {
    const element = renderTemplate(this.templates.other, data)
    this._addUIToAttachmentsList(this.lists.other, element)
  }

  _addUIToAttachmentsList(list, element) {
    list.querySelector("ul").prepend(element)
    list.classList.remove("d-none")
  }

  _createAttachmentIDField(attachment) {
    const input = document.createElement("input")
    input.setAttribute("type", "hidden")
    input.setAttribute("name", this.field.name)
    input.setAttribute("value", attachment.id)
    this.field.element.appendChild(input)
  }

  _updateFileUI(attachment, element) {
    if (attachment.filetype["is_media"]) {
      this._updateMediaFileUI(attachment, element)
    } else {
      this._updateOtherFileUI(attachment, element)
    }
  }

  _updateMediaFileUI(attachment, element) {
    const footer = renderTemplate(this.templates.mediaFooter, attachment)

    footer
      .querySelector("[misago-editor-attachment]")
      .setAttribute(
        "misago-editor-attachment",
        attachment.name + ":" + attachment.id
      )

    element.querySelector("[misago-tpl-footer]").replaceWith(footer)
  }

  _updateOtherFileUI(attachment, element) {
    const item = renderTemplate(this.templates.otherUploaded, attachment)

    item
      .querySelector("[misago-editor-attachment]")
      .setAttribute(
        "misago-editor-attachment",
        attachment.name + ":" + attachment.id
      )

    element.replaceWith(item)
  }
}
