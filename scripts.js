var leftModified = new function() { this.condition = false; }
var rightModified = new function() { this.condition = false; }
var lastLeftClassUpdated = new function() { this.value = ""; };
var lastRightClassUpdated = new function() { this.value = ""; };
var currColor = "333333";

function clickNpLeftDoc(classToShow, assocNps) {
	var lockingBool = leftModified;
	if(!lockingBool.condition) {
		lockingBool.condition = true;
		highlightChain(classToShow, "left");
		cycle(assocNps);
	}
	setTimeout(function(){lockingBool.condition=false},200);
}

function clickNpRightDoc(classToShow) {
	highlightChain(classToShow, "right");
}

function highlightChain(classToShow, leftOrRight) {
	var lastClassUpdated;
	var textToAddToClass = "";
	var allHtmlTags = document.getElementsByTagName("*");

	if(leftOrRight == "left") {
		lockingBool = leftModified;
		lastClassUpdated = lastLeftClassUpdated;
		textToAddToClass = "";
	}
	else if (leftOrRight == "right") {
		lockingBool = rightModified;
		lastClassUpdated = lastRightClassUpdated;
		textToAddToClass = "-tracking";
	}
	else {
		throw "highlight chain leftOrRight param does not accept " + leftOrRight +
		" as valid input";
	}

	for(i=0; i<allHtmlTags.length; i++) {
		if(allHtmlTags[i].className==lastClassUpdated.value + textToAddToClass) {
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
	lastClassUpdated.value = classToShow;
}

function cycle(assocNps) {
	for(var i = 0; i < assocNps.length; i++) {
		var tmpClass = assocNps[i];
		var allHTMLTags = document.getElementsByTagName("*");
		for(var n = 0; n < allHTMLTags.length; n++) {
			if(allHTMLTags[n].className==(tmpClass+"-tracking")) {
				allHTMLTags[n].style.color=currColor;
				allHTMLTags[n].style.fontWeight="bold";
				allHTMLTags[n].style.textDecoration="underline";
			}
		}
		currColor = (parseInt(currColor, 16) + 30000).toString(16);
	}
}

function printAttributes(id, start, end) {
	var elem = document.getElementById("attribute-display");
	elem.innerHTML = "CorefID: " + id + 
		"<br>Starting byte: " + start + "<br>Ending byte: " + end;
}

// Add event handlers for every single NP
document.addEventListener("DOMContentLoaded", function() {
	var allHtmlTags = document.getElementsByTagName("*");
	for(i=0;i<allHtmlTags.length;i++) {
		// TODO TODO TODO: Make this only work if we can parse an int out of it!
		if(allHtmlTags[i].className!=("")) {
			// Hack: in JS, you are not allowed to re-declare variables, so you have to
			// double-bind it to create a new execution context. Adding this code
			// lets us automate the adding of event handlers for any arbitrary id/class
			// tag we choose, rather than to manually enumerate the adding of event
			// handlers for all possible tag ids.
			setTimeout((function (_tag, _class, _assocAttr) {
				return function () {
					_tag.addEventListener("click", function(event) {
						clickNpLeftDoc(_class, _assocAttr.nodeValue.split(","));
					}, false);
				}
			})(allHtmlTags[i], allHtmlTags[i].className, allHtmlTags[i].attributes[2]), 100);
		}
	}
}, false);