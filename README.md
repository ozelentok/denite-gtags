# denite-gtags #
denite-gtags is a denite.nvim source for GNU Global

## Requirements ##
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
- `gtags_context` - Definition/References to tag (based on current tag context)
- `gtags_grep` - Grep search of tag
- `gtags_completion` - List all tags
- `gtags_file` - List all tags in file - (default is current file)
- `gtags_files` - List all tags under current directory
- `gtags_path` - List all paths in GTAGS file

## Key Mapping ##
Map commands for easier usage
```vim
nnoremap <leader>a :DeniteCursorWord -buffer-name=gtags_context gtags_context<cr>
nnoremap <leader>d :DeniteCursorWord -buffer-name=gtags_def gtags_def<cr>
nnoremap <leader>r :DeniteCursorWord -buffer-name=gtags_ref gtags_ref<cr>
nnoremap <leader>g :DeniteCursorWord -buffer-name=gtags_grep gtags_grep<cr>
nnoremap <leader>t :Denite -buffer-name=gtags_completion gtags_completion<cr>
nnoremap <leader>f :Denite -buffer-name=gtags_file gtags_file<cr>
nnoremap <leader>F :Denite -buffer-name=gtags_files gtags_files<cr>
nnoremap <leader>p :Denite -buffer-name=gtags_path gtags_path<cr>
```

## Dynamic Configuration ##
To set `GTAGSROOT` and `GTAGSDBPATH` dynamically, set the following variables per buffer
```vim
let b:denite_gtags_root='/path/to/project'
let b:denite_gtags_db_path='/path/to/gtags-db'
```

### Examples ###

To jump to a tag definition, move the cursor to the tag, press `<leader>d` or execute the following command:
```vim
:DeniteCursorWord gtags_def
```

Alternatively, enter the tag as an argument
```vim
:Denite gtags_def:TAG
```
