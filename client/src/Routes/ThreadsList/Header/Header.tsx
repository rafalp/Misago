import React from "react"
import { Card } from "../../../UI"

interface IHeaderProps {
  text: React.ReactNode
}

const Header: React.FC<IHeaderProps> = ({ text }) => <Card>{text}</Card>

export default Header
