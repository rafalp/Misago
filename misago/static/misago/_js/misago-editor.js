// Basic editor API
function storeCaret(ftext) {
  if (ftext.createTextRange) {
    ftext.caretPos = document.selection.createRange().duplicate();
  }
}

function SelectionRange(start, end) {
  this.start = start;
  this.end = end;
}

function getSelection(textId) {
  ctrl = document.getElementById(textId);
  if (document.selection) {
    ctrl.focus();
    var range = document.selection.createRange();
    var length = range.text.length;
    range.moveStart('character', -ctrl.value.length);
    return new SelectionRange(range.text.length - length, range.text.length);
  } else if (ctrl.selectionStart || ctrl.selectionStart == '0') {
    return new SelectionRange(ctrl.selectionStart, ctrl.selectionEnd);
  }
}

function getSelectionText(textId) {
  var ctrl = document.getElementById(textId);
  var text = ctrl.value;
  myRange = getSelection(textId);
  return $.trim(text.substring(myRange.start, myRange.end));
}

function setSelection(textId, SelectionRange) {
  ctrl = document.getElementById(textId);
  if (ctrl.setSelectionRange) {
    ctrl.focus();
    ctrl.setSelectionRange(SelectionRange.start, SelectionRange.end);
  } else if (ctrl.createTextRange) {
    var range = ctrl.createTextRange();
    range.collapse(true);
    range.moveStart('character', SelectionRange.start);
    range.moveEnd('character', SelectionRange.end);
    range.select();
  }
}

function _makeWrap(textId, myRange, wrap_start, wrap_end) {
  var ctrl = document.getElementById(textId);
  var text = ctrl.value;
  var startText = text.substring(0, myRange.start) + wrap_start;
  var middleText = text.substring(myRange.start, myRange.end);
  var endText = wrap_end + text.substring(myRange.end);
  ctrl.value = startText + middleText + endText;
  setSelection(textId, new SelectionRange(startText.length, startText.length + middleText.length));
}

function makeWrap(textId, wrap_start, wrap_end) {
  _makeWrap(textId, getSelection(textId), wrap_start, wrap_end);
}

function _makeReplace(textId, myRange, replacement) {
  var ctrl = document.getElementById(textId);
  var text = ctrl.value;
  var startText = text.substring(0, myRange.start);
  var middleText = text.substring(myRange.start, myRange.end);
  var endText = text.substring(myRange.end);
  ctrl.value = text.substring(0, myRange.start) + replacement + text.substring(myRange.end);
  setSelection(textId, new SelectionRange(startText.length + middleText.length, startText.length + middleText.length));
}

function makeReplace(textId, replacement) {
  _makeReplace(textId, getSelection(textId), replacement);
}

var url_pattern = new RegExp('^(https?:\\/\\/)?((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|((\\d{1,3}\\.){3}\\d{1,3}))(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*(\\?[;&a-z\\d%_.~+=-]*)?(\\#[-a-z\\d_]*)?$','i');
function is_url(str) {
  return url_pattern.test($.trim(str));
}

function extractor(query) {
    var result = /([^\s]+)$/.exec(query);
    if(result && result[1])
        return result[1].trim();
    return '';
}


// Enable editor
function enable_editor(name) {
  var $editor = $(name);
  var $textarea = $editor.find('textarea');
  var $upload = $editor.find('.editor-upload');

  $textarea.autosize();
  var textarea_id = $textarea.attr('id');

  $editor.find('.btn-strong').click(function() {
    makeWrap(textarea_id, '**', '**');
    return false;
  });

  $editor.find('.btn-emphasis').click(function() {
    makeWrap(textarea_id, '*', '*');
    return false;
  });
  $editor.find('.btn-bold').click(function() {
    makeWrap(textarea_id, '[b]', '[/b]');
    return false;
  });

  $editor.find('.btn-italic').click(function() {
    makeWrap(textarea_id, '[i]', '[/i]');
    return false;
  });

  $editor.find('.btn-underline').click(function() {
    makeWrap(textarea_id, '[u]', '[/u]');
    return false;
  });

  $editor.find('.btn-insert-hr').click(function() {
    makeReplace(textarea_id, '\r\n\r\n- - - - -\r\n\r\n');
    return false;
  });

  // File upload handler WIP
  $editor.find('.btn-upload-file').click(function() {
    $upload.click();
  });

  $upload.on("change", function() {
    if (this.files[0]) {
      var uploaded_file = this.files[0];

      var reader = new FileReader();
      reader.onloadend = function() {
        $editor.append('<img src="' + reader.result + '">');
      }
      reader.readAsDataURL(uploaded_file)
    }
  });
};
