import React from "react"
import * as urls from "../../../urls"
import MobileCategoryNavLink from "./MobileCategoryNavLink"

interface IMobileCategoryNavCategoryProps {
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

const MobileCategoryNavCategory: React.FC<IMobileCategoryNavCategoryProps> = ({
  category,
}) => {
  const [isOpen, setOpen] = React.useState<boolean>(false)

  return (
    <>
      <div
        className="btn-group"
        role={category.children.length > 0 ? "group" : undefined}
      >
        <MobileCategoryNavLink
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
            <MobileCategoryNavLink
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

export default MobileCategoryNavCategory
