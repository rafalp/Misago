export enum ButtonType {
  PRIMARY = "primary",
  SECONDARY = "secondary",
  SUCCESS = "success",
  WARNING = "warning",
  DANGER = "danger",
  LINK = "link",
}

export interface IBaseButtonProps {
  block?: boolean
  className?: string | null
  disabled?: boolean
  elementRef?: React.MutableRefObject<HTMLButtonElement | null>
  icon?: string
  iconSolid?: boolean
  image?: React.ReactNode
  loading?: boolean
  text?: React.ReactNode
  outline?: boolean
  onClick?: () => void
}

export interface IButtonProps extends IBaseButtonProps {
  type?: ButtonType
}
