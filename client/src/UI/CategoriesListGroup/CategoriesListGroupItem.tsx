import React from "react"

interface CategoriesListGroupItemProps {
  children: React.ReactNode
}

const CategoriesListGroupItem: React.FC<CategoriesListGroupItemProps> = ({
  children,
}) => <li className="categories-list-group-item">{children}</li>

export default CategoriesListGroupItem
