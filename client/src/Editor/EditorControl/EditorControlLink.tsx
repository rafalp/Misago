import React from "react"
import { EditorControlProps } from "./EditorControl.types"
import EditorControlButton from "./EditorControlButton"
import EditorControlLinkModal from "./EditorControlLinkModal"

const EditorControlLink: React.FC<EditorControlProps> = ({
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
      <EditorControlLinkModal
        context={context}
        isOpen={isOpen}
        close={() => setOpen(false)}
      />
    </>
  )
}

export default EditorControlLink
