import React from "react"
import { SettingsContext } from "../../Context"

interface IWindowTitleProps {
  title?: string | null
}

const WindowTitle: React.FC<IWindowTitleProps> = ({ title }) => {
  const settings = React.useContext(SettingsContext)
  if (!settings) return null
  
  if (title) {
    document.title = `${title} | ${settings.forumName}`
  } else {
    document.title = settings.forumName
  }

  return null  // never render itself
}

export default WindowTitle