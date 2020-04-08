import React from "react"
import { CategoriesContext } from "../../../Context"
import * as urls from "../../../urls"
import MobileCategoryNavLink from "./MobileCategoryNavLink"

interface IMobileCategoryNavActiveCategoryProps {
  active: string
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

const MobileCategoryNavActiveCategory: React.FC<IMobileCategoryNavActiveCategoryProps> = ({
  active,
}) => {
  const categories = React.useContext(CategoriesContext)
  const [category, setState] = React.useState<IActiveCategory>()

  React.useEffect(() => {
    categories.forEach((parent) => {
      if (parent.id === active && parent.children.length) {
        setState(parent)
      } else {
        parent.children.forEach((child) => {
          if (child.id === active) {
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
      <MobileCategoryNavLink
        category={category}
        text={category.name}
        to={urls.category(category)}
        isActive={category.id === active}
      />
      {category.children.map((child) => (
        <MobileCategoryNavLink
          category={child}
          key={child.id}
          text={child.name}
          to={urls.category(child)}
          isActive={child.id === active}
          isChild
        />
      ))}
      <hr />
    </>
  )
}

export default MobileCategoryNavActiveCategory
