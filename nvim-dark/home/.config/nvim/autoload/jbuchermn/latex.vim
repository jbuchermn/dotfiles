function! s:GetFileName(force_prompt, ending) abort
    if(!exists("s:FileBase") || a:force_prompt)
        call inputsave()
        let s:FileBase = input("Filename (without extensions): ")
        call inputrestore()
    endif

    return expand('%:h') . "/" . s:FileBase . "." . a:ending
endfunction

function! jbuchermn#latex#view(force_prompt) abort
    execute "silent !open -a Skim " . s:GetFileName(a:force_prompt, "pdf")
endfunction

function! jbuchermn#latex#compile(force_prompt) abort
    execute "!pdflatex " . s:GetFileName(a:force_prompt, "tex")
endfunction
