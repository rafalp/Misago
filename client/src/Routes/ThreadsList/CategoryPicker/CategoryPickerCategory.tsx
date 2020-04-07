import React from "react"
import * as urls from "../../../urls"
import CategoryPickerItem from "./CategoryPickerItem"

interface ICategoryPickerCategoryProps {
  category: {
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
}

const CategoryPickerCategory: React.FC<ICategoryPickerCategoryProps> = ({
  category,
}) => {
  const [isOpen, setOpen] = React.useState<boolean>(false)

  return (
    <>
      <div
        className="btn-group"
        role={category.children.length > 0 ? "group" : undefined}
      >
        <CategoryPickerItem
          category={category}
          text={category.name}
          to={urls.category(category)}
          hasChildren={category.children.length > 0}
          isOpen={isOpen}
          toggle={() => setOpen((state) => !state)}
        />
      </div>
      {category.children.length > 0 && isOpen && (
        <>
          {category.children.map((child) => (
            <CategoryPickerItem
              category={child}
              key={child.id}
              text={child.name}
              to={urls.category(child)}
              isChild
            />
          ))}
        </>
      )}
    </>
  )
}

export default CategoryPickerCategory
