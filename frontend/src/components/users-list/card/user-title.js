import React from "react"

export default function ({ rank, title }) {
  let userTitle = title || rank.title || rank.name

  let className = "user-title"
  if (rank.css_class) {
    className += " user-title-" + rank.css_class
  }

  if (rank.is_tab) {
    return (
      <a className={className} href={rank.url}>
        {userTitle}
      </a>
    )
  }

  return <span className={className}>{userTitle}</span>
}
