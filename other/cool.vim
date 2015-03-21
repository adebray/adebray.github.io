"Syntax file for Cool programming language
"Arun Debray 2 Apr 13

if exists("b:current_syntax")
  finish
endif

"syn keyword IllegalKeywords native abstract catch do final finally for forSome implicit import lazy object package private protected requires return sealed throw trait try type val with yield
syn match ccom '--.*$' contains=celTodo
"syn match ccom '/\*[.\n]\{-}\*/' contains=celTodo
syn region ccom start='(\*' end='\*)' contains=celTodo
"backslashes are going to be weird...
"syn match str '".\{-}"' contains=strEscapeSeq
syn region str start='"' end='"' contains=strEscapeSeq
syn match strEscapeSeq '\\[btnf"\\]' contained
syn keyword celTodo contained TODO FIXME XXX todo Todo
syn keyword classes class inherits new self SELF_TYPE Bool Int String Object IO
syn keyword methods isvoid abort type_name copy out_string out_int in_string in_int length concat substr not
syn match consts '\d\+' 
syn keyword control if then else fi while loop pool let case of esac in =>
"syn match main 'main()'
syn keyword main Main main

let b:current_syntax = "cool"

hi def link celTodo Todo
hi def link ccom Comment
hi def link strEscapeSeq PreProc
hi def link str String
hi def link classes StorageClass
hi def link control Statement
hi def link typeDec Type
hi def link methods Function
hi def link consts Number
hi def link main Function
"for noe
