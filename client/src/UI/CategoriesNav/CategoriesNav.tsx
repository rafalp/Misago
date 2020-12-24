import { Trans } from "@lingui/macro"
import React from "react"
import { useCategoriesContext, useSettingsContext } from "../../Context"
import * as urls from "../../urls"
import CategoryIcon from "../CategoryIcon"
import { SideNav, SideNavItem } from "../SideNav"
import { ActiveCategory } from "./CategoriesNav.types"
import CategoriesNavItem from "./CategoriesNavItem"

interface CategoriesNavProps {
  active?: ActiveCategory | null
}

const CategoriesNav: React.FC<CategoriesNavProps> = ({ active }) => {
  const categories = useCategoriesContext()
  const settings = useSettingsContext()

  return (
    <SideNav className="categories-nav">
      <SideNavItem
        icon={<CategoryIcon className="nav-link-icon" />}
        to={settings.forumIndexThreads ? urls.index() : urls.threads()}
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

export default React.memo(CategoriesNav)
