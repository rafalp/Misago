import editor from "./editor"

export default editor

export function activateEditors() {
  document
    .querySelectorAll("[misago-editor-active='false']")
    .forEach(editor.activate)
}
