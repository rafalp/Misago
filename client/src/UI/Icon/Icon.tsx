import { IconDefinition } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import React from "react"

interface IIconProps {
  icon: IconDefinition
}

const Icon: React.FC<IIconProps> = ({ icon }) => <FontAwesomeIcon icon={icon} />

export default Icon
