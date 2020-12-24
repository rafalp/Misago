import React from "react"

interface PlaceholderProps {
  text: string
}

const Placeholder: React.FC<PlaceholderProps> = ({ text }) => (
  <div
    style={{
      color: "#8993a4",
      border: "3px dashed #b3bac5",
      padding: "5rem 0px",
      textAlign: "center",
    }}
  >
    {text}
  </div>
)

export default Placeholder
