;;; $DOOMDIR/config.el -*- lexical-binding: t; -*-

;; Place your private configuration here! Remember, you do not need to run 'doom
;; sync' after modifying this file!


;; Some functionality uses this to identify you, e.g. GPG configuration, email
;; clients, file templates and snippets.
(setq user-full-name "Jonas Bucher"
      user-mail-address "j.bucher.mn@gmail.com")

;; Doom exposes five (optional) variables for controlling fonts in Doom. Here
;; are the three important ones:
;;
;; + `doom-font'
;; + `doom-variable-pitch-font'
;; + `doom-big-font' -- used for `doom-big-font-mode'; use this for
;;   presentations or streaming.
;;
;; They all accept either a font-spec, font string ("Input Mono-12"), or xlfd
;; font string. You generally only need these two:
(setq doom-font (font-spec :family "Source Code Pro for Powerline" :size 11)
      doom-variable-pitch-font (font-spec :family "sans" :size 11))
(after! doom-themes
  (setq doom-themes-enable-bold t)
  (setq doom-themes-enable-italic t))
(custom-set-faces!
  '(font-lock-comment-face :slant italic)
  '(font-lock-keyword-face :slant italic))

;; There are two ways to load a theme. Both assume the theme is installed and
;; available. You can either set `doom-theme' or manually load a theme with the
;; `load-theme' function. This is the default:
(setq doom-theme 'doom-one)

;; If you use `org' and don't want your org files in the default location below,
;; change `org-directory'. It must be set before org loads!
(setq org-directory "~/org/")

;; This determines the style of line numbers in effect. If set to `nil', line
;; numbers are disabled. For relative line numbers, set this to `relative'.
(setq display-line-numbers-type t)


;; Here are some additional functions/macros that could help you configure Doom:
;;
;; - `load!' for loading external *.el files relative to this one
;; - `use-package!' for configuring packages
;; - `after!' for running code after a package has loaded
;; - `add-load-path!' for adding directories to the `load-path', relative to
;;   this file. Emacs searches the `load-path' when you load packages with
;;   `require' or `use-package'.
;; - `map!' for binding new keys
;;
;; To get information about any of these functions/macros, move the cursor over
;; the highlighted symbol at press 'K' (non-evil users must press 'C-c c k').
;; This will open documentation for it, including demos of how they are used.
;;
;; You can also try 'gd' (or 'C-c c d') to jump to their definition and see how
;; they are implemented.



;; Restore sensible s/S
(after! evil-snipe (evil-snipe-mode -1))

;; Restore sensible word detection
(defun my-restore-sensible-words ()
  (modify-syntax-entry ?_ "w"))
(dolist (hook '(python-mode-hook c-mode-hook js-mode-hook))
  (add-hook hook 'my-restore-sensible-words))


;; Activate centered-cursor-mode by default
;; (define-global-minor-mode my-global-ccm-mode centered-cursor-mode
;;   (lambda ()
;;     (when (not (memq major-mode
;;                      (list 'Info-mode 'term-mode 'eshell-mode 'shell-mode 'erc-mode)))
;;       (centered-cursor-mode)
;;       )))
;; (my-global-ccm-mode 1)
;; (setq ccm-recenter-at-end-of-file t)
(setq scroll-margin 15)

;; Enable breadcrumbs per default
(use-package! lsp-mode
  :custom
  (lsp-headerline-breadcrumb-enable t))

;; Disable LSP file watchers as they love node_modules and similar
(setq lsp-enable-file-watchers nil)

;; Open treemacs-symbols
(map! :leader
      :desc "Treemacs symbols"
      "c S" #'lsp-treemacs-symbols)

;; Comments on SPC c c
(map! :leader
      :desc "Comment"
      "c c" #'comment-line)

;; Indentation using arrow keys
(evil-define-key 'normal 'global
  (kbd "<left>") 'evil-shift-left-line)
(evil-define-key 'normal 'global
  (kbd "<right>") 'evil-shift-right-line)
(evil-define-key 'visual 'global
  (kbd "<left>") 'evil-shift-left)
(evil-define-key 'visual 'global
  (kbd "<right>") 'evil-shift-right)

;; Mouse fix
(setq mouse-wheel-progressive-speed nil)

;; Flycheck
(setq flycheck-relevant-error-other-file-show nil)

;; Select mypy checker for all python files as default
(load! "lisp/flycheck-mypy")
(defun my-py-flycheck-setup ()
  (flycheck-select-checker 'python-mypy))
(add-hook 'python-mode-local-vars-hook #'my-py-flycheck-setup)

;; mu4e at ~/mail
(setq +mu4e-backend 'offlineimap)
;; Each path is relative to the path of the maildir you passed to mu
(set-email-account! "j.bucher.mn@gmail.com"
  '((mu4e-sent-folder       . "/[Google Mail].Gesendet")
    (mu4e-drafts-folder     . "/[Google Mail].Entw&APw-rfe")
    (mu4e-trash-folder      . "/[Google Mail].Papierkorb")
    (mu4e-refile-folder     . "/[Google Mail].Alle Nachrichten")
    (smtpmail-smtp-user     . "j.bucher@gmail.com")
    (mu4e-compose-signature . ""))
  t)
(setq +mu4e-gmail-accounts '(("j.bucher.mn@gmail.com" . "/")))
(setq mu4e-index-cleanup nil
      mu4e-index-lazy-check t)
