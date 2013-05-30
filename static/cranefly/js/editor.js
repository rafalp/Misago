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
    makeWrap(ta, '*', '*');
    return false;
  });
  
  $('.editor-link').click(function() {
    ta = get_textarea(this).attr('id');
    var link_url = $.trim(prompt(ed_lang_enter_link_url));
    if (link_url.length > 0) {
      link_url = link_url.toLowerCase();
      var pattern = /^(("[\w-+\s]+")|([\w-+]+(?:\.[\w-+]+)*)|("[\w-+\s]+")([\w-+]+(?:\.[\w-+]+)*))(@((?:[\w-+]+\.)*\w[\w-+]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][\d]\.|1[\d]{2}\.|[\d]{1,2}\.))((25[0-5]|2[0-4][\d]|1[\d]{2}|[\d]{1,2})\.){2}(25[0-5]|2[0-4][\d]|1[\d]{2}|[\d]{1,2})\]?$)/i;
      if (!pattern.test(link_url)) {
        if (link_url.indexOf("http://") != 0 && link_url.indexOf("https://") != 0 && link_url.indexOf("ftp://") != 0) {
          link_url = "http://" + link_url;
        }
      }
      var link_label = $.trim(prompt(ed_lang_enter_link_label, $.trim(getSelectionText(get_textarea(this).attr('id')))));
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
    var image_url = $.trim(prompt(ed_lang_enter_image_url, $.trim(getSelectionText(get_textarea(this).attr('id')))));
    if (image_url.length > 0) {
      var image_label = $.trim(prompt(ed_lang_enter_image_label));
      if (image_label.length > 0) {
        makeReplace(ta, '![' + image_label + '](' + image_url + ')');
      } else {
        makeReplace(ta, '!(' + image_url + ')');
      }
    }
    return false;
  });
  
  $('.editor-hr').click(function() {
    ta = get_textarea(this).attr('id');
    makeReplace(ta, '\r\n\r\n- - - - -\r\n\r\n');
    return false;
  });
});
