import React from "react"
import { Card, CardBody, CardColorBand } from "../../../UI"

interface IHeaderProps {
  color?: string | null
  text: React.ReactNode
}

const Header: React.FC<IHeaderProps> = ({ color, text }) => (
  <Card>
    {color && <CardColorBand color={color} />}
    <CardBody>
      <h1 className="m-0">{text}</h1>
    </CardBody>
  </Card>
)

export default Header
