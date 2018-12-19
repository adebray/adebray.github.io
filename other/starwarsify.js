// Preset information, stored as an array of dicts
all_episodes_info = [
	/* Spaceballs */ {
		title: 'Chapter Eleven',
		subtitle: '',
		text: '<p>The evil leaders of Planet Spaceball, having foolishly squandered their precious atmosphere, have devised a secret plan to take every breath of air away from their peace-loving neighbor, Planet Druidia.</p><p>Today is Princess Vespa\'s wedding day. Unbeknownest to the princess, but knownst to us, danger lurks in the stars above...</p><p>If you can read this, you don\'t need glasses.</p>'
	},
	/* Phantom Menace */ {
		title: "THE PHANTOM MENACE",
		subtitle: "Episode I",
		text: "<p>Turmoil has engulfed the Galactic Republic. The taxation of trade routes to outlying star systems is in dispute.</p><p>Hoping to resolve the matter with a blockade of deadly battleships, the greedy Trade Federation has stopped all shipping to the small planet of Naboo.</p><p>While the Congress of the Republic endlessly debates this alarming chain of events, the Supreme Chancellor has secretly dispatched two Jedi Knights, the guardians of peace and justice in the galaxy, to settle the conflict....</p>"
	},
	/* Attack of the Clones */ {
		title: "ATTACK OF THE CLONES",
		subtitle: "Episode II",
		text: '<p>There is unrest in the Galactic Senate. Several thousand solar systems have declared their intentions to leave the Republic.</p><p>This separatist movement, under the leadership of the mysterious Count Dooku, has made it difficult for the limited number of Jedi Knights to maintain peace and order in the galaxy.</p><p>Senator Amidala, the former Queen of Naboo, is returning to the Galactic Senate to vote on the critical issue of creating an ARMY OF THE REPUBLIC to assist the overwhelmed Jedi....</p>'
	},
	/* Revenge of the Sith */ {
		title: "REVENGE OF THE SITH",
		subtitle: "Episode III",
		text: '<p>War! The Republic is crumbling under attacks by the ruthless Sith Lord, Count Dooku. There are heroes on both sides. Evil is everywhere.</p><p>In a stunning move, the fiendish droid leader, General Grievous, has swept into the Republic capital and kidnapped Chancellor Palpatine, leader of the Galactic Senate.</p><p>As the Separatist Droid Army attempts to flee the besieged capital with their valuable hostage, two Jedi Knights lead a desperate mission to rescue the captive Chancellor....</p>'
	},
	/* A New Hope */ {
		title: "A NEW HOPE",
		subtitle: "Episode IV",
		text: "<p>It is a period of civil war. Rebel spaceships, striking from a hidden base, have won their first victory against the evil Galactic Empire.</p><p>During the battle, Rebel spies managed to steal secret plans to the Empire's ultimate weapon, the DEATH STAR, an armored space station with enough power to destroy an entire planet.</p><p>Pursued by the Empire's sinister agents, Princess Leia races home aboard her starship, custodian of the stolen plans that can save her people and restore freedom to the galaxy.....</p>"
	},
	/* The Empire Strikes Back */ {
		title: "THE EMPIRE STRIKES BACK",
		subtitle: "Episode V",
		text: "<p>It is a dark time for the Rebellion. Although the Death Star has been destroyed, Imperial troops have driven the Rebel forces from their hidden base and pursued them across the galaxy.</p><p>Evading the dreaded Imperial Starfleet, a group of freedom fighters led by Luke Skywalker has established a new secret base on the remote ice world of Hoth.</p><p>The evil lord Darth Vader, obsessed with finding young Skywalker, has dispatched thousands of remote probes into the far reaches of space....</p>"
	},
	/* Return of the Jedi */ {
		title: "RETURN OF THE JEDI",
		subtitle: "Episode VI",
		text: "<p>Luke Skywalker has returned to his home planet of Tatooine in an attempt to rescue his friend Han Solo from the clutches of the vile gangster Jabba the Hutt.</p><p>Little does Luke know that the GALACTIC EMPIRE has secretly begun construction on a new armored space station even more powerful than the first dreaded Death Star.</p><p>When completed, this ultimate weapon will spell certain doom for the small band of rebels struggling to restore freedom to the galaxy...</p>"
	},
	/* The Force Awakens */ {
		title: "THE FORCE AWAKENS",
		subtitle: "Episode VII",
		text: "<p>Luke Skywalker has vanished. In his absence, the sinister FIRST ORDER has risen from the ashes of the Empire and will not rest until Skywalker, the last Jedi, has been destroyed.</p><p>With the support of the REPUBLIC, General Leia Organa leads a brave RESISTANCE. She is desperate to find her brother Luke and gain his help in restoring peace and justice to the galaxy.</p><p>Leia has sent her most daring pilot on a secret mission to Jakku, where an old ally has discovered a clue to Luke's whereabouts....</p>"
	},
	/* The Last Jedi */ {
		title: "THE LAST JEDI",
		subtitle: "Episode VIII",
		text: "<p>The FIRST ORDER reigns. Having decimated the peaceful Republic, Supreme Leader Snoke now deploys the merciless legions to seize military control of the galaxy.</p><p>Only General Leia Organa's band of RESISTANCE fighters stand against the rising tyranny, certain that Jedi Master Luke Skywalker will return and restore a spark of hope to the fight.</p><p>But the Resistance has been exposed. As the First Order speeds toward the rebel base, the brave heroes mount a desperate escape....</p>"
	},
	/* The Third Gather */ {
		title: "THE BACKSTROKE OF THE WEST",
		subtitle: "The Third Gather",
		text: "<p>The war came! The republic encountered Two squares fight the vehemence The improbity fills the world</p><p>The space general of the alliance is skillful Kidnap the D the speaker the conduct  The proper abruption alliance troops tries ratio prosperous drive with the</p>"
	}
]

// Given the id of an element, add the line `update` to its CSS.
const update_css = function(id, update) {
	document.getElementById(id).setAttribute('style', update);
}

// Takes the text inside the input form `source` and puts it in the innerHTML of `target`.
const update_text = function(target, source) {
	document.getElementById(target).innerHTML = document.getElementById(source).value;
}

const set_value_by_id = function(id, to_set) {
	document.getElementById(id).value = to_set;
}

// from Stackoverflow
const sleep = function(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}

// Adds an event listener for the specified button and function. Button specified by id
const button_event_listener = function(button, fn) {
	document.getElementById(button).addEventListener('click', fn, false);
}

// Attempts to make this work well on different-sized screens
const screen_size_adjustments = function() {
	// horizontal, resp.\ vertical scale factor relative to my screen
	const scale_x = window.innerWidth / 1350.0;
	const scale_y = window.innerHeight / 800.0;

	update_css('track', 'margin-top: ' + (-120 / scale_x).toString() + 'pt');
	//console.log(document.getElementById('track').style.marginTop);
}

async function start_animation() {
	update_css('pre_animation', 'display: none');
	
	// first, the "a long time ago" bit
	document.body.setAttribute('style', 'background-color: black')
	update_css("longtime", "visibility: visible");
	update_css('longanim', 'animation-play-state: running')
	await sleep(5000);
	update_css("longtime", "display: none");

	// TODO: the STAR WARS bit (or Spaceballs I guess?)

	// Then the opening crawl
	update_text('just_the_title', 'crawl_title');
	update_text('subtitle', 'crawl_subtitle');
	update_text('crawl_body', 'crawl_text');

	screen_size_adjustments();

	update_css('track', 'visibility: visible')
	update_css('crawler', 'animation-play-state: running')
}

const prefill = function() {
	const episode = parseInt(document.getElementById('presets').value);
	const episode_data = all_episodes_info[episode];
	set_value_by_id('crawl_title', episode_data.title)
	set_value_by_id('crawl_subtitle', episode_data.subtitle)
	set_value_by_id('crawl_text', episode_data.text)
}

window.onload = function() {
	button_event_listener('animation_button', start_animation);
	button_event_listener('apply_preset', prefill);
}
