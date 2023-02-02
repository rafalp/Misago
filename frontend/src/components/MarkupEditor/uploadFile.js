import moment from "moment"
import misago from "../../"
import ajax from "../../services/ajax"
import snackbar from "../../services/snackbar"

const ID_LEN = 32

const uploadFile = (file, setState) => {
  let upload = {
    id: null,
    key: getRandomString(ID_LEN),
    error: null,
    uploaded_on: null,
    progress: 0,
    filename: file.name,
    filetype: null,
    is_image: false,
    size: 0,
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
          refreshState()
        } else {
          snackbar.apiError(rejection)
        }
      }
    )
}

const ALPHA = "12345678990abcdefghijklmnopqrstuvwxyz"
const ALPHA_LEN = ALPHA.length

const getRandomString = (len) => {
  const chars = []
  for (let i = 0; i < len; i++) {
    const index = Math.floor(Math.random() * ALPHA_LEN)
    chars.push(ALPHA[index])
  }
  return chars.join("")
}

export default uploadFile
