import { appendCSRFTokenToForm } from "../csrf"
import getRandomString from "../getRandomString"
import renderTemplate from "../renderTemplate"
import * as snackbar from "../snackbars"

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
      error: document.getElementById("attachment-upload-error-template"),
      media: document.getElementById("attachment-media-template"),
      mediaFooter: document.getElementById("attachment-media-footer-template"),
      mediaFailedFooter: document.getElementById(
        "attachment-media-failed-footer-template"
      ),
      other: document.getElementById("attachment-other-template"),
      otherFailed: document.getElementById("attachment-other-failed-template"),
      otherUploaded: document.getElementById(
        "attachment-other-uploaded-template"
      ),
    }

    const attachmentsElement = element.querySelector(
      "[misago-editor-attachments]"
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
    snackbar.error(
      pgettext("markup editor upload", "You can't upload attachments")
    )
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
        this.uploadFiles(files, insert)
      }
      input.remove()
    })

    this.element.appendChild(input)
    input.click()
  }

  _getAcceptAttributeStr(accept) {
    return (this.accept[accept] || this.accept.all).join(",")
  }

  uploadFiles(files, insert) {
    const allowedFiles = []

    for (let i = 0; i < files.length; i++) {
      const file = files[i]
      if (this._isFileTypeAccepted(file)) {
        allowedFiles.push(file)
      } else {
        snackbar.error(
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

      elements[key] = this._createUploadUI(file, key)
    })

    if (insert) {
      this._insertAttachmentsInTextarea(keys, allowedFiles)
    }

    const request = new XMLHttpRequest()

    this._addOnLoadedEventListener(request, keys, elements)
    this._addOnProgressEventListener(request, keys, elements)

    request.open("POST", this.uploadUrl)
    request.send(data)

    return { keys, files: allowedFiles }
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

  _insertAttachmentsInTextarea(keys, files) {
    const markup = []

    for (let i = 0; i < keys.length; i++) {
      const key = keys[i]
      const file = files[i]
      markup.push("<attachment=" + file.name + ":" + key + ">")
    }

    if (markup) {
      const selection = this.editor.getSelection(this.textarea)
      selection.insert(markup.join("\n"), { whitespace: "\n\n" })
    }
  }

  _addOnLoadedEventListener(request, keys, elements) {
    request.addEventListener("loadend", () => {
      if (request.readyState === XMLHttpRequest.DONE) {
        if (request.status === 200) {
          this._handleUploadSuccess(request, keys, elements)
        } else {
          this._handleUploadError(request, keys)
        }

        keys.forEach((key) => (elements[key] = null))
      }
    })
  }

  _handleUploadSuccess(request, keys, elements) {
    try {
      const { attachments, errors } = JSON.parse(request.response)

      this._replaceTextareaPlaceholders(this.textarea, keys, attachments)

      if (errors) {
        const helpText = this.element.querySelector(
          "[misago-editor-attachments-help]"
        )
        keys.forEach((key) => {
          const error = errors[key]
          if (error) {
            this._updateUploadUIWithError(key, helpText, error)
          }
        })
      }

      if (attachments) {
        attachments.forEach((attachment) => {
          try {
            this._updateUploadUI(attachment, elements[attachment.key])
            this._createAttachmentIDField(attachment)
          } catch (error) {
            console.error(error)
          }
        })
      }
    } catch (error) {
      snackbar.error(
        pgettext("markup editor upload", "Unexpected upload API response")
      )
      console.error(error)
    }
  }

  _handleUploadError(request, keys) {
    if (request.status === 0) {
      snackbar.error(
        pgettext("markup editor upload", "Site could not be reached")
      )
    } else if (request.status >= 400 && request.status < 500) {
      try {
        snackbar.error(JSON.parse(request.response).error)
      } catch (error) {
        snackbar.error(
          pgettext(
            "markup editor upload",
            "Unexpected upload API error response"
          )
        )
        console.error(error)
      }
    } else {
      snackbar.error(
        pgettext("markup editor upload", "Unexpected error during upload")
      )
    }

    keys.forEach((key) => {
      this._updateUploadUIWithError(key)
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

  _replaceTextareaPlaceholders(textarea, keys, attachments) {
    const results = {}
    keys.forEach((key) => (results[key] = null))
    if (attachments) {
      attachments.forEach(
        (attachment) => (results[attachment.key] = attachment)
      )
    }

    const selection = this.editor.getSelection(textarea)
    selection.replaceAttachments(function ({ id: key }) {
      const attachment = results[key]
      if (attachment) {
        return "<attachment=" + attachment.name + ":" + attachment.id + ">"
      } else if (attachment === null) {
        return ""
      }
    })
  }

  _createUploadUI(file, key) {
    const data = {
      key,
      file,
      name: file.name,
      isImage: false,
      isVideo: false,
    }

    if (this._isFileTypeImage(file)) {
      data.isImage = true
      this._createMediaUploadUI(data)
    } else if (this._isFileTypeVideo(file)) {
      data.isVideo = true
      this._createMediaUploadUI(data)
    } else {
      this._createOtherUploadUI(data)
    }

    return this.editor.getAttachmentByKey(key)
  }

  _createMediaUploadUI(data) {
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

  _createOtherUploadUI(data) {
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

  _updateUploadUI(attachment, element) {
    if (attachment.filetype["is_media"]) {
      this._updateMediaUploadUI(attachment, element)
    } else {
      this._updateOtherUploadUI(attachment, element)
    }
  }

  _updateMediaUploadUI(attachment, element) {
    const footer = renderTemplate(this.templates.mediaFooter, attachment)

    footer
      .querySelector("[misago-editor-attachment]")
      .setAttribute(
        "misago-editor-attachment",
        attachment.name + ":" + attachment.id
      )

    element.querySelector("[misago-tpl-footer]").replaceWith(footer)
  }

  _updateOtherUploadUI(attachment, element) {
    const item = renderTemplate(this.templates.otherUploaded, attachment)

    item
      .querySelector("[misago-editor-attachment]")
      .setAttribute(
        "misago-editor-attachment",
        attachment.name + ":" + attachment.id
      )

    element.replaceWith(item)
  }

  _updateUploadUIWithError(key, helpText, error) {
    if (error) {
      this._createErrorMessage(key, error, helpText)
    }

    const attachment = this.editor.getAttachmentByKey(key)
    const footer = attachment.querySelector("[misago-tpl-footer]")
    if (footer) {
      // Media attachment
      const template = renderTemplate(this.templates.mediaFailedFooter, { key })
      footer.replaceWith(template)
    } else {
      // Other attachment
      const upload = attachment.querySelector("[misago-tpl-upload]")
      const button = upload.closest("li").querySelector("button")

      button.setAttribute("misago-editor-action", "attachment-error-dismiss")
      button.setAttribute("misago-editor-attachment-key", key)
      button.removeAttribute("disabled")

      upload.replaceWith(renderTemplate(this.templates.otherFailed))
    }
  }

  _createErrorMessage(key, error, insertAfter) {
    const errorTemplate = renderTemplate(this.templates.error, { key, error })
    insertAfter.after(errorTemplate)
  }
}
