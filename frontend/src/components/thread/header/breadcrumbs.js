import React from "react"

export default function (props) {
  return (
    <div className="page-breadcrumbs">
      <div className="container">
        <ol className="breadcrumb hidden-xs">
          {props.path.map((item) => {
            return <Breadcrumb key={item.id} node={item} />
          })}
        </ol>
        <GoBack {...props} />
      </div>
    </div>
  )
}

export function Breadcrumb(props) {
  return (
    <li>
      <a href={props.node.url.index}>{props.node.name}</a>
    </li>
  )
}

export function GoBack(props) {
  const lastItem = props.path[props.path.length - 1]

  return (
    <a href={lastItem.url.index} className="go-back-sm visible-xs-block">
      <span className="material-icon">chevron_left</span>
      {lastItem.name}
    </a>
  )
}
