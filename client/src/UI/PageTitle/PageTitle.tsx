import React from "react"

interface IPageTitleProps {
  text: React.ReactNode
}

const PageTitle: React.FC<IPageTitleProps> = ({ text }) => (
  <h1 className="page-title">{text}</h1>
)

export default PageTitle
