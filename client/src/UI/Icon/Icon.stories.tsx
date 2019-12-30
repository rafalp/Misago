import { faCommentAlt as faRegular } from '@fortawesome/free-regular-svg-icons'
import { faCommentAlt as faSolid } from '@fortawesome/free-solid-svg-icons'
import React from "react"
import { Icon } from ".."
 
export default {
  title: "UI/Icon",
}

export const Regular = () => <Icon icon={faRegular} />

export const Solid = () => <Icon icon={faSolid} />
