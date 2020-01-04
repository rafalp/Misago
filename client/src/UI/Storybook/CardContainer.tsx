import classNames from "classnames"
import React from "react"

interface ICardContainerProps {
  children: React.ReactNode
  padding?: boolean
}

const CardContainer: React.FC<ICardContainerProps> = ({ children, padding }) => (
  <div className="container-fluid p-0">
    <div className="card p-0 border-0 rounded-0">
      <div className={classNames("card-body", padding ? "p-4" : "p-0")}>{children}</div>
    </div>
  </div>
)

export default CardContainer
