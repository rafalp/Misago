import React from "react"
import Header from "./Header"

interface ICategoryHeaderProps {
  category: {
    name: string
  }
}

const CategoryHeader: React.FC<ICategoryHeaderProps> = ({ category }) => (
  <Header text={category.name} />
)

export default CategoryHeader
