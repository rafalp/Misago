import React from "react"
import * as urls from "../../../urls"
import { IActiveCategory } from "../Threads.types"
import MobileCategoryNavLink from "./MobileCategoryNavLink"

interface IMobileCategoryNavActiveCategoryProps {
  active: IActiveCategory
}

const MobileCategoryNavActiveCategory: React.FC<IMobileCategoryNavActiveCategoryProps> = ({
  active,
}) => {
  const { category, parent } = active

  return (
    <>
      <MobileCategoryNavLink
        category={parent}
        text={parent.name}
        to={urls.category(parent)}
        isActive
      />
      {parent.children.map((child) => (
        <MobileCategoryNavLink
          category={child}
          key={child.id}
          text={child.name}
          to={urls.category(child)}
          isActive={child.id === category.id}
          isChild
        />
      ))}
    </>
  )
}

export default MobileCategoryNavActiveCategory
