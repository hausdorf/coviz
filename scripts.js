var allHTMLTags = new Array();
var recentlyModified = false;
var lastClass = "";
var toMarkup = new Array();
var currColor = "333333"

// Highlight all words in a coref chain, and un-highlight
// the ones from the previous chain.
function peek(theClass) {
	if(!recentlyModified) {
		recentlyModified = true;
		var allHTMLTags = document.getElementsByTagName("*");
		for(i=0; i<allHTMLTags.length;i++) {
		  if(allHTMLTags[i].className==lastClass) {
		    allHTMLTags[i].style.color="inherit";
		    allHTMLTags[i].style.fontWeight="inherit";
		    allHTMLTags[i].style.textDecoration="inherit";
		  }
		  if(allHTMLTags[i].className==theClass) {
		    allHTMLTags[i].style.color="blue";
		    allHTMLTags[i].style.fontWeight="bold";
		    allHTMLTags[i].style.textDecoration="underline";
		  }
		}
		lastClass = theClass;
	}
	toMarkup.push(theClass);
	setTimeout(function(){recentlyModified=false},200);
}

function cycle() {
	for(var i=0;i<toMarkup.length;i++) {
		var tmpClass = toMarkup.pop();
		var allHTMLTags = document.getElementsByTagName("*");
		for(i=0; i<allHTMLTags.length;i++) {
		  if(allHTMLTags[i].className==(tmpClass+"-tracking")) {
		    allHTMLTags[i].style.color=currColor;
		    allHTMLTags[i].style.fontWeight="bold";
		    allHTMLTags[i].style.textDecoration="underline";
		  }
		}
	}
	currColor = (parseInt(currColor, 16) + 30000).toString(16);
}

function printAttributes(id, start, end) {
	var elem = document.getElementById("attribute-display");
	elem.innerHTML = "CorefID: " + id + 
		"<br>Starting byte: " + start + "<br>Ending byte: " + end;
}

// Add event handlers for every single NP
document.addEventListener("DOMContentLoaded", function() {
	allHTMLTags = document.getElementsByTagName("*");
	for(i=0;i<allHTMLTags.length;i++) {
		// TODO TODO TODO: Make this only work if we can parse an int out of it!
		if(allHTMLTags[i].className!=("")) {
			// Hack: in JS, you are not allowed to re-declare variables, so you have to
			// double-bind it to create a new execution context. Adding this code
			// lets us automate the adding of event handlers for any arbitrary id/class
			// tag we choose (in this case, the ids will represent the bytespan #, but
			// could concievably be anything).
			setTimeout((function (_tag, _class) {
				return function () {
					_tag.addEventListener("click", function(event){peek(_class);setTimeout(function(){cycle();}, 500);}, false);
				}
			})(allHTMLTags[i], allHTMLTags[i].className), i * 100);
		}
	}
}, false);