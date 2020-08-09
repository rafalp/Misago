import React from "react"
import Button from "./Button"
import { IButtonProps } from "./Button.types"

const ButtonPrimary: React.FC<IButtonProps> = (props) => (
  <Button className={"btn-primary"} {...props} />
)

const ButtonSecondary: React.FC<IButtonProps> = (props) => (
  <Button className={"btn-secondary"} {...props} />
)

const ButtonSuccess: React.FC<IButtonProps> = (props) => (
  <Button className={"btn-success"} {...props} />
)

const ButtonWarning: React.FC<IButtonProps> = (props) => (
  <Button className={"btn-warning"} {...props} />
)

const ButtonDanger: React.FC<IButtonProps> = (props) => (
  <Button className={"btn-danger"} {...props} />
)

const ButtonDark: React.FC<IButtonProps> = (props) => (
  <Button className={"btn-dark"} {...props} />
)

const ButtonLink: React.FC<IButtonProps> = (props) => (
  <Button className={"btn-link"} {...props} />
)

const ButtonOutlinePrimary: React.FC<IButtonProps> = (props) => (
  <Button className={"btn-outline-primary"} {...props} />
)

const ButtonOutlineSecondary: React.FC<IButtonProps> = (props) => (
  <Button className={"btn-outline-secondary"} {...props} />
)

const ButtonOutlineSuccess: React.FC<IButtonProps> = (props) => (
  <Button className={"btn-outline-success"} {...props} />
)

const ButtonOutlineWarning: React.FC<IButtonProps> = (props) => (
  <Button className={"btn-outline-warning"} {...props} />
)

const ButtonOutlineDanger: React.FC<IButtonProps> = (props) => (
  <Button className={"btn-outline-danger"} {...props} />
)

export {
  ButtonPrimary,
  ButtonDanger,
  ButtonDark,
  ButtonLink,
  ButtonSecondary,
  ButtonSuccess,
  ButtonWarning,
  ButtonOutlinePrimary,
  ButtonOutlineSecondary,
  ButtonOutlineSuccess,
  ButtonOutlineWarning,
  ButtonOutlineDanger,
}
