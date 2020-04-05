import { Trans } from "@lingui/macro"
import classNames from "classnames"
import React from "react"
import { Link } from "react-router-dom"
import { CategoriesContext, SettingsContext } from "../../Context"
import { IActiveCategory } from "./CategoriesNav.types"
import Category from "./Category"
import { NavItemIcon } from "./NavItem"

interface ICategoriesNavProps {
  active?: IActiveCategory | null
}

const CategoriesNav: React.FC<ICategoriesNavProps> = ({ active }) => {
  const categories = React.useContext(CategoriesContext)
  const settings = React.useContext(SettingsContext) || {
    forumIndexThreads: true,
  }
  const activeRootId = active?.parent?.id || active?.id

  return (
    <ul className="nav nav-side nav-categories flex-column">
      <li className="nav-item">
        <Link
          aria-selected="true"
          className={classNames("nav-link", { active: !activeRootId })}
          to={settings.forumIndexThreads ? "/" : "/threads/"}
        >
          <NavItemIcon isActive={!activeRootId} />
          <Trans id="threads.header">All threads</Trans>
        </Link>
      </li>
      {categories.map((category) => (
        <Category active={active} category={category} key={category.id} />
      ))}
    </ul>
  )
}

export default CategoriesNav
