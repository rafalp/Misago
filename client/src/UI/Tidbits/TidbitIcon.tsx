import React from "react"
import Icon from "../Icon"

interface ITibitIconProps {
  icon: string
}

const TidbitIcon: React.FC<ITibitIconProps> = ({ icon }) => (
  <span className="tidbit-icon">
    <Icon icon={icon} fixedWidth />
  </span>
)

export default TidbitIcon
