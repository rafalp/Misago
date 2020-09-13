import React from "react"

interface ICategoriesListGroupItemProps {
  children: React.ReactNode
}

const CategoriesListGroupItem: React.FC<ICategoriesListGroupItemProps> = ({
  children,
}) => <li className="categories-list-group-item">{children}</li>

export default CategoriesListGroupItem
