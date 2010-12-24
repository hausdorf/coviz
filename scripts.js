var allHTMLTags = new Array();
var recentlyModified = false;
var otherRecentlyModified = false;
var lastClass = "";
var leftModified = new function() { this.condition = false; }
var rightModified = new function() { this.condition = false; }
var lastClassUpdated = "";
var lastOtherClass = "";
var toMarkup = new Array();
var currColor = "333333"

function clickNpLeftDoc(classToShow) {
	highlightChain(classToShow, "left");
}

function clickNpRightDoc(classToShow) {
	highlightChain(classToShow, "right");
}

function highlightChain(classToShow, leftOrRight) {
	var textToAddToClass = "";
	var allHtmlTags = document.getElementsByTagName("*");

	if(leftOrRight == "left") {
		lockingBool = leftModified;
		textToAddToClass = "";
	}
	else if (leftOrRight == "right") {
		lockingBool = rightModified;
		textToAddToClass = "-tracking";
	}
	else {
		throw "highlight chain leftOrRight param does not accept " + leftOrRight +
		" as valid input";
	}

	if(!lockingBool.condition) {
		lockingBool.condition = true;
		for(i=0; i<allHtmlTags.length; i++) {
			if(allHtmlTags[i].className==lastClassUpdated + textToAddToClass) {
				allHtmlTags[i].style.color="inherit";
				allHtmlTags[i].style.fontWeight="inherit";
				allHtmlTags[i].style.textDecoration="inherit";
			}
			if(allHtmlTags[i].className==classToShow + textToAddToClass) {
				allHtmlTags[i].style.color="blue";
				allHtmlTags[i].style.fontWeight="bold";
				allHtmlTags[i].style.textDecoration="underline";
			}
		}
		lastClassUpdated = classToShow;
	}
	setTimeout(function(){lockingBool.condition=false},200);
}

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

function peekOther(theClass) {
	if(!otherRecentlyModified) {
		otherRecentlyModified = true;
		var allHTMLTags = document.getElementsByTagName("*");
		for(i=0; i<allHTMLTags.length;i++) {
			if(allHTMLTags[i].className==lastOtherClass+"-tracking") {
				allHTMLTags[i].style.color="inherit";
				allHTMLTags[i].style.fontWeight="inherit";
				allHTMLTags[i].style.textDecoration="inherit";
			}
			if(allHTMLTags[i].className==(theClass+"-tracking")) {
				allHTMLTags[i].style.color="blue";
				allHTMLTags[i].style.fontWeight="bold";
				allHTMLTags[i].style.textDecoration="underline";
			}
		}
		lastOtherClass = theClass;
	}
	setTimeout(function(){otherRecentlyModified=false},200);
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
			// tag we choose, rather than to manually enumerate the adding of event
			// handlers for all possible tag ids.
			setTimeout((function (_tag, _class, _assocAttr) {
				return function () {
					_tag.addEventListener("click", function(event) {
						clickNpLeftDoc(_class);
						clickNpRightDoc(_assocAttr.nodeValue);
					}, false);
				}
			})(allHTMLTags[i], allHTMLTags[i].className, allHTMLTags[i].attributes[3]), 100);
		}
	}
}, false);