export default function PageTitle({ title, subtitle }) {
  const parts = []
  if (subtitle) {
    parts.push(subtitle)
  }
  if (title) {
    parts.push(title)
  }
  parts.push(misago.get("SETTINGS").forum_name)

  document.title = parts.join(" | ")
  return null
}
