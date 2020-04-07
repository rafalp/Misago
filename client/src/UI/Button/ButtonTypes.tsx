import React from "react"
import Button from "./Button"
import { ButtonType, IBaseButtonProps } from "./Button.types"

const ButtonSecondary: React.FC<IBaseButtonProps> = (props) => (
  <Button type={ButtonType.SECONDARY} {...props} />
)

const ButtonSuccess: React.FC<IBaseButtonProps> = (props) => (
  <Button type={ButtonType.SUCCESS} {...props} />
)

const ButtonWarning: React.FC<IBaseButtonProps> = (props) => (
  <Button type={ButtonType.WARNING} {...props} />
)

const ButtonDanger: React.FC<IBaseButtonProps> = (props) => (
  <Button type={ButtonType.DANGER} {...props} />
)

const ButtonLink: React.FC<IBaseButtonProps> = (props) => (
  <Button type={ButtonType.LINK} {...props} />
)

export {
  ButtonDanger,
  ButtonLink,
  ButtonSecondary,
  ButtonSuccess,
  ButtonWarning,
}
