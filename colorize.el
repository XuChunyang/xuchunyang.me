;;; colorize.el --- Export code into HTML with syntax highlighting  -*- lexical-binding: t; -*-

;; Copyright (C) 2019  Xu Chunyang

;; Author: Xu Chunyang <mail@xuchunyang.me>
;; Keywords: hypermedia

;; This program is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation, either version 3 of the License, or
;; (at your option) any later version.

;; This program is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.

;; You should have received a copy of the GNU General Public License
;; along with this program.  If not, see <https://www.gnu.org/licenses/>.

;;; Commentary:

;;

;;; Code:

;; maybe `translate-region' is faster?
(defun colorize-escape (text)
  (mapconcat
   (lambda (char)
     (pcase char
       (?& "&amp;")
       (?< "&lt;")
       (?> "&gt;")
       (_ (string char))))
   text ""))

(defun colorize-1 (end)
  (let ((s (buffer-substring-no-properties (point) end)))
    (setq s (colorize-escape s))
    (let* ((props (get-text-property (point) 'face))
           (prop (if (listp props) (car props) props)))
      (cond
       ((null props) s)
       ((plist-get props :background)
        (format "<span style=\"background-color: %s\">%s</span>"
                (plist-get props :background) s))
       (t
        (unless (eq (face-attribute prop :inherit) 'unspecified)
          (setq prop (face-attribute prop :inherit)))
        (format "<span class=\"%s\">%s</span>" prop s))))))

(defun colorize ()
  "Colorize the current buffer."
  (goto-char (point-min))
  (let (np (result ""))
    (while (setq np (next-property-change (point)))
      (setq result (concat result (colorize-1 np)))
      (goto-char np))
    (when (< (point) (point-max))
      (setq result (concat result (colorize-1 (point-max)))))
    (format "<pre>%s</pre>" result)))

;; The command line interface:
;; $ cat colorize.el | emacs -Q --batch -l colorize.el --lang emacs-lisp > index.html
;; $ echo '<link rel="stylesheet" href="font-lock.css">' >> index.html
;; $ open index.html
(when noninteractive
  (pcase argv
    (`("--lang" ,lang)
     (setq argv nil)
     ;; the message is annoying
     (setq python-indent-guess-indent-offset nil)
     (setq code (with-temp-buffer
                  (insert-file-contents "/dev/stdin")
                  (delay-mode-hooks
                    (funcall (intern-soft (format "%s-mode" lang))))
                  (let ((noninteractive nil))
                    (font-lock-mode)
                    (font-lock-ensure))
                  (princ (colorize)))))
    (_
     (message "Usage: --lang <lang>")
     (kill-emacs 1))))

(provide 'colorize)
;;; colorize.el ends here
