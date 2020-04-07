import React from "react"
import { CategoriesContext } from "../../../Context"
import * as urls from "../../../urls"
import CategoryPickerItem from "./CategoryPickerItem"

interface ICategoryPickerActiveItemProps {
  active: { id: string }
}

interface IActiveCategory {
  id: string
  name: string
  slug: string
  icon: string | null
  color: string | null
  children: Array<{
    id: string
    name: string
    slug: string
    icon: string | null
    color: string | null
  }>
}

const CategoryPickerActiveItem: React.FC<ICategoryPickerActiveItemProps> = ({
  active,
}) => {
  const categories = React.useContext(CategoriesContext)
  const [category, setState] = React.useState<IActiveCategory>()

  React.useEffect(() => {
    categories.forEach((parent) => {
      if (parent.id === active.id && parent.children.length) {
        setState(parent)
      } else {
        parent.children.forEach((child) => {
          if (child.id === active.id) {
            setState(parent)
          }
        })
      }
    })
  }, [active, categories])

  if (!category) return null

  return (
    <>
      <hr />
      <CategoryPickerItem
        category={category}
        text={category.name}
        to={urls.category(category)}
        isActive={category.id === active.id}
      />
      {category.children.map((child) => (
        <CategoryPickerItem
          category={child}
          key={child.id}
          text={child.name}
          to={urls.category(child)}
          isActive={child.id === active.id}
          isChild
        />
      ))}
      <hr />
    </>
  )
}

export default CategoryPickerActiveItem
