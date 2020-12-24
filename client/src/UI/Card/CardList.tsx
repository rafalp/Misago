import React from "react"

interface CardListProps {
  children: React.ReactNode
}

const CardList: React.FC<CardListProps> = ({ children }) => (
  <ul className="list-group list-group-flush">{children}</ul>
)

export default CardList
