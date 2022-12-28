import React from "react"

export default function ({ rank, title }) {
  let userTitle = title || rank.title
  if (!userTitle && rank.is_tab) {
    userTitle = rank.name
  }

  if (!userTitle) return null

  let className = "user-title"
  if (rank.css_class) {
    className += " user-title-" + rank.css_class
  }

  if (rank.is_tab) {
    return (
      <div className={className}>
        <a href={rank.url}>{userTitle}</a>
      </div>
    )
  }

  return <div className={className}>{userTitle}</div>
}
