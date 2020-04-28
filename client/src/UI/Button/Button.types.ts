export interface IButtonProps {
  block?: boolean
  className?: string | null
  disabled?: boolean
  elementRef?: React.MutableRefObject<HTMLButtonElement | null>
  icon?: string
  iconSolid?: boolean
  image?: React.ReactNode
  loading?: boolean
  small?: boolean
  text?: React.ReactNode
  outline?: boolean
  onClick?: () => void
}
