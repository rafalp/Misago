import classnames from "classnames"
import React from "react"

interface ICardColorBand {
  className?: string | null
  color: string
}

const CardColorBand: React.FC<ICardColorBand> = ({ className, color }) => (
  <div
    className={classnames("card-color-band", className)}
    style={{ background: color }}
  />
)

export default CardColorBand
