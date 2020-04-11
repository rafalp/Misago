import React from "react"
import Header from "./Header"
import { ICategoryBanner } from "../../../types"

interface ICategoryHeaderProps {
  category: {
    name: string
    color: string | null
    banner: { full: ICategoryBanner; half: ICategoryBanner } | null
  }
}

const CategoryHeader: React.FC<ICategoryHeaderProps> = ({ category }) => (
  <Header
    banner={category.banner}
    color={category.color}
    text={category.name}
  />
)

export default CategoryHeader
