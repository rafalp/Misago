import React from "react"

interface ICardListProps {
  children: React.ReactNode
}

const CardList: React.FC<ICardListProps> = ({ children }) => (
  <ul className="list-group list-group-flush">{children}</ul>
)

export default CardList
