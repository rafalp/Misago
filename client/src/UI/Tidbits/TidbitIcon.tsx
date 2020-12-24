import React from "react"
import Icon from "../Icon"

interface TibitIconProps {
  icon: string
}

const TidbitIcon: React.FC<TibitIconProps> = ({ icon }) => (
  <span className="tidbit-icon">
    <Icon icon={icon} fixedWidth />
  </span>
)

export default TidbitIcon
