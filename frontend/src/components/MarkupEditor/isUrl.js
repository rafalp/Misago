const URL_PATTERN = new RegExp("^(((ftps?)|(https?))://)", "i")

export default function isUrl(str) {
  return URL_PATTERN.test(str.trim())
}
