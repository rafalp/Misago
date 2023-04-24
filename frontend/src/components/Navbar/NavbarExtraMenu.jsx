import React from "react"

export default function NavbarExtraMenu({ items }) {
  return (
    <ul className="navbar-extra-menu" role="nav">
      {items.map((item, index) => (
        <li key={index} className={item.className}>
          <a
            href={item.url}
            target={item.targetBlank ? "_blank" : null}
            rel={item.rel}
          >
            {item.title}
          </a>
        </li>
      ))}
    </ul>
  )
}
