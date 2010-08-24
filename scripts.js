var allHTMLTags = new Array();
var lastClass = "";
function peek(theClass) {
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

function printAttributes(id, start, end) {
  var elem = document.getElementById("attribute-display");
  elem.innerHTML = "CorefID: " + id + 
	"<br>Starting byte: " + start + "<br>Ending byte: " + end;
}
