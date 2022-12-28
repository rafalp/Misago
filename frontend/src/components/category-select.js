import React from "react"

export default function (props) {
  return (
    <select
      className={props.className || "form-control"}
      disabled={props.disabled || false}
      id={props.id || null}
      onChange={props.onChange}
      value={props.value}
    >
      {props.choices.map((item) => {
        return (
          <option
            disabled={item.disabled || false}
            key={item.value}
            value={item.value}
          >
            {"- - ".repeat(item.level) + item.label}
          </option>
        )
      })}
    </select>
  )
}
