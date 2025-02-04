import { appendCSRFTokenToForm } from "../csrf"
import getRandomString from "../getRandomString"
import renderTemplate from "../renderTemplate"
import { error } from "../snackbars"

export default class MarkupEditorUploader {
  constructor(editor, element) {
    this.editor = editor

    this.element = element

    this.lists = {
      media: element.querySelector('[misago-editor-attachments="media"]'),
      other: element.querySelector('[misago-editor-attachments="other"]'),
    }

    this.templates = {
      media: document.getElementById("attachment-media-template"),
      other: document.getElementById("attachment-other-template"),
      mediaUpload: document.getElementById("attachment-media-upload-template"),
      otherUpload: document.getElementById("attachment-other-upload-template"),
    }

    const attachmentsElement = element.querySelector('[misago-editor="attachments"]')
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
    return extensions.split(",").map(item => item.trim())
  }

  showPermissionDeniedError() {
    error(
      pgettext("markup editor upload", "You can't upload attachments")
    )
  }

  uploadFiles(files) {
    const allowedFiles = []
    for (let i = 0; i < files.length; i ++) {
      const file = files[i]
      if (this._isFileTypeAccepted(file)) {
        allowedFiles.push(file)
      } else {
        error(
          pgettext(
            "markup editor upload",
            "%(name)s: uploaded file type is not allowed."
          ).replace(
            "%(name)s", file.name
          )
        )
      }
    }
    
    if (!allowedFiles) {
      return
    }

    const elements = {}
    const keys = []
    const data = new FormData()
    appendCSRFTokenToForm(data)

    allowedFiles.forEach(file => {
      const key = getRandomString(16)
      keys.push(key)
      data.append("keys", key)
      data.append("upload", file)

      this._prependAttachmentsListUploadItem(file, key)
      elements[key] = this.element.querySelector(
        'ul li[misago-editor-upload-key="' + key +'"]'
      )
    })

    const request = new XMLHttpRequest()
    
    // this._addOnLoadEventListener(request, keys, elements);
    this._addOnProgressEventListener(request, keys, elements);

    request.open("POST", this.uploadUrl);
    request.send(data)
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

  _prependAttachmentsListUploadItem(file, key) {
    const data = {
      key,
      file,
      name: file.name,
      isImage: false,
      isVideo: false,
    }

    if (this._isFileTypeImage(file)) {
      data.isImage = true
      this._prependAttachmentsListUploadMediaItem(data)
    } else if (this._isFileTypeVideo(file)) {
      data.isVideo = true
      this._prependAttachmentsListUploadMediaItem(data)
    } else {
      this._prependAttachmentsListUploadOtherItem(data)
    }
  }
  
  _prependAttachmentsListUploadMediaItem(data) {
    const element = renderTemplate(this.templates.mediaUpload, data)

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

    this._prependToAndShowList(this.lists.media, element)
  }

  _prependAttachmentsListUploadOtherItem(data) {
    const element = renderTemplate(this.templates.otherUpload, data)
    this._prependToAndShowList(this.lists.other, element)
  }

  _addOnLoadEventListener(request, keys, elements) {
    request.addEventListener("load", () => {
      if (request.readyState === XMLHttpRequest.DONE && request.status === 200) {
        try {
          const { attachments } = JSON.parse(request.response)
          if (attachments) {
            attachments.forEach(attachment => {
              try {
                this._prependAttachmentHiddenField(attachment)
                this._prependAttachmentsListItem(attachment)
              } catch(error) {
                console.error(error)
              }
            })
          }
        } catch(error) {
  
        }
      }
    });
  }

  _addOnProgressEventListener(request, keys, elements) {
    request.upload.addEventListener("progress", (event) => {
      if (event.lengthComputable) {
        const progress = Math.ceil(event.loaded * 100 / event.total)
        for (const key of keys) {
          const progressBar = elements[key].querySelector(".progress-bar")
          progressBar.setAttribute("aria-valuenow", progress)
          progressBar.style.width = progress + "%"
        }
      }
    });
  }

  _prependAttachmentHiddenField(attachment) {
    const input = document.createElement("input")
    input.setAttribute("type", "hidden")
    input.setAttribute("name", this.field.name)
    input.setAttribute("value", attachment.id)
    this.field.element.appendChild(input)
  }

  _prependAttachmentsListItem(attachment) {
    if (attachment.filetype["is_media"]) {
      this._prependAttachmentsMediaListItem(attachment)
    } else {
      this._prependAttachmentsOtherListItem(attachment)
    }
  }

  _prependAttachmentsMediaListItem(attachment) {
    const item = renderTemplate(this.templates.media, attachment)

    if (attachment.filetype["is_video"]) {
      const video = item.querySelector("video")
      if (video) {
        const source = document.createElement("source")
        source.setAttribute("src", attachment.upload.url)
        source.setAttribute("type", attachment.content_type)
        video.append(source)
      }
    } else {
      const image = item.querySelector("[misago-tpl-image]")
      const url = attachment.thumbnail ? attachment.thumbnail.url : attachment.upload.url
      image.style.backgroundImage = "url('" + url + "')"
      image.removeAttribute("misago-tpl-image")
    }

    item.querySelector("[misago-editor-attachment]").setAttribute(
      "misago-editor-attachment", attachment.name + ":" + attachment.id
    )

    this._prependToAndShowList(this.lists.media, item)
  }

  _prependAttachmentsOtherListItem(attachment) {
    const item = renderTemplate(this.templates.other, attachment)

    item.querySelector("[misago-editor-attachment]").setAttribute(
      "misago-editor-attachment", attachment.name + ":" + attachment.id
    )

    this._prependToAndShowList(this.lists.other, item)
  }

  _prependToAndShowList(list, element) {
    list.querySelector("ul").prepend(element)
    list.classList.remove("d-none")
  }
}
