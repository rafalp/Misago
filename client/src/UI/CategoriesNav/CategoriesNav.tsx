import { Trans } from "@lingui/macro"
import React from "react"
import { CategoriesContext, SettingsContext } from "../../Context"
import * as urls from "../../urls"
import CategoryIcon from "../CategoryIcon"
import { SideNav, SideNavItem } from "../SideNav"
import { IActiveCategory } from "./CategoriesNav.types"
import CategoriesNavItem from "./CategoriesNavItem"

interface ICategoriesNavProps {
  active?: IActiveCategory | null
}

const CategoriesNav: React.FC<ICategoriesNavProps> = ({ active }) => {
  const categories = React.useContext(CategoriesContext)
  const settings = React.useContext(SettingsContext)

  return (
    <SideNav className="categories-nav">
      <SideNavItem
        icon={<CategoryIcon className="nav-link-icon" />}
        to={settings?.forumIndexThreads ? urls.index() : urls.threads()}
        isActive={!active}
      >
        <Trans id="threads.header">All threads</Trans>
      </SideNavItem>
      {categories.map((category) => (
        <CategoriesNavItem
          active={active}
          category={category}
          key={category.id}
        />
      ))}
    </SideNav>
  )
}

export default CategoriesNav
