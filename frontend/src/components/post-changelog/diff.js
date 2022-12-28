import React from "react"

export default function (props) {
  return (
    <div className="modal-body post-changelog-diff">
      <ul className="list-unstyled">
        {props.diff.map((item, i) => {
          return <DiffItem item={item} key={i} />
        })}
      </ul>
    </div>
  )
}

export function DiffItem(props) {
  if (props.item[0] === "?") return null

  return (
    <li className={getItemClassName(props.item)}>{cleanItem(props.item)}</li>
  )
}

export function getItemClassName(item) {
  let className = "diff-item"
  if (item[0] === "-") {
    className += " diff-item-sub"
  } else if (item[0] === "+") {
    className += " diff-item-add"
  }
  return className
}

export function cleanItem(item) {
  return item.substr(2)
}
