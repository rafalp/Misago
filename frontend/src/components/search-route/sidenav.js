import React from "react"
import { Link } from "react-router"

export default function (props) {
  return (
    <div className="list-group nav-side">
      {props.providers.map((provider) => {
        return (
          <Link
            activeClassName="active"
            className="list-group-item"
            key={provider.id}
            to={provider.url}
          >
            <span className="material-icon">{provider.icon}</span>
            {provider.name}
            <Badge results={provider.results} />
          </Link>
        )
      })}
    </div>
  )
}

export function Badge(props) {
  if (!props.results) return null

  let count = props.results.count
  if (count > 1000000) {
    count = Math.ceil(count / 1000000) + "KK"
  } else if (count > 1000) {
    count = Math.ceil(count / 1000) + "K"
  }

  return <span className="badge">{count}</span>
}
