import React from "react"
import Button from "./Button"
import { ButtonProps } from "./Button.types"

const ButtonPrimary: React.FC<ButtonProps> = (props) => (
  <Button className={"btn-primary"} {...props} />
)

const ButtonSecondary: React.FC<ButtonProps> = (props) => (
  <Button className={"btn-secondary"} {...props} />
)

const ButtonSuccess: React.FC<ButtonProps> = (props) => (
  <Button className={"btn-success"} {...props} />
)

const ButtonWarning: React.FC<ButtonProps> = (props) => (
  <Button className={"btn-warning"} {...props} />
)

const ButtonDanger: React.FC<ButtonProps> = (props) => (
  <Button className={"btn-danger"} {...props} />
)

const ButtonInverse: React.FC<ButtonProps> = (props) => (
  <Button className={"btn-dark"} {...props} />
)

const ButtonLink: React.FC<ButtonProps> = (props) => (
  <Button className={"btn-link"} {...props} />
)

const ButtonOutlinePrimary: React.FC<ButtonProps> = (props) => (
  <Button className={"btn-outline-primary"} {...props} />
)

const ButtonOutlineSecondary: React.FC<ButtonProps> = (props) => (
  <Button className={"btn-outline-secondary"} {...props} />
)

const ButtonOutlineSuccess: React.FC<ButtonProps> = (props) => (
  <Button className={"btn-outline-success"} {...props} />
)

const ButtonOutlineWarning: React.FC<ButtonProps> = (props) => (
  <Button className={"btn-outline-warning"} {...props} />
)

const ButtonOutlineDanger: React.FC<ButtonProps> = (props) => (
  <Button className={"btn-outline-danger"} {...props} />
)

export {
  ButtonPrimary,
  ButtonDanger,
  ButtonInverse,
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
