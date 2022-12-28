import React from "react"

export default function ({ html, text, url }) {
  if (html) {
    return (
      <div
        className="form-control-static col-md-9"
        dangerouslySetInnerHTML={{ __html: html }}
      />
    )
  }

  return (
    <div className="form-control-static col-md-9">
      <SafeValue text={text} url={url} />
    </div>
  )
}

export function SafeValue({ text, url }) {
  if (url) {
    return (
      <p>
        <a href={url} target="_blank" rel="nofollow">
          {text || url}
        </a>
      </p>
    )
  }

  if (text) {
    return <p>{text}</p>
  }

  return null
}
