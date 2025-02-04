import { appendCSRFTokenToForm } from "../csrf"
import getRandomString from "../getRandomString"
import { error } from "../snackbars"

export default class MarkupEditorUploader {
  constructor(editor, element) {
    this.editor = editor

    this.element = element

    this.uploadUrl = this._getUploadUrl(element)
    this.canUpload = !!this.uploadUrl

    this.lists = {
      media: element.querySelector('[misago-editor-attachments="media"]'),
      other: element.querySelector('[misago-editor-attachments="other"]'),
    }

    this.templates = {
      media: document.getElementById("attachment-media-template"),
      other: document.getElementById("attachment-other-template"),
    }

    this.field = {
      name: element.getAttribute("misago-editor-attachments-name"),
      element: element.querySelector('[misago-editor="attachments"]'),
    }
  }

  _getUploadUrl(element) {
    return element.getAttribute("misago-editor-attachments-url") || null
  }

  showPermissionDeniedError() {
    error(
      pgettext("markup editor", "You can't upload attachments")
    )
  }

  uploadFiles(files) {
    const request = new XMLHttpRequest()
    
    this._addOnLoadEventListener(request);
    this._addOnProgressEventListener(request);

    const keys = []
    
    const data = new FormData()
    appendCSRFTokenToForm(data)

    for (let i = 0; i < files.length; i ++) {
      const key = getRandomString(16)
      keys.push(key)
      data.append("keys", key)
      data.append("upload", files[i])
    }

    request.open("POST", this.uploadUrl);
    request.send(data)
  }

  _addOnLoadEventListener(request) {
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
                console.log(error)
              }
            })
          }
        } catch(error) {
  
        }
      }
    });
  }

  _addOnProgressEventListener(request) {

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
    this._prependToAndShowList(this.lists.other, item)
  }

  _prependToAndShowList(list, item) {
    list.querySelector("ul").prepend(item)
    list.classList.remove("d-none")
  }
}

function renderTemplate(template, data) {
  const node = template.content.cloneNode(true)

  node.querySelectorAll("[misago-tpl-if]").forEach(element => {
    const variable = element.getAttribute("misago-tpl-if")
    if (getVariableValue(data, variable)) {
      element.removeAttribute("misago-tpl-if")
    } else {
      element.remove()
    }
  })

  node.querySelectorAll("[misago-tpl-ifnot]").forEach(element => {
    const variable = element.getAttribute("misago-tpl-ifnot")
    if (getVariableValue(data, variable)) {
      element.remove()
    } else {
      element.removeAttribute("misago-tpl-ifnot")
    }
  })

  node.querySelectorAll("[misago-tpl-var]").forEach(element => {
    const variable = element.getAttribute("misago-tpl-var")
    element.innerText = getVariableValue(data, variable) || ""
    element.removeAttribute("misago-tpl-var")
  })

  node.querySelectorAll("[misago-tpl-attr]").forEach(element => {
    const attr = element.getAttribute("misago-tpl-attr")
    if (attr.indexOf(":") !== ":") {
      const name = attr.substring(0, attr.indexOf(":")).trim()
      const variable = attr.substring(attr.indexOf(":") + 1).trim()
      const value = variable ? getVariableValue(data, variable) : undefined

      if (name && value) {
        element.setAttribute(name, value)
      }
    }
    element.removeAttribute("misago-tpl-attr")
  })

  return node
}

function getVariableValue(data, variable) {
  if (variable.indexOf(".") === -1) {
    return data[variable]
  } else {
    let value = data
    for (const part of variable.split(".")) {
      if (part && typeof value[part] !== "undefined") {
        value = value[part]
      } else {
        return undefined
      }
    }
    return value
  }
}