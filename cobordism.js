/* This code uses a modified version of the partition-number algorithm to compute the
   dimension of the F_2-vector space of unoriented coboridsm classes in a given dimension.
 */

// used for memoization
var already_computed = {}

// turns (n, cutoff) into a string, so it can be used as a key in a dict.
const to_repr = function(i, j) {
	return '' + i + ' ' + j;
}

/* Returns a set of numbers of the form 2^j - 1 (up to n), for ease of checking whether
   a generator of the cobordism ring exists in a given dimension
 */
const not_generators = function(n) {
	let no_gens = new Set();
	for(let j = 0; j < 1 + Math.log2(n+1); j++) {
		no_gens.add(Math.pow(2, j) - 1);
	}
	return no_gens;
}

const partitions_specified_by = function(no_gens, n, cutoff) {
	if (n == 0) return 1;
	if (n <  0) return 0;
	const precomp = already_computed[to_repr(n, cutoff)]
	if (precomp !== undefined) return precomp;
	else {
		let result = 0;
		for(let k = 1; k <= cutoff; k++) {
			if (!no_gens.has(k)) result += partitions_specified_by(no_gens, n-k, k);
		}
		already_computed[to_repr(n, cutoff)] = result;
		return result;
	}
}

// n is the dimension, so should be a nonnegative integer
const dim_of_unoriented_cobordism_group = function(n) {
	return partitions_specified_by(not_generators(n), n, n);
}


/* Cobordism of unoriented manifolds together with a principal Z/2-bundle.
   This turns out to be the cumulative sum of all unoriented cobordism classes of dimension
   at most n, plus an extra copy of the top dimension.
 */
const dim_of_z2_cobordism_group = function(n) {
	let to_return = dim_of_unoriented_cobordism_group(n);
	for(let i = 0; i <= n; i++) {
		to_return += dim_of_unoriented_cobordism_group(i);
	}
	return to_return;
}

// Cobordism of stably almost complex manifolds, which is a partition function for only even-size partitions.
const dim_of_complex_cobordism_group = function(n) {
	if (n % 2 !== 0) return 0;
	return partitions_specified_by(new Set(), n/2, n/2); // this is literally the partition function
}

// tang_str is a string indicating which calculation we're doing
const main = function(tang_str) {
	let n = parseInt(document.getElementById('input_' + tang_str).value);
	if (tang_str === 'MO') {
		document.getElementById('answer_MO').innerHTML = dim_of_unoriented_cobordism_group(n);
	} else if (tang_str === 'BZ2') {
		document.getElementById('answer_BZ2').innerHTML = dim_of_z2_cobordism_group(n);
	} else if (tang_str === 'MU') {
		document.getElementById('answer_MU').innerHTML = dim_of_complex_cobordism_group(n);
	}
	document.getElementById('dim_' + tang_str).innerHTML = n;
}
