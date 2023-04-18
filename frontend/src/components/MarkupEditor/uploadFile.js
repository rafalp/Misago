import moment from "moment"
import misago from "../../"
import ajax from "../../services/ajax"
import snackbar from "../../services/snackbar"
import formatFilesize from "../../utils/file-size"
import getRandomString from "../../utils/getRandomString"

const ID_LEN = 32

const uploadFile = (file, setState) => {
  const maxSize = misago.get("user").acl.max_attachment_size * 1024

  if (file.size > maxSize) {
    snackbar.error(
      interpolate(
        pgettext(
          "markup editor",
          "File %(filename)s is bigger than %(limit)s."
        ),
        { filename: file.name, limit: formatFilesize(maxSize) },
        true
      )
    )

    return
  }

  let upload = {
    id: null,
    key: getRandomString(ID_LEN),
    error: null,
    uploaded_on: null,
    progress: 0,
    filename: file.name,
    filetype: null,
    is_image: false,
    size: file.size,
    url: null,
    uploader_name: null,
  }

  setState(({ attachments }) => {
    return { attachments: [upload].concat(attachments) }
  })

  const refreshState = () => {
    setState(({ attachments }) => {
      return { attachments: attachments.concat() }
    })
  }

  const data = new FormData()
  data.append("upload", file)

  ajax
    .upload(misago.get("ATTACHMENTS_API"), data, (progress) => {
      upload.progress = progress
      refreshState()
    })
    .then(
      (data) => {
        Object.assign(upload, data, { uploaded_on: moment(data.uploaded_on) })
        refreshState()
      },
      (rejection) => {
        if (rejection.status === 400 || rejection.status === 413) {
          upload.error = rejection.detail
          snackbar.error(rejection.detail)
          refreshState()
        } else {
          snackbar.apiError(rejection)
        }
      }
    )
}

export default uploadFile
