import classnames from "classnames"
import React from "react"

export default function SiteNav({ dropdown, overlay }) {
  const settings = misago.get("SETTINGS")
  const extraItems = misago.get("extraMenuItems")
  const categories = misago.get("categoriesMap")

  return (
    <ul
      className={classnames("site-nav-menu", {
        "dropdown-menu-list": dropdown,
        "overlay-menu-list": overlay,
      })}
    >
      <li className="dropdown-subheader">{settings.forum_name}</li>
      <li className="dropdown-menu-item">
        <a href="#">Click me!</a>
      </li>
      {extraItems.map((item, index) => (
        <li
          key={index}
          className={classnames("dropdown-menu-item", item.className)}
        >
          <a
            href={item.url}
            target={item.targetBlank ? "_blank" : null}
            rel={item.rel}
          >
            {item.title}
          </a>
        </li>
      ))}
      <li className="divider"></li>
      <li className="dropdown-subheader">{pgettext("nav section", "Users")}</li>
      <li className="divider"></li>
      <li className="dropdown-subheader">
        {pgettext("nav section", "Categories")}
      </li>
      {categories.map((category) => (
        <li className="dropdown-menu-item" key={category.id}>
          <a href={category.url}>{category.name}</a>
        </li>
      ))}
    </ul>
  )
}
