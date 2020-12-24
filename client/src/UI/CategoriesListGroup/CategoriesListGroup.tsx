import React from "react"

interface CategoriesListGroupProps {
  children: React.ReactNode
}

const CategoriesListGroup: React.FC<CategoriesListGroupProps> = ({
  children,
}) => <ul className="categories-list-group">{children}</ul>

export default CategoriesListGroup
