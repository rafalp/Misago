import { Trans } from "@lingui/macro"
import classNames from "classnames"
import React from "react"
import { Link } from "react-router-dom"
import { CategoriesContext } from "../../Context"
import * as urls from "../../urls"

interface ICategoriesNavProps {
  active?: {
    id: string
    parent: { id: string } | null
  } | null
}

const CategoriesNav: React.FC<ICategoriesNavProps> = ({ active }) => {
  const categories = React.useContext(CategoriesContext)
  const activeRootId = active?.parent?.id || active?.id
  const activeChildId = active?.id

  return (
    <div
      className="nav flex-column nav-pills"
      role="tablist"
      aria-orientation="vertical"
    >
      <Link
        aria-selected="true"
        className={classNames("nav-link", {
          active: !activeRootId,
        })}
        to="/"
      >
        <Trans id="threads.header">All threads</Trans>
      </Link>
      {categories.map((category) => (
        <React.Fragment key={category.id}>
          <Link
            aria-selected="true"
            className={classNames("nav-link", {
              active: category.id === activeRootId,
            })}
            to={urls.category(category)}
          >
            {category.name}
          </Link>
          {category.id === activeRootId &&
            category.children.map((child) => (
              <Link
                aria-selected="true"
                className={classNames("nav-link", {
                  active: child.id === activeChildId,
                })}
                key={child.id}
                to={urls.category(child)}
              >
                {child.name}
              </Link>
            ))}
        </React.Fragment>
      ))}
    </div>
  )
}

export default CategoriesNav
