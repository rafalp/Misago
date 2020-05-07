import React from "react"
import * as urls from "../../../urls"
import { IActiveCategory } from "../Threads.types"
import ThreadsCategoriesModalLink from "./ThreadsCategoriesModalLink"

interface IThreadsCategoriesModalActiveItemProps {
  active: IActiveCategory
}

const ThreadsCategoriesModalActiveItem: React.FC<IThreadsCategoriesModalActiveItemProps> = ({
  active,
}) => {
  const { category, parent } = active

  return (
    <>
      <ThreadsCategoriesModalLink
        category={parent}
        text={parent.name}
        to={urls.category(parent)}
        isActive
      />
      {parent.children.map((child) => (
        <ThreadsCategoriesModalLink
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

export default ThreadsCategoriesModalActiveItem
