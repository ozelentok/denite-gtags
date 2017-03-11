# denite-gtags #
denite-gtags is a denite.nvim source for GNU Global

## Requirments ##
- GNU Global
- denite.nvim

## Installation ##

For dein.vim
```vim
call dein#add('ozelentok/denite-gtags')
```

## Usage ##
denite-gtags implements the following sources for denite

- `gtags_def` - Definition of tag
- `gtags_ref` - References to tag
- `gtags_grep` - Grep search of tag
- `gtags_completion` - List all tags
- `gtags_file` - List all tags in file - (default is current file)
- `gtags_path` - List all paths in GTAGS file

## Key Mapping ##
Map commands for easier usage
```vim
nnoremap <leader>d :DeniteCursorWord gtags_def<cr>
nnoremap <leader>r :DeniteCursorWord gtags_ref<cr>
nnoremap <leader>g :DeniteCursorWord gtags_grep<cr>
nnoremap <leader>t :Denite gtags_completion<cr>
nnoremap <leader>f :Denite gtags_file<cr>
nnoremap <leader>p :Denite gtags_path<cr>
```
### Examples ###

To show tag definition, move the cursor to the tag, press `<leader>d` or execute the following command:
```vim
:DeniteCursorWord gtags_def
```

Alternatively, enter the tag as an argument
```vim
:Denite gtags_def:TAG
```
