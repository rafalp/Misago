// Basic editor functions
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

// Nice editor functionality
$(function() {
  $('.editor-tools').fadeIn(600);
  
  function get_textarea(obj) {
      return $(obj).parent().parent().parent().parent().find('textarea');
  }
  
  $('.editor-bold').click(function() {
      ta = get_textarea(this).attr('id');
      makeWrap(ta, '**', '**');
      return false;
  });
  
  $('.editor-emphasis').click(function() {
      ta = get_textarea(this).attr('id');
      makeWrap(ta, '_', '_');
      return false;
  });
  
  $('.editor-link').click(function() {
      ta = get_textarea(this).attr('id');
      var link_url = $.trim(prompt(ed_lang_enter_link_url));
      if (link_url.length > 0) {
          var link_label = $.trim(prompt(ed_lang_enter_link_label));
          if (link_label.length > 0) {
              makeReplace(ta, '[' + link_label + '](' + link_url + ')');
          } else {
              makeReplace(ta, '<' + link_url + '>');
          }
      }
      return false;
  });
  
  $('.editor-image').click(function() {
      ta = get_textarea(this).attr('id');
      var image_url = $.trim(prompt(ed_lang_enter_image_url));
      if (image_url.length > 0) {
          var image_label = $.trim(prompt(ed_lang_enter_image_label));
          if (image_label.length > 0) {
              makeReplace(ta, '![' + image_label + '](' + image_url + ')');
          }
      }
      return false;
  });
  
  $('.editor-hr').click(function() {
      ta = get_textarea(this).attr('id');
      makeReplace(ta, '- - - - -');
      return false;
  });
});
