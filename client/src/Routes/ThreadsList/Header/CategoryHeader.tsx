import React from "react"
import Header from "./Header"

interface ICategoryHeaderProps {
  category: {
    name: string
    color: string | null
  }
}

const CategoryHeader: React.FC<ICategoryHeaderProps> = ({ category }) => (
  <Header color={category.color} text={category.name} />
)

export default CategoryHeader
