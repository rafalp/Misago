import React from "react"
import Icon from "../Icon"

interface ITibitIconProps {
  icon: string
  solid?: boolean
}

const TidbitIcon: React.FC<ITibitIconProps> = ({ icon, solid }) => (
  <span className="tidbit-icon">
    <Icon icon={icon} solid={solid} fixedWidth />
  </span>
)

export default TidbitIcon
