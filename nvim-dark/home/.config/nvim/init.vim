
" Dein.vim {{{
if &compatible
    set nocompatible
endif
set runtimepath+=~/.cache/dein/repos/github.com/Shougo/dein.vim


if dein#load_state('~/.cache/dein')
    call dein#begin('~/.cache/dein')

    call dein#add('~/.cache/dein/repos/github.com/Shougo/dein.vim')

    " Denite
    call dein#add('Shougo/denite.nvim')
    
    " Neomake
    call dein#add('neomake/neomake')
    call dein#add('mhartington/denite-neomake')

    " Navigation
    call dein#add('tpope/vim-eunuch')
    call dein#add('tpope/vim-projectionist')
    call dein#add('scrooloose/nerdtree') 
    call dein#add('lambdalisue/lista.nvim')
    call dein#add('cloudhead/neovim-fuzzy')
    
    " Util
    call dein#add('tomtom/tcomment_vim')
    call dein#add('jiangmiao/auto-pairs')
    
    " Git
    call dein#add('tpope/vim-fugitive')
    call dein#add('airblade/vim-gitgutter')
    call dein#add('Xuyuanp/nerdtree-git-plugin')
    call dein#add('gregsexton/gitv')
    
    " Styling
    call dein#add('mhartington/oceanic-next')
    call dein#add('bling/vim-airline') 
    
    " CPP
    call dein#add('jbuchermn/rtags-nvim')
    
    " Python
    call dein#add('Vimjas/vim-python-pep8-indent')
    
    " JavaScript
    call dein#add('pangloss/vim-javascript')
    call dein#add('moll/vim-node')
    call dein#add('mxw/vim-jsx')
    
    " CSV
    call dein#add('chrisbra/csv.vim')

    " Flutter
    call dein#add('dart-lang/dart-vim-plugin')
    call dein#add('thosakwe/vim-flutter')
    call dein#add('tiagofumo/dart-vim-flutter-layout')

    call dein#end()
    call dein#save_state()
endif

" }}}

" Global {{{
language en_GB.UTF-8 " Language is ENGLISH!
set encoding=utf8
set mouse=a " Mouse scrolling
set exrc " Use local .vimrc
set so=999 " Keep cursor centered vertically
syntax enable
set number

set path=$PWD/**

" 80 is a bit too harsh..
set textwidth=120

" Fold by syntax
set foldmethod=syntax
set foldlevelstart=20

" Indentation
set autoindent
set smartindent
" set cinoptions+=:0 " Indentation of switch-case

filetype plugin indent on

" Tabs
set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab
set smarttab

set wildignore+=*/tmp/*,*.so,*.swp,*.o,*.a,*.d " Ignores
set wildmenu " Command completion
set wildmode=longest,full

" Splits
set splitbelow
set splitright

" Leader
let mapleader = " "
nnoremap <Space> <nop>

" Remember cursor position between sessions
autocmd BufReadPost *
            \ if line("'\"") > 0 && line ("'\"") <= line("$") |
            \   exe "normal! g'\"" |
            \ endif

" Use ag over grep
if executable('ag')
    set grepprg=ag\ --nogroup\ --nocolor
endif

" Save undos
set undodir=~/.config/nvim/undodir
set undofile

" }}}

" Key Mappings - Needs to be cleaned up{{{

" Easier to reach
nmap ö :
vmap ö :

" Clear highlights
nmap <silent> <ESC> :noh<CR>

" Highlight without jumping
nnoremap * *N 

" Change word under cursor and repeat with dot operator (or n. to preview)
nnoremap c* *Ncgn

" Map arrow keys
nmap <silent> <Up> :lprevious<CR>
nmap <silent> <Down> :lnext<CR>
nmap <silent> <S-Up> :cprevious<CR>
nmap <silent> <S-Down> :cnext<CR>

vmap <Up> <Nop>
vmap <Down> <Nop>

nmap <Left> <<
nmap <Right> >>
vmap <Left> <gv
vmap <Right> >gv

" Toggle comments
let g:tcomment_maps = 0
nnoremap <silent> <leader>cc :TComment<CR>
vnoremap <silent> <leader>cc :TComment<CR>
vnoremap <silent> <leader>ci :TCommentInline<CR>

" Vim-Projectionist
noremap  <silent> <leader>ph :A<CR>
noremap  <silent> <leader>pv :AV<CR>
noremap  <silent> <leader>ps :AS<CR>

" Neomake/Location list
noremap <leader>mm :Neomake<CR>
noremap <leader>md :Denite neomake<CR>
noremap <leader>mo :lopen<CR>
noremap <leader>mc :lclose<CR>

" Lista
nnoremap # :Lista<CR>
nnoremap g# :ListaCursorWord<CR>

let g:lista#custom_mappings = [ 
            \   ['<C-k>', '<lista:select_previous_candidate>', 'noremap'], 
            \   ['<C-j>', '<lista:select_next_candidate>', 'noremap']
            \ ]

" Denite
map <silent> <leader>gi :Denite -post-action=open -start-filter grep:::!<CR>
map <silent> <leader>gg :Denite -post-action=open grep<CR>

" Fuzzy Finder
nnoremap <silent> <leader>e :FuzzyOpen<CR>
nnoremap <silent> <leader>v :vnew<CR>:FuzzyOpen<CR>
nnoremap <silent> <leader>s :new<CR>:FuzzyOpen<CR>

" NERDTree
let NERDTreeShowHidden=1
nnoremap - :NERDTreeToggle<CR>
vnoremap - :NERDTreeToggle<CR>

" Frequent Typos
command! Q :q
command! WQ :wq
command! Wq :wq
command! W :w

" Window movement
nnoremap <C-j> <C-w><C-j>
nnoremap <C-k> <C-w><C-k>
nnoremap <C-l> <C-w><C-l>
nnoremap <C-h> <C-w><C-h>

" }}}

" VimScript {{{
augroup filetype_vim
    autocmd!
    autocmd FileType vim setlocal foldmethod=marker
augroup end
"  }}}

" JavaScript {{{
let g:jsx_ext_required = 0
" }}}

" Dart {{{
let g:dart_style_guide = 1
" }}}

" Neomake {{{
let g:neomake_cpp_enabled_makers = ['rtags']
let g:neomake_c_enabled_makers =  ['rtags']
let g:neomake_javascript_enabled_makers = ['eslint']
let g:neomake_python_enabled_makers = ['flake8']

function! ConfigureNeomake()
    if(&filetype == 'cpp' || &filetype == 'c')
        call neomake#configure#automake('r', 750)
    else
        call neomake#configure#automake('rnw', 750)
    endif
endfunction

augroup Neomake_Filetype
    autocmd!
    autocmd Filetype * :call ConfigureNeomake()
augroup end
" }}}

" Denite {{{

autocmd FileType denite call s:denite_my_settings()
function! s:denite_my_settings() abort
  nnoremap <silent><buffer><expr> <CR> denite#do_map('do_action')
  nnoremap <silent><buffer><expr> d denite#do_map('do_action', 'delete')
  nnoremap <silent><buffer><expr> p denite#do_map('do_action', 'preview')
  nnoremap <silent><buffer><expr> q denite#do_map('quit')
  nnoremap <silent><buffer><expr> i denite#do_map('open_filter_buffer')
  nnoremap <silent><buffer><expr> <Space> denite#do_map('toggle_select').'j'
endfunction


" Configure grep source
call denite#custom#var('grep', 'matchers', ['matcher_regexp'])
call denite#custom#var('grep', 'command', ['ag'])
call denite#custom#var('grep', 'default_opts', ['--vimgrep'])
call denite#custom#var('grep', 'recursive_opts', [])
call denite#custom#var('grep', 'pattern_opt', [])
call denite#custom#var('grep', 'separator', ['--'])
call denite#custom#var('grep', 'final_opts', [])
" }}}

" LaTeX {{{
nnoremap <leader>lc :call jbuchermn#latex#compile(0)<CR>
nnoremap <leader>lC :call jbuchermn#latex#compile(1)<CR>
nnoremap <leader>lv :call jbuchermn#latex#view(0)<CR>
nnoremap <leader>lV :call jbuchermn#latex#view(1)<CR>
" }}}

" Vim-Projectionist {{{
let g:projectionist_heuristics = {
            \     "*": {
            \         "*.cpp": { "alternate": ["{}.h"] },
            \         "*.c":   { "alternate": ["{}.h"] },
            \         "*.h":   { "alternate": ["{}.cpp", "{}.c"] }
            \     }
            \ }
" }}}

" Styling {{{
if (has("termguicolors"))
    set termguicolors
endif

colorscheme OceanicNext
let g:airline_theme='oceanicnext'
let g:airline_powerline_fonts = 1
let g:airline_section_b = ''

let g:airline#extensions#neomake#error_symbol='✖ '
let g:airline#extensions#neomake#warning_symbol='⚠️  '

" guibg matches OceanicNext
hi NeomakeErrorMsg guifg=#ff0000 guibg=#343d46
hi NeomakeWarningMsg guifg=#ffff00 guibg=#343d46
let g:neomake_error_sign = {'text': '•', 'texthl': 'NeomakeErrorMsg'}
let g:neomake_warning_sign = {'text': '•', 'texthl': 'NeomakeWarningMsg'}

hi CursorLineNR guifg=#ffffff

" Focus by Wincent
augroup WincentFocus
    autocmd!
    autocmd BufEnter,FocusGained,VimEnter,WinEnter * call wincent#focus_window()
    autocmd FocusLost,WinLeave * call wincent#blur_window()
augroup end

" Always display signcolumn
augroup SignColumn
    autocmd!
    autocmd BufRead,BufNewFile * setlocal signcolumn=yes
    autocmd FileType nerdtree,nvimbols setlocal signcolumn=no
augroup end

" Make textwidth visible
let &colorcolumn=&textwidth+1

" Folding by wincent
set fillchars=vert:┃    " BOX DRAWINGS HEAVY VERTICAL (U+2503, UTF-8: E2 94 83)
set fillchars+=fold:·   " MIDDLE DOT (U+00B7, UTF-8: C2 B7)
set foldtext=wincent#foldtext()


let s:arrow='↪ '
let &showbreak = s:arrow 

" }}}

