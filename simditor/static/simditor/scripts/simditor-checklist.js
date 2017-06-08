(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD. Register as an anonymous module unless amdModuleId is set
    define('simditor-checklist', ["jquery","simditor"], function (a0,b1) {
      return (root['ChecklistButton'] = factory(a0,b1));
    });
  } else if (typeof exports === 'object') {
    // Node. Does not work with strict CommonJS, but
    // only CommonJS-like environments that support module.exports,
    // like Node.
    module.exports = factory(require("jquery"),require("simditor"));
  } else {
    root['ChecklistButton'] = factory(jQuery,Simditor);
  }
}(this, function ($, Simditor) {

var ChecklistButton,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty,
  slice = [].slice;

ChecklistButton = (function(superClass) {
  extend(ChecklistButton, superClass);

  ChecklistButton.prototype.type = 'ul.simditor-checklist';

  ChecklistButton.prototype.name = 'checklist';

  ChecklistButton.prototype.icon = 'checklist';

  ChecklistButton.prototype.htmlTag = 'li';

  ChecklistButton.prototype.disableTag = 'pre, table';

  function ChecklistButton() {
    var args;
    args = 1 <= arguments.length ? slice.call(arguments, 0) : [];
    ChecklistButton.__super__.constructor.apply(this, args);
    if ('input' && $.inArray('input', this.editor.formatter._allowedTags) < 0) {
      this.editor.formatter._allowedTags.push('input');
    }
    $.extend(this.editor.formatter._allowedAttributes, {
      input: ['type', 'checked']
    });
  }

  ChecklistButton.prototype._init = function() {
    ChecklistButton.__super__._init.call(this);
    this.editor.on('decorate', (function(_this) {
      return function(e, $el) {
        return $el.find('ul > li input[type=checkbox]').each(function(i, checkbox) {
          return _this._decorate($(checkbox));
        });
      };
    })(this));
    this.editor.on('undecorate', (function(_this) {
      return function(e, $el) {
        return $el.find('.simditor-checklist > li').each(function(i, node) {
          return _this._undecorate($(node));
        });
      };
    })(this));
    this.editor.body.on('click', '.simditor-checklist > li', (function(_this) {
      return function(e) {
        var $node, range;
        e.preventDefault();
        e.stopPropagation();
        $node = $(e.currentTarget);
        range = document.createRange();
        _this.editor.selection.save();
        range.setStart($node[0], 0);
        range.setEnd($node[0], _this.editor.util.getNodeLength($node[0]));
        _this.editor.selection.range(range);
        document.execCommand('strikethrough');
        $node.attr('checked', !$node.attr('checked'));
        _this.editor.selection.restore();
        return _this.editor.trigger('valuechanged');
      };
    })(this));
    return this.editor.keystroke.add('13', 'li', (function(_this) {
      return function(e, $node) {
        return setTimeout(function() {
          var $li;
          $li = _this.editor.selection.blockNodes().last().next();
          if ($li.length) {
            $li[0].removeAttribute('checked');
            if (document.queryCommandState('strikethrough')) {
              return document.execCommand('strikethrough');
            }
          }
        }, 0);
      };
    })(this));
  };

  ChecklistButton.prototype._status = function() {
    var $node;
    ChecklistButton.__super__._status.call(this);
    $node = this.editor.selection.rootNodes();
    if ($node.is('.simditor-checklist')) {
      this.editor.toolbar.findButton('ul').setActive(false);
      this.editor.toolbar.findButton('ol').setActive(false);
      this.editor.toolbar.findButton('ul').setDisabled(true);
      return this.editor.toolbar.findButton('ol').setDisabled(true);
    } else {
      return this.editor.toolbar.findButton('checklist').setActive(false);
    }
  };

  ChecklistButton.prototype.command = function(param) {
    var $list, $rootNodes;
    $rootNodes = this.editor.selection.blockNodes();
    this.editor.selection.save();
    $list = null;
    $rootNodes.each((function(_this) {
      return function(i, node) {
        var $node;
        $node = $(node);
        if ($node.is('blockquote, li') || $node.is(_this.disableTag) || !$.contains(document, node)) {
          return;
        }
        if ($node.is('.simditor-checklist')) {
          $node.children('li').each(function(i, li) {
            var $childList, $li;
            $li = $(li);
            $childList = $li.children('ul, ol').insertAfter($node);
            return $('<p/>').append($(li).html() || _this.editor.util.phBr).insertBefore($node);
          });
          return $node.remove();
        } else if ($node.is('ul, ol')) {
          return $('<ul class="simditor-checklist" />').append($node.contents()).replaceAll($node);
        } else if ($list && $node.prev().is($list)) {
          $('<li/>').append($node.html() || _this.editor.util.phBr).appendTo($list);
          return $node.remove();
        } else {
          $list = $('<ul class="simditor-checklist"><li></li></ul>');
          $list.find('li').append($node.html() || _this.editor.util.phBr);
          return $list.replaceAll($node);
        }
      };
    })(this));
    this.editor.selection.restore();
    return this.editor.trigger('valuechanged');
  };

  ChecklistButton.prototype._decorate = function($checkbox) {
    var $node, checked;
    checked = !!$checkbox.attr('checked');
    $node = $checkbox.closest('li');
    $checkbox.remove();
    $node.attr('checked', checked);
    return $node.closest('ul').addClass('simditor-checklist');
  };

  ChecklistButton.prototype._undecorate = function($node) {
    var $checkbox, checked;
    checked = !!$node.attr('checked');
    $checkbox = $('<input type="checkbox">').attr('checked', checked);
    return $node.attr('checked', '').prepend($checkbox);
  };

  return ChecklistButton;

})(Simditor.Button);

Simditor.Toolbar.addButton(ChecklistButton);

return ChecklistButton;

}));