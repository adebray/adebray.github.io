(* Determines if OCaml is currently on the frontpage of Hacker News.
 * I apologize if the following code is inefficient, unidiomatic, or confusing;
 * I knew literally nothing about this language save its name before this afternoon.
 *
 * Compile as:
 * ocamlopt str.cmxa unix.cmxa isOCamlMentionedOnHN.ml -o isOCamlMentionedOnHN
 *
 * Arun Debray, September 5, 2013
 *)

let contains s1 s2 = 
	let re = Str.regexp_string s2 in
		try ignore (Str.search_forward re s1 0); true
		with Not_found -> false

let load_file f =
	let ic = open_in f in
	let n = in_channel_length ic in
	let s = String.create n in
	really_input ic s 0 n;
	close_in ic;
	(s)

let isOCamlMentioned source =
	let t1 = contains source "OCaml"
	and t2 = contains source "Ocaml"
	and t3 = contains source "ocaml"
	and t4 = contains source "Objective Caml" in
	let result = t1 || t2 || t3 || t4 in
		result

(* This is far from the most straightforward way to implement wget, but I want to do the following:
 *	1. Implement everything in pure OCaml, so that it's easier to get running, and
 *	2. Get it working quickly, especially given my... limited understanding of this language.
 *)
let getHTMLSource url =
	ignore (let syscall = "curl \"" ^ url ^ "\" &> temp" in
		Unix.system syscall);
	let s = load_file "temp" in
	ignore (let syscall = "rm temp" in
		Unix.system syscall);
	(s)

let message presence = match presence with
	true -> print_endline "Yes, OCaml is on the front page of Hacker News."
  | false -> print_endline "No, OCaml isn't on the front page of Hacker News."

let main () =
	let source = getHTMLSource "https://news.ycombinator.com/" in
		message (isOCamlMentioned source);;

main ()
