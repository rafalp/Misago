import React from "react"
import { EditorControlProps } from "./EditorControl.types"
import EditorControlButton from "./EditorControlButton"
import EditorControlListModal from "./EditorControlListModal"

const EditorControlList: React.FC<EditorControlProps> = ({
  name,
  title,
  icon,
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
      <EditorControlListModal
        context={context}
        isOpen={isOpen}
        close={() => setOpen(false)}
      />
    </>
  )
}

export default EditorControlList
