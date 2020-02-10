import React from "react"
import { SettingsContext } from "../../Context"

interface IPageTitleProps {
  title?: string | null
}

const PageTitle: React.FC<IPageTitleProps> = ({ title }) => {
  const settings = React.useContext(SettingsContext)
  if (!settings) return null
  
  if (title) {
    document.title = `${title} | ${settings.forumName}`
  } else {
    document.title = settings.forumName
  }

  return null  // never render itself
}

export default PageTitle