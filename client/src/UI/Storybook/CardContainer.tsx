import classNames from "classnames"
import React from "react"

interface ICardContainerProps {
  children: React.ReactNode
  center?: boolean
  padding?: boolean
}

const CardContainer: React.FC<ICardContainerProps> = ({
  children,
  center,
  padding,
}) => (
  <div className="container-fluid p-0">
    <div className="card p-0 border-0 rounded-0">
      <div
        className={classNames(
          "card-body",
          { "d-flex justify-content-center": center },
          padding ? "p-4" : "p-0"
        )}
      >
        {children}
      </div>
    </div>
  </div>
)

export default CardContainer
