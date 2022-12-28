import React from "react"
import Card from "./card"

export default function ({ colClassName, cols }) {
  const list = Array.apply(null, { length: cols }).map(Number.call, Number)

  return (
    <div className="users-cards-list ui-preview">
      <div className="row">
        {list.map((i) => {
          let className = colClassName
          if (i !== 0) className += " hidden-xs"
          if (i === 3) className += " hidden-sm"

          return (
            <div className={className} key={i}>
              <Card />
            </div>
          )
        })}
      </div>
    </div>
  )
}
