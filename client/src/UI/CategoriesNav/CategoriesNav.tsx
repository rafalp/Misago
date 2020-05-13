import { Trans } from "@lingui/macro"
import React from "react"
import { useCategoriesContext, useSettingsContext } from "../../Context"
import * as urls from "../../urls"
import CategoryIcon from "../CategoryIcon"
import { SideNav, SideNavItem } from "../SideNav"
import { IActiveCategory } from "./CategoriesNav.types"
import CategoriesNavItem from "./CategoriesNavItem"

interface ICategoriesNavProps {
  active?: IActiveCategory | null
}

const CategoriesNav: React.FC<ICategoriesNavProps> = ({ active }) => {
  const categories = useCategoriesContext()
  const settings = useSettingsContext()

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

export default React.memo(CategoriesNav)
