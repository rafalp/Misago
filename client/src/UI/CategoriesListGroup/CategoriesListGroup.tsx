import React from "react"

interface ICategoriesListGroupProps {
  children: React.ReactNode
}

const CategoriesListGroup: React.FC<ICategoriesListGroupProps> = ({
  children,
}) => <ul className="categories-list-group">{children}</ul>

export default CategoriesListGroup
