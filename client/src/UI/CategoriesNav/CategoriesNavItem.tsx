import React from "react"
import * as urls from "../../urls"
import CategoryIcon from "../CategoryIcon"
import { SideNavItem } from "../SideNav"
import { IActiveCategory, ICategory } from "./CategoriesNav.types"

interface ICategoriesNavItemProps {
  category: ICategory
  active?: IActiveCategory | null
}

const CategoriesNavItem: React.FC<ICategoriesNavItemProps> = ({
  category,
  active,
}) => {
  const isActive = category.id === active?.parent.id

  return (
    <React.Fragment key={category.id}>
      <SideNavItem
        hasChildren={category.children.length > 0}
        icon={<CategoryIcon className="nav-link-icon" category={category} />}
        to={urls.category(category)}
        isActive={isActive}
      >
        {category.name}
      </SideNavItem>
      {isActive &&
        category.children.map((child) => (
          <SideNavItem
            icon={<CategoryIcon className="nav-link-icon" category={child} />}
            key={child.id}
            to={urls.category(child)}
            isActive={active?.category.id === child.id}
            isChild
          >
            {child.name}
          </SideNavItem>
        ))}
    </React.Fragment>
  )
}

export default CategoriesNavItem
