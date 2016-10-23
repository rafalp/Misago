export const textareaId = 'editor-textarea';

export function getTextarea() {
  return document.getElementById(textareaId);
}

export function getValue() {
  return document.getElementById(textareaId).value;
}

export function getSelectionRange(start, end) {
  return {
    start,
    end
  };
}

export function getSelection() {
  const ctrl = getTextarea();
  if (document.selection) {
    ctrl.focus();
    const range = document.selection.createRange();
    const length = range.text.length;
    range.moveStart('character', -ctrl.value.length);
    return getSelectionRange(range.text.length - length, range.text.length);
  } else if (ctrl.selectionStart || ctrl.selectionStart == '0') {
    return getSelectionRange(ctrl.selectionStart, ctrl.selectionEnd);
  }
}

export function getSelectionText() {
  const range = getSelection();
  return $.trim(getValue().substring(range.start, range.end));
}


export function setSelection(selectionRange) {
  const ctrl = getTextarea();
  if (ctrl.setSelectionRange) {
    ctrl.focus();
    ctrl.setSelectionRange(selectionRange.start, selectionRange.end);
  } else if (ctrl.createTextRange) {
    const range = ctrl.createTextRange();
    range.collapse(true);
    range.moveStart('character', selectionRange.start);
    range.moveEnd('character', selectionRange.end);
    range.select();
  }
}

export function _replace(myRange, replacement) {
  const ctrl = getTextarea();
  const text = ctrl.value;
  const startText = text.substring(0, myRange.start);
  ctrl.value = text.substring(0, myRange.start) + replacement + text.substring(myRange.end);
  setSelection(getSelectionRange(startText.length + replacement.length, startText.length + replacement.length));
  return ctrl.value;
}

export function replace(replacement) {
  return _replace(getSelection(), replacement);
}
