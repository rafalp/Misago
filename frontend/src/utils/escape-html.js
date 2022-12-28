const map = {
  "&": "&amp;",
  "<": "&lt;",
  ">": "&gt;",
  '"': "&quot;",
  "'": "&#039;",
}

export default function (text) {
  return text.replace(/[&<>"']/g, function (m) {
    return map[m]
  })
}
