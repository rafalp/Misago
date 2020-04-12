import React from "react"
import Header from "./Header"
import { ICategoryBanner } from "../../../types"

interface IHeaderCategoryProps {
  category: {
    name: string
    color: string | null
    banner: { full: ICategoryBanner; half: ICategoryBanner } | null
  }
}

const HeaderCategory: React.FC<IHeaderCategoryProps> = ({ category }) => (
  <Header
    banner={category.banner}
    color={category.color}
    text={category.name}
  />
)

export default HeaderCategory
