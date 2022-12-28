import React from "react"

export default function (props) {
  return (
    <div className={props.className || "loader"}>
      <div className="loader-spinning-wheel" />
    </div>
  )
}
