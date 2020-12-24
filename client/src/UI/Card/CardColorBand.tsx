import classnames from "classnames"
import React from "react"

interface CardColorBandProps {
  className?: string | null
  color: string
}

const CardColorBand: React.FC<CardColorBandProps> = ({ className, color }) => (
  <div
    className={classnames("card-color-band", className)}
    style={{ background: color }}
  />
)

export default CardColorBand
