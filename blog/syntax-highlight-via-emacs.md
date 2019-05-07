---
created: 2019-05-07
title: 基于 Emacs 的语法高亮
tags: [emacs, syntax highlight]
---

给 HTML 中代码块添加语法高亮的工具很多，比如非常流行的 [Pygments](http://pygments.org/) 和 [highlight.js](https://highlightjs.org/)，但它们大多不支持 Emacs Lisp 或者效果不好，我暂时没有能力折腾它们，所以尝试用 Emacs 来添加代码高亮。

## 不得不提的 [htmlize](https://github.com/hniksic/emacs-htmlize)

Htmlize 把 Emacs Buffer 的内容和样子一块导出到 HTML，效果非常逼真。但我对它的代码不熟悉，没有认真考虑过用它实现。

## 开始高亮

在 Emacs Lisp Mode 中加入这样一段代码：

```emacs-lisp
(setq foo "Hello")
```

Emacs 加上语法高亮后，也就是加上 [(elisp) Text Properties](https://www.gnu.org/software/emacs/manual/html_node/elisp/Text-Properties.html) 后，`buffer-string` 会得到：


    #("(setq foo \"Hello\")" 0 1
      (fontified t)
      1 5
      (fontified t face font-lock-keyword-face)
      5 10
      (fontified t)
      10 16
      (fontified t face font-lock-string-face)
      16 17
      (fontified t face font-lock-string-face)
      17 18
      (fontified t))

把 `face` 属性翻译成 HTML Class：

```html
<pre>(<span class="font-lock-keyword-face">setq</span> foo <span class="font-lock-string-face">"Hello"</span>)
</pre>
```

最后我用 <kbd>C-u C-x</kbd> 一一找出 `font-lock-*-face` 的颜色（相信可以自动找出，但我懒得折腾了），写成 CSS 就大功告成了。

```css
/* 图形界面 Emacs 默认配色 */
.font-lock-builtin-face {color: #483d8b;}
.font-lock-comment-delimiter-face {color: #b22222;}
.font-lock-comment-face {color: #b22222;}
.font-lock-constant-face {color: #008b8b;}
.font-lock-doc-face {color: #8b2252;}
.font-lock-function-name-face {color: blue;}
.font-lock-keyword-face {color: purple;}
.font-lock-preprocessor-face {color: #483d8b;}
.font-lock-string-face {color: #8b2252;}
.font-lock-type-face {color: #228b22;}
.font-lock-variable-name-face {color: #A0522D;}
.font-lock-warning-face {color: red;}
```

## 一些问题

### Emacs Lisp 代码高亮不完整

比如宏 `when-let` 如果 Emacs 没有加载 `subr-x.el` 就不会有高亮。
