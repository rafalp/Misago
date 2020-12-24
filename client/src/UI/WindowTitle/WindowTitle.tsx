import React from "react"
import { useSettingsContext } from "../../Context"

interface WindowTitleProps {
  alerts?: number
  index?: boolean
  title?: string | null
  parent?: string | null
}

const WindowTitle: React.FC<WindowTitleProps> = ({
  alerts,
  index,
  title,
  parent,
}) => {
  const settings = useSettingsContext()
  if (!settings) return null

  const prefix = alerts ? `(${alerts}) ` : ""

  if (index) {
    const indexTitle = settings.forumIndexTitle || settings.forumName
    document.title = prefix + indexTitle
  } else if (title) {
    if (parent) {
      document.title = `${prefix}${title} | ${parent} | ${settings.forumName}`
    } else {
      document.title = `${prefix}${title} | ${settings.forumName}`
    }
  } else {
    document.title = prefix + settings.forumName
  }

  return null // never render itself
}

export default WindowTitle
