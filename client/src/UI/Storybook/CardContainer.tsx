import classnames from "classnames"
import React from "react"

interface CardContainerProps {
  children: React.ReactNode
  center?: boolean
  nopadding?: boolean
}

const CardContainer: React.FC<CardContainerProps> = ({
  children,
  center,
  nopadding,
}) => (
  <div className="container-fluid p-0">
    <div className="card p-0 border-0 rounded-0">
      <div
        className={classnames(
          "card-body",
          { "d-flex justify-content-center": center },
          nopadding ? "p-0" : "p-4"
        )}
      >
        {children}
      </div>
    </div>
  </div>
)

export default CardContainer
