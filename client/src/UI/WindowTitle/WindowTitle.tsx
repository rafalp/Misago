import React from "react"
import { SettingsContext } from "../../Context"

interface IWindowTitleProps {
  index?: boolean
  title?: string | null
}

const WindowTitle: React.FC<IWindowTitleProps> = ({ index, title }) => {
  const settings = React.useContext(SettingsContext)
  if (!settings) return null
  
  if (index && settings.forumIndexTitle) {
    document.title = settings.forumIndexTitle
  } else if (title) {
    document.title = `${title} | ${settings.forumName}`
  } else {
    document.title = settings.forumName
  }

  return null  // never render itself
}

export default WindowTitle