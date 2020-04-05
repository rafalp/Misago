import React from "react"
import { IActiveCategory, ICategory } from "./CategoriesNav.types"
import NavItem from "./NavItem"

interface ICategoryProps {
  category: ICategory
  active?: IActiveCategory | null
}

const Category: React.FC<ICategoryProps> = ({ category, active }) => {
  const activeRootId = active?.parent?.id || active?.id
  const isActive = category.id === activeRootId
  const activeChildId = active?.id

  return (
    <React.Fragment key={category.id}>
      <NavItem
        category={category}
        isActive={isActive}
        hasChildren={category.children.length > 0}
      />
      {isActive &&
        category.children.map((child) => (
          <NavItem
            category={child}
            isActive={activeChildId === child.id}
            isChild
          />
        ))}
    </React.Fragment>
  )
}

export default Category
