import React from "react"
import { EditorControlProps } from "./EditorControl.types"
import EditorControlButton from "./EditorControlButton"
import EditorControlCodeModal from "./EditorControlCodeModal"

const EditorControlCode: React.FC<EditorControlProps> = ({
  name,
  icon,
  title,
  context,
}) => {
  const { disabled } = context
  const [isOpen, setOpen] = React.useState(false)

  return (
    <>
      <EditorControlButton
        name={name}
        disabled={disabled}
        icon={icon}
        title={title}
        onClick={() => setOpen(true)}
      />
      <EditorControlCodeModal
        context={context}
        isOpen={isOpen}
        close={() => setOpen(false)}
      />
    </>
  )
}

export default EditorControlCode
