import React from "react"

interface PageTitleProps {
  text: React.ReactNode
}

const PageTitle: React.FC<PageTitleProps> = ({ text }) => (
  <h1 className="page-title">{text}</h1>
)

export default PageTitle
