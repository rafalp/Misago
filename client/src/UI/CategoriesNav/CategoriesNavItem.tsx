import React from "react"
import * as urls from "../../urls"
import Icon from "../Icon"
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
  const activeRootId = active?.parent?.id || active?.id
  const isActive = category.id === activeRootId
  const activeChildId = active?.id

  return (
    <React.Fragment key={category.id}>
      <SideNavItem
        hasChildren={category.children.length > 0}
        icon={<CategoryIcon category={category} />}
        to={urls.category(category)}
        isActive={isActive}
      >
        {category.name}
      </SideNavItem>
      {isActive &&
        category.children.map((child) => (
          <SideNavItem
            icon={<CategoryIcon category={child} />}
            key={child.id}
            to={urls.category(child)}
            isActive={activeChildId === child.id}
            isChild
          >
            {child.name}
          </SideNavItem>
        ))}
    </React.Fragment>
  )
}

interface ICategoryIconProps {
  category: {
    color: string | null
    icon: string | null
  }
}

const CategoryIcon: React.FC<ICategoryIconProps> = ({ category }) => (
  <span
    className="nav-link-category-icon"
    style={category.color ? { color: category.color } : undefined}
  >
    {category.icon ? (
      <i className={category.icon + " fa-fw"} />
    ) : (
      <Icon icon="comment-alt" fixedWidth />
    )}
  </span>
)

export default CategoriesNavItem
